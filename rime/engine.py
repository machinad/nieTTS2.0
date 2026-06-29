"""
RimeEngine — librime 的高层 Python 封装。

自动管理会话生命周期，提供简洁的输入法操作接口。
所有 T1-T6 级别的 API 统一通过此层调用。

线程安全：此类不是线程安全的。每个线程应使用独立的 RimeEngine 实例。
"""

import logging
import time
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger("rime")

from rime._utils import find_data_dir
from rime.binding import (
    RimeApiWrapper,
    RimeConfig,
    RimeNotificationHandler,
    RimeTraits,
    rime_struct_init,
)


@dataclass
class InputResult:
    """按键处理的结果。

    Attributes:
        committed: 已上屏的文本（无提交时为 None）
        preedit: 当前拼音组合（如 "zhong"）
        candidates: 候选词列表
        page_no: 当前候选词页码
        is_last_page: 是否最后一页
        highlighted: 高亮候选词的页内索引
    """

    committed: str | None = None
    preedit: str = ""
    candidates: list[str] = field(default_factory=list)
    page_no: int = 0
    is_last_page: bool = False
    highlighted: int = 0


@dataclass
class StatusInfo:
    """引擎状态信息。

    Attributes:
        schema_id: 当前方案 ID
        schema_name: 当前方案名称
        is_composing: 是否正在输入中
        is_ascii_mode: 是否英文模式
        is_full_shape: 是否全角
        is_simplified: 是否简体
        is_traditional: 是否繁体
        is_ascii_punct: 是否英文标点
        is_disabled: 是否已禁用
    """

    schema_id: str = ""
    schema_name: str = ""
    is_composing: bool = False
    is_ascii_mode: bool = False
    is_full_shape: bool = False
    is_simplified: bool = False
    is_traditional: bool = False
    is_ascii_punct: bool = False
    is_disabled: bool = False


class RimeEngine:
    """RIME 输入法引擎。

    封装了 librime 的会话管理，提供简洁的输入法操作接口。
    所有 T1-T6 级别的 API 统一通过此类调用。

    支持上下文管理器，自动处理 shutdown：
        with RimeEngine(user_data_dir="./data") as engine:
            engine.process_key(ord('a'))

    线程安全：此类不是线程安全的。每个线程应使用独立的 RimeEngine 实例。

    Args:
        shared_data_dir: 方案数据目录，None 则使用包内数据
        user_data_dir: 用户数据目录，None 则使用 ./rime_user_data
        dll_path: librime.dll 路径，None 则自动搜索
        schema_id: 初始方案 ID，默认 luna_pinyin
    """

    # X11 keysym 常量
    XK_BackSpace = 0xFF08
    XK_Return = 0xFF0D
    XK_space = 0x0020
    XK_Escape = 0xFF1B

    def __init__(
        self,
        shared_data_dir: str | None = None,
        user_data_dir: str | None = None,
        dll_path: str | None = None,
        schema_id: str = "luna_pinyin",
    ):
        self._shared_data_dir = shared_data_dir or find_data_dir()
        self._user_data_dir = user_data_dir or str(Path.cwd() / "rime_user_data")
        self._schema_id = schema_id
        self._session_id: int = 0
        self._deployed = False

        # 加载底层 API
        self._api = RimeApiWrapper(dll_path)

        # 通知回调（保持引用防止 GC）
        self._notify_cb = RimeNotificationHandler(self._on_notification)

        # 初始化引擎
        self._init_traits()

    def _init_traits(self):
        """设置 RimeTraits 并初始化引擎。"""
        traits = RimeTraits()
        rime_struct_init(traits)

        traits.shared_data_dir = self._shared_data_dir.encode("utf-8")
        traits.user_data_dir = self._user_data_dir.encode("utf-8")
        traits.distribution_name = b"rime-python"
        traits.distribution_code_name = b"rime-python"
        traits.distribution_version = b"0.1.0"
        traits.app_name = b"rime-python"
        traits.min_log_level = 3  # WARNING

        self._api.setup(traits)
        self._api.set_notification_handler(self._notify_cb)
        self._api.initialize(traits)

    def _on_notification(self, _context_object, _session_id, message_type, message_value):
        """librime 部署通知回调（内部使用）。"""
        t = self._api._decode(message_type) or ""
        v = self._api._decode(message_value) or ""
        logger.info("%s: %s", t, v)

    # ══════════════════════════════════════════
    # T5: 部署与维护
    # ══════════════════════════════════════════

    def deploy(self, timeout: float = 60.0):
        """部署输入法方案。

        编译方案数据、创建会话、选择方案。
        必须在 process_key 之前调用。

        Args:
            timeout: 部署超时时间（秒）

        Raises:
            TimeoutError: 部署超时
            RuntimeError: 会话创建失败或方案不存在
        """
        Path(self._user_data_dir).mkdir(parents=True, exist_ok=True)

        self._api.start_maintenance(full_check=True)

        deadline = time.monotonic() + timeout
        while self._api.is_maintenance_mode():
            time.sleep(0.1)
            if time.monotonic() > deadline:
                raise TimeoutError(f"RIME 部署超时，请检查方案数据是否完整：{self._shared_data_dir}")

        self._api.join_maintenance_thread()

        self._session_id = self._api.create_session()
        if not self._session_id:
            raise RuntimeError("创建 RIME 会话失败")

        ok = self._api.select_schema(self._session_id, self._schema_id)
        if not ok:
            schemas = self._api.get_schema_list()
            available = [s["schema_id"] for s in schemas]
            raise RuntimeError(f"方案 '{self._schema_id}' 不存在，可用方案：{available}")

        self._deployed = True

        # 默认启用简体中文
        self._api.set_option(self._session_id, "zh_hans", True)

        logger.info("已部署方案: %s", self._schema_id)
        logger.info("librime 版本: %s", self._api.get_version())

    def start_maintenance(self, full_check: bool = True) -> bool:
        """启动部署维护（重新编译方案数据）。

        Args:
            full_check: 是否完整检查

        Returns:
            是否成功启动
        """
        return self._api.start_maintenance(full_check)

    def is_maintenance_mode(self) -> bool:
        """查询是否正在维护中。

        Returns:
            True 表示正在编译方案数据
        """
        return self._api.is_maintenance_mode()

    def join_maintenance_thread(self):
        """等待维护线程结束。"""
        self._api.join_maintenance_thread()

    def sync_user_data(self) -> bool:
        """同步用户数据（如用户词库）。

        Returns:
            是否成功同步
        """
        return self._api.sync_user_data()

    def deploy_schema(self, schema_file: str) -> bool:
        """部署指定的方案文件。

        Args:
            schema_file: 方案文件路径

        Returns:
            是否成功部署
        """
        return self._api.deploy_schema(schema_file)

    # ══════════════════════════════════════════
    # T1: 核心输入
    # ══════════════════════════════════════════

    def process_key(self, keycode: int, mask: int = 0) -> InputResult:
        """处理按键事件。

        Args:
            keycode: X11 keysym 值（如 ord('a')、0xFF08 表示退格）
            mask: 修饰键掩码（0 = 无）

        Returns:
            InputResult 包含提交文本、预编辑、候选词等
        """
        self._ensure_deployed()
        result = InputResult()

        handled = self._api.process_key(self._session_id, keycode, mask)
        if not handled:
            return result

        committed = self._api.get_commit(self._session_id)
        if committed is not None:
            result.committed = committed

        self._read_context(result)
        return result

    def select_candidate_on_page(self, index: int) -> InputResult:
        """按页内索引选择候选词。

        Args:
            index: 页内索引（从 0 开始）

        Returns:
            InputResult 包含提交文本和更新后的候选词
        """
        self._ensure_deployed()
        result = InputResult()

        self._api.select_candidate_on_current_page(self._session_id, index)

        committed = self._api.get_commit(self._session_id)
        if committed is not None:
            result.committed = committed

        self._read_context(result)
        return result

    def select_candidate(self, index: int) -> InputResult:
        """按全局索引选择候选词。

        Args:
            index: 全局索引（跨页连续编号）

        Returns:
            InputResult
        """
        self._ensure_deployed()
        result = InputResult()

        self._api.select_candidate(self._session_id, index)

        committed = self._api.get_commit(self._session_id)
        if committed is not None:
            result.committed = committed

        self._read_context(result)
        return result

    def change_page(self, backward: bool = False) -> InputResult:
        """翻页。

        Args:
            backward: True 为上一页，False 为下一页

        Returns:
            InputResult 包含翻页后的候选词
        """
        self._ensure_deployed()
        result = InputResult()

        self._api.change_page(self._session_id, backward)

        committed = self._api.get_commit(self._session_id)
        if committed is not None:
            result.committed = committed

        self._read_context(result)
        return result

    def delete_candidate_on_page(self, index: int) -> bool:
        """按页内索引删除候选词。

        Args:
            index: 页内索引（从 0 开始）

        Returns:
            是否成功删除
        """
        self._ensure_deployed()
        return self._api.delete_candidate_on_current_page(self._session_id, index)

    def delete_candidate(self, index: int) -> bool:
        """按全局索引删除候选词。

        Args:
            index: 全局索引

        Returns:
            是否成功删除
        """
        self._ensure_deployed()
        return self._api.delete_candidate(self._session_id, index)

    def highlight_candidate_on_page(self, index: int) -> bool:
        """按页内索引高亮候选词。

        Args:
            index: 页内索引

        Returns:
            是否成功高亮
        """
        self._ensure_deployed()
        return self._api.highlight_candidate_on_current_page(self._session_id, index)

    def highlight_candidate(self, index: int) -> bool:
        """按全局索引高亮候选词。

        Args:
            index: 全局索引

        Returns:
            是否成功高亮
        """
        self._ensure_deployed()
        return self._api.highlight_candidate(self._session_id, index)

    def commit_current(self) -> str | None:
        """强制提交当前组合文本。

        Returns:
            提交的文本，无内容时返回 None
        """
        self._ensure_deployed()
        if self._api.commit_composition(self._session_id):
            return self._api.get_commit(self._session_id)
        return None

    def clear(self):
        """清空当前输入组合。"""
        self._ensure_deployed()
        self._api.clear_composition(self._session_id)

    def get_input(self) -> str | None:
        """获取原始输入字符串。

        Returns:
            当前输入的原始字符串（如 "zhong"），无输入时返回 None
        """
        self._ensure_deployed()
        return self._api.get_input(self._session_id)

    def get_caret_pos(self) -> int:
        """获取光标位置。

        Returns:
            光标在输入串中的位置
        """
        self._ensure_deployed()
        return self._api.get_caret_pos(self._session_id)

    def set_caret_pos(self, pos: int):
        """设置光标位置。

        Args:
            pos: 光标位置
        """
        self._ensure_deployed()
        self._api.set_caret_pos(self._session_id, pos)

    def set_input(self, text: str) -> bool:
        """直接设置输入字符串。

        Args:
            text: 要设置的输入文本

        Returns:
            是否成功
        """
        self._ensure_deployed()
        return self._api.set_input(self._session_id, text)

    def simulate_key_sequence(self, key_sequence: str) -> InputResult:
        """模拟按键序列（主要用于测试）。

        Args:
            key_sequence: 按键序列字符串

        Returns:
            InputResult
        """
        self._ensure_deployed()
        result = InputResult()

        handled = self._api.simulate_key_sequence(self._session_id, key_sequence)
        if not handled:
            return result

        committed = self._api.get_commit(self._session_id)
        if committed is not None:
            result.committed = committed

        self._read_context(result)
        return result

    # ══════════════════════════════════════════
    # T2: 方案管理
    # ══════════════════════════════════════════

    def get_schema_list(self) -> list[dict]:
        """获取所有可用输入方案。

        Returns:
            方案列表，每项包含 schema_id 和 name
        """
        return self._api.get_schema_list()

    def get_current_schema(self) -> str | None:
        """获取当前输入方案 ID。

        Returns:
            方案 ID 字符串（如 "luna_pinyin"）
        """
        self._ensure_deployed()
        return self._api.get_current_schema(self._session_id)

    def switch_schema(self, schema_id: str) -> bool:
        """运行时切换输入方案。

        Args:
            schema_id: 目标方案 ID

        Returns:
            是否成功切换
        """
        self._ensure_deployed()
        ok = self._api.select_schema(self._session_id, schema_id)
        if ok:
            self._schema_id = schema_id
        return ok

    # ══════════════════════════════════════════
    # T3: 选项控制
    # ══════════════════════════════════════════

    def set_option(self, option: str, value: bool):
        """设置布尔选项。

        常用选项：
        - ascii_mode: 英文模式
        - zh_hans: 简体中文
        - zh_hant: 繁体中文
        - full_shape: 全角
        - ascii_punct: 英文标点

        Args:
            option: 选项名称
            value: 选项值
        """
        self._ensure_deployed()
        self._api.set_option(self._session_id, option, value)

    def get_option(self, option: str) -> bool:
        """获取布尔选项值。

        Args:
            option: 选项名称

        Returns:
            选项当前值
        """
        self._ensure_deployed()
        return self._api.get_option(self._session_id, option)

    def set_property(self, key: str, value: str):
        """设置字符串属性。

        Args:
            key: 属性名
            value: 属性值
        """
        self._ensure_deployed()
        self._api.set_property(self._session_id, key, value)

    def get_property(self, key: str) -> str | None:
        """获取字符串属性。

        Args:
            key: 属性名

        Returns:
            属性值，不存在时返回 None
        """
        self._ensure_deployed()
        return self._api.get_property(self._session_id, key)

    def get_state_label(self, option_name: str, state: bool) -> str | None:
        """获取选项状态的显示标签。

        Args:
            option_name: 选项名称
            state: 选项状态

        Returns:
            标签文本（如 "中"/"西"、"简"/"繁"）
        """
        self._ensure_deployed()
        return self._api.get_state_label(self._session_id, option_name, state)

    def toggle_ascii_mode(self):
        """切换中英文模式。"""
        self._ensure_deployed()
        current = self._api.get_option(self._session_id, "ascii_mode")
        self._api.set_option(self._session_id, "ascii_mode", not current)

    def get_ascii_mode(self) -> bool:
        """查询当前是否英文模式。

        Returns:
            True 表示英文模式
        """
        self._ensure_deployed()
        return self._api.get_option(self._session_id, "ascii_mode")

    # ══════════════════════════════════════════
    # T4: 状态查询
    # ══════════════════════════════════════════

    def get_status(self) -> StatusInfo:
        """获取引擎当前状态。

        Returns:
            StatusInfo 包含方案、模式等状态信息
        """
        self._ensure_deployed()
        status = self._api.get_status(self._session_id)
        if status is None:
            return StatusInfo()

        info = StatusInfo(
            schema_id=self._api._decode(status.schema_id) or "",
            schema_name=self._api._decode(status.schema_name) or "",
            is_composing=bool(status.is_composing),
            is_ascii_mode=bool(status.is_ascii_mode),
            is_full_shape=bool(status.is_full_shape),
            is_simplified=bool(status.is_simplified),
            is_traditional=bool(status.is_traditional),
            is_ascii_punct=bool(status.is_ascii_punct),
            is_disabled=bool(status.is_disabled),
        )
        self._api.free_status(status)
        return info

    def get_version(self) -> str | None:
        """获取 librime 版本号。

        Returns:
            版本字符串（如 "1.17.0"）
        """
        return self._api.get_version()

    # ══════════════════════════════════════════
    # T6: 配置读写
    # ══════════════════════════════════════════

    def config_open(self, config_id: str) -> RimeConfig | None:
        """打开配置文件。

        Args:
            config_id: 配置 ID（如 "luna_pinyin"）

        Returns:
            RimeConfig 句柄，失败返回 None
        """
        config = RimeConfig()
        if self._api.config_open(config_id, config):
            return config
        return None

    def config_close(self, config: RimeConfig) -> bool:
        """关闭配置文件。

        Args:
            config: 配置句柄

        Returns:
            是否成功关闭
        """
        return self._api.config_close(config)

    def config_get_bool(self, config: RimeConfig, key: str) -> bool | None:
        """读取布尔配置值。

        Args:
            config: 配置句柄
            key: 配置键（如 "ascii_composer/switch_key/Shift_L"）

        Returns:
            配置值，不存在返回 None
        """
        return self._api.config_get_bool(config, key)

    def config_get_int(self, config: RimeConfig, key: str) -> int | None:
        """读取整数配置值。

        Args:
            config: 配置句柄
            key: 配置键（如 "menu/page_size"）

        Returns:
            配置值，不存在返回 None
        """
        return self._api.config_get_int(config, key)

    def config_get_double(self, config: RimeConfig, key: str) -> float | None:
        """读取浮点配置值。

        Args:
            config: 配置句柄
            key: 配置键

        Returns:
            配置值，不存在返回 None
        """
        return self._api.config_get_double(config, key)

    def config_get_string(self, config: RimeConfig, key: str) -> str | None:
        """读取字符串配置值。

        Args:
            config: 配置句柄
            key: 配置键（如 "translator/dictionary"）

        Returns:
            配置值，不存在返回 None
        """
        return self._api.config_get_string(config, key)

    def config_set_bool(self, config: RimeConfig, key: str, value: bool) -> bool:
        """写入布尔配置值。

        Args:
            config: 配置句柄
            key: 配置键
            value: 要设置的值

        Returns:
            是否成功
        """
        return self._api.config_set_bool(config, key, value)

    def config_set_int(self, config: RimeConfig, key: str, value: int) -> bool:
        """写入整数配置值。

        Args:
            config: 配置句柄
            key: 配置键
            value: 要设置的值

        Returns:
            是否成功
        """
        return self._api.config_set_int(config, key, value)

    def config_set_double(self, config: RimeConfig, key: str, value: float) -> bool:
        """写入浮点配置值。

        Args:
            config: 配置句柄
            key: 配置键
            value: 要设置的值

        Returns:
            是否成功
        """
        return self._api.config_set_double(config, key, value)

    def config_set_string(self, config: RimeConfig, key: str, value: str) -> bool:
        """写入字符串配置值。

        Args:
            config: 配置句柄
            key: 配置键
            value: 要设置的值

        Returns:
            是否成功
        """
        return self._api.config_set_string(config, key, value)

    def config_clear(self, config: RimeConfig, key: str) -> bool:
        """清除配置项。

        Args:
            config: 配置句柄
            key: 配置键

        Returns:
            是否成功
        """
        return self._api.config_clear(config, key)

    def config_create_list(self, config: RimeConfig, key: str) -> bool:
        """创建空列表配置项。

        Args:
            config: 配置句柄
            key: 配置键

        Returns:
            是否成功
        """
        return self._api.config_create_list(config, key)

    def config_create_map(self, config: RimeConfig, key: str) -> bool:
        """创建空映射配置项。

        Args:
            config: 配置句柄
            key: 配置键

        Returns:
            是否成功
        """
        return self._api.config_create_map(config, key)

    def config_list_size(self, config: RimeConfig, key: str) -> int:
        """获取列表配置项的大小。

        Args:
            config: 配置句柄
            key: 配置键

        Returns:
            列表大小
        """
        return self._api.config_list_size(config, key)

    def schema_open(self, schema_id: str) -> RimeConfig | None:
        """打开方案配置。

        Args:
            schema_id: 方案 ID

        Returns:
            RimeConfig 句柄，失败返回 None
        """
        config = RimeConfig()
        if self._api.schema_open(schema_id, config):
            return config
        return None

    # ══════════════════════════════════════════
    # 生命周期
    # ══════════════════════════════════════════

    def __enter__(self):
        """上下文管理器入口：自动调用 deploy()。"""
        self.deploy()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口：自动调用 shutdown()。"""
        self.shutdown()
        return False

    def __del__(self):
        """析构函数：确保资源被释放。"""
        if getattr(self, "_session_id", 0):
            try:
                self.shutdown()
            except Exception:
                pass

    def shutdown(self):
        """销毁会话并释放引擎资源。"""
        if self._session_id:
            self._api.destroy_session(self._session_id)
            self._session_id = 0
        self._api.finalize()
        self._deployed = False

    # ══════════════════════════════════════════
    # 内部方法
    # ══════════════════════════════════════════

    def _ensure_deployed(self):
        """确保引擎已部署。"""
        if not self._deployed:
            raise RuntimeError("引擎未部署，请先调用 deploy()")

    def _read_context(self, result: InputResult):
        """读取输入上下文（预编辑 + 候选词）。"""
        ctx = self._api.get_context(self._session_id)
        if ctx is None:
            return

        try:
            # 读取预编辑文本
            if ctx.composition.length > 0 and ctx.composition.preedit:
                preedit_raw = ctx.composition.preedit
                result.preedit = preedit_raw.decode("utf-8", errors="replace") if preedit_raw else ""

            # 读取候选词（直接访问数组，不用迭代器）
            num = ctx.menu.num_candidates
            if num > 0 and ctx.menu.candidates:
                for i in range(num):
                    cand = ctx.menu.candidates[i]
                    text = self._api._decode(cand.text) or ""
                    comment = self._api._decode(cand.comment) or ""
                    if comment:
                        result.candidates.append(f"{text} {comment}")
                    else:
                        result.candidates.append(text)

            result.page_no = ctx.menu.page_no
            result.is_last_page = bool(ctx.menu.is_last_page)
            result.highlighted = ctx.menu.highlighted_candidate_index

        finally:
            self._api.free_context(ctx)
