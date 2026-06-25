"""
librime.dll 的 ctypes 绑定。

结构体布局严格匹配 rime_api.h（字段顺序和类型完全一致）。
所有字符串参数自动处理 UTF-8 编码/解码。
"""

import ctypes
from ctypes import (
    Structure, CFUNCTYPE, POINTER, byref, cast,
    c_int, c_char, c_char_p, c_void_p, c_size_t, c_double,
)
import os
from pathlib import Path

from rime._utils import find_dll


# ──────────────────────────────────────────────
# 类型别名
# ──────────────────────────────────────────────
Bool = c_int            # librime 使用 int 表示 bool
RimeSessionId = c_size_t  # typedef uintptr_t

# 通知回调类型
RimeNotificationHandler = CFUNCTYPE(
    None, c_void_p, RimeSessionId, c_char_p, c_char_p
)


# ──────────────────────────────────────────────
# 数据结构体（无 data_size 版本控制）
# ──────────────────────────────────────────────
class RimeComposition(Structure):
    """输入组合信息（拼音预编辑）。"""
    _fields_ = [
        ("length", c_int),
        ("cursor_pos", c_int),
        ("sel_start", c_int),
        ("sel_end", c_int),
        ("preedit", c_char_p),
    ]


class RimeCandidate(Structure):
    """单个候选词。"""
    _fields_ = [
        ("text", c_char_p),
        ("comment", c_char_p),
        ("reserved", c_void_p),
    ]


class RimeMenu(Structure):
    """候选词菜单。"""
    _fields_ = [
        ("page_size", c_int),
        ("page_no", c_int),
        ("is_last_page", Bool),
        ("highlighted_candidate_index", c_int),
        ("num_candidates", c_int),
        ("candidates", POINTER(RimeCandidate)),
        ("select_keys", c_char_p),
    ]


class RimeConfig(Structure):
    """配置对象句柄。"""
    _fields_ = [("ptr", c_void_p)]


class RimeSchemaListItem(Structure):
    """方案列表中的单个条目。"""
    _fields_ = [
        ("schema_id", c_char_p),
        ("name", c_char_p),
        ("reserved", c_void_p),
    ]


class RimeSchemaList(Structure):
    """方案列表。"""
    _fields_ = [
        ("size", c_size_t),
        ("list", POINTER(RimeSchemaListItem)),
    ]


class RimeCandidateListIterator(Structure):
    """候选词列表迭代器。"""
    _fields_ = [
        ("ptr", c_void_p),
        ("index", c_int),
        ("candidate", RimeCandidate),
    ]


class RimeStringSlice(Structure):
    """字符串切片。"""
    _fields_ = [
        ("str", c_char_p),
        ("length", c_size_t),
    ]


# ──────────────────────────────────────────────
# 版本化结构体（首字段 = data_size）
# 传给 librime 前必须设置 data_size = sizeof - sizeof(int)
# 等价于 C 宏 RIME_STRUCT_INIT
# ──────────────────────────────────────────────
class RimeTraits(Structure):
    """引擎特征配置（路径、应用信息等）。"""
    _fields_ = [
        ("data_size", c_int),
        ("shared_data_dir", c_char_p),
        ("user_data_dir", c_char_p),
        ("distribution_name", c_char_p),
        ("distribution_code_name", c_char_p),
        ("distribution_version", c_char_p),
        ("app_name", c_char_p),
        ("modules", c_void_p),
        ("min_log_level", c_int),
        ("log_dir", c_char_p),
        ("prebuilt_data_dir", c_char_p),
        ("staging_dir", c_char_p),
    ]


class RimeCommit(Structure):
    """已提交的文本。"""
    _fields_ = [
        ("data_size", c_int),
        ("text", c_char_p),
    ]


class RimeContext(Structure):
    """输入上下文（组合信息 + 候选词菜单）。

    注意：commit_text_preview 是 char*（指针），不是 char[96]。
    """
    _fields_ = [
        ("data_size", c_int),
        ("composition", RimeComposition),
        ("menu", RimeMenu),
        ("commit_text_preview", c_char_p),
        ("select_labels", POINTER(c_char_p)),
    ]


class RimeStatus(Structure):
    """引擎状态信息。"""
    _fields_ = [
        ("data_size", c_int),
        ("schema_id", c_char_p),
        ("schema_name", c_char_p),
        ("is_disabled", Bool),
        ("is_composing", Bool),
        ("is_ascii_mode", Bool),
        ("is_full_shape", Bool),
        ("is_simplified", Bool),
        ("is_traditional", Bool),
        ("is_ascii_punct", Bool),
    ]


class RimeModule(Structure):
    """模块（前向声明）。"""
    pass


class RimeCustomApi(Structure):
    """自定义 API。"""
    _fields_ = [("data_size", c_int)]


# ──────────────────────────────────────────────
# RimeApi 结构体 — rime_api.h 中所有函数指针
# 严格按头文件中的顺序排列
# ──────────────────────────────────────────────
class RimeApi(Structure):
    """librime 导出的全部 API 函数指针表。"""
    _fields_ = [
        ("data_size", c_int),
        # setup
        ("setup", c_void_p),
        ("set_notification_handler", c_void_p),
        # entry / exit
        ("initialize", c_void_p),
        ("finalize", c_void_p),
        ("start_maintenance", c_void_p),
        ("is_maintenance_mode", c_void_p),
        ("join_maintenance_thread", c_void_p),
        # deployment
        ("deployer_initialize", c_void_p),
        ("prebuild", c_void_p),
        ("deploy", c_void_p),
        ("deploy_schema", c_void_p),
        ("deploy_config_file", c_void_p),
        ("sync_user_data", c_void_p),
        # session
        ("create_session", c_void_p),
        ("find_session", c_void_p),
        ("destroy_session", c_void_p),
        ("cleanup_stale_sessions", c_void_p),
        ("cleanup_all_sessions", c_void_p),
        # input
        ("process_key", c_void_p),
        ("commit_composition", c_void_p),
        ("clear_composition", c_void_p),
        # output
        ("get_commit", c_void_p),
        ("free_commit", c_void_p),
        ("get_context", c_void_p),
        ("free_context", c_void_p),
        ("get_status", c_void_p),
        ("free_status", c_void_p),
        # runtime options
        ("set_option", c_void_p),
        ("get_option", c_void_p),
        ("set_property", c_void_p),
        ("get_property", c_void_p),
        ("get_schema_list", c_void_p),
        ("free_schema_list", c_void_p),
        ("get_current_schema", c_void_p),
        ("select_schema", c_void_p),
        # config getters
        ("schema_open", c_void_p),
        ("config_open", c_void_p),
        ("config_close", c_void_p),
        ("config_get_bool", c_void_p),
        ("config_get_int", c_void_p),
        ("config_get_double", c_void_p),
        ("config_get_string", c_void_p),
        ("config_get_cstring", c_void_p),
        ("config_update_signature", c_void_p),
        ("config_begin_map", c_void_p),
        ("config_next", c_void_p),
        ("config_end", c_void_p),
        # testing
        ("simulate_key_sequence", c_void_p),
        # module
        ("register_module", c_void_p),
        ("find_module", c_void_p),
        ("run_task", c_void_p),
        # dir accessors (deprecated)
        ("get_shared_data_dir", c_void_p),
        ("get_user_data_dir", c_void_p),
        ("get_sync_dir", c_void_p),
        ("get_user_id", c_void_p),
        ("get_user_data_sync_dir", c_void_p),
        # config init / load
        ("config_init", c_void_p),
        ("config_load_string", c_void_p),
        # config setters
        ("config_set_bool", c_void_p),
        ("config_set_int", c_void_p),
        ("config_set_double", c_void_p),
        ("config_set_string", c_void_p),
        # config complex
        ("config_get_item", c_void_p),
        ("config_set_item", c_void_p),
        ("config_clear", c_void_p),
        ("config_create_list", c_void_p),
        ("config_create_map", c_void_p),
        ("config_list_size", c_void_p),
        ("config_begin_list", c_void_p),
        # input access
        ("get_input", c_void_p),
        ("get_caret_pos", c_void_p),
        ("select_candidate", c_void_p),
        ("get_version", c_void_p),
        ("set_caret_pos", c_void_p),
        ("select_candidate_on_current_page", c_void_p),
        # candidate list iteration
        ("candidate_list_begin", c_void_p),
        ("candidate_list_next", c_void_p),
        ("candidate_list_end", c_void_p),
        # user config
        ("user_config_open", c_void_p),
        ("candidate_list_from_index", c_void_p),
        # dir accessors (deprecated)
        ("get_prebuilt_data_dir", c_void_p),
        ("get_staging_dir", c_void_p),
        # proto (deprecated)
        ("commit_proto", c_void_p),
        ("context_proto", c_void_p),
        ("status_proto", c_void_p),
        # state label
        ("get_state_label", c_void_p),
        # delete candidate
        ("delete_candidate", c_void_p),
        ("delete_candidate_on_current_page", c_void_p),
        # state label abbreviated
        ("get_state_label_abbreviated", c_void_p),
        # set input
        ("set_input", c_void_p),
        # safe dir accessors
        ("get_shared_data_dir_s", c_void_p),
        ("get_user_data_dir_s", c_void_p),
        ("get_prebuilt_data_dir_s", c_void_p),
        ("get_staging_dir_s", c_void_p),
        ("get_sync_dir_s", c_void_p),
        # highlight / page
        ("highlight_candidate", c_void_p),
        ("highlight_candidate_on_current_page", c_void_p),
        ("change_page", c_void_p),
    ]


# ──────────────────────────────────────────────
# 辅助函数
# ──────────────────────────────────────────────
def rime_struct_init(instance):
    """初始化版本化结构体的 data_size 字段。

    等价于 C 宏 RIME_STRUCT_INIT：
    instance.data_size = sizeof(instance) - sizeof(int)
    """
    instance.data_size = ctypes.sizeof(instance) - ctypes.sizeof(c_int)


# ──────────────────────────────────────────────
# RimeApiWrapper — Python 友好的 librime 调用封装
# ──────────────────────────────────────────────
class RimeApiWrapper:
    """librime RimeApi 的 Python 封装。

    自动加载 DLL，通过 CFUNCTYPE 转换函数指针，
    处理 UTF-8 编码/解码。

    Args:
        dll_path: librime.dll 路径，None 则自动搜索
    """

    def __init__(self, dll_path: str | None = None):
        if dll_path is None:
            dll_path = find_dll()

        # 添加 DLL 目录到搜索路径（解决依赖 DLL 问题）
        dll_dir = str(Path(dll_path).parent)
        if hasattr(os, "add_dll_directory"):
            os.add_dll_directory(dll_dir)
        os.environ["PATH"] = dll_dir + os.pathsep + os.environ.get("PATH", "")

        self._dll = ctypes.CDLL(dll_path)

        # 获取 RimeApi 指针
        self._dll.rime_get_api.restype = c_void_p
        api_ptr = self._dll.rime_get_api()
        if not api_ptr:
            raise RuntimeError("rime_get_api() 返回 NULL")

        self._api = cast(api_ptr, POINTER(RimeApi)).contents

        # 防止 GC 回收通知回调
        self._notification_handler = None

    def _call(self, field, restype, argtypes, *args):
        """将 c_void_p 转换为 CFUNCTYPE 并调用。"""
        fn_type = CFUNCTYPE(restype, *argtypes)
        func = cast(field, fn_type)
        return func(*args)

    # ──────────────────────────────────────────
    # T5: 部署与维护
    # ──────────────────────────────────────────

    def setup(self, traits: RimeTraits):
        """设置引擎特征（路径等）。"""
        self._call(self._api.setup, None, [POINTER(RimeTraits)], byref(traits))

    def set_notification_handler(self, handler, context_object=None):
        """注册部署通知回调。"""
        self._notification_handler = handler
        self._call(self._api.set_notification_handler, None,
                   [RimeNotificationHandler, c_void_p],
                   handler, context_object)

    def initialize(self, traits: RimeTraits):
        """初始化引擎。"""
        self._call(self._api.initialize, None,
                   [POINTER(RimeTraits)], byref(traits))

    def finalize(self):
        """释放引擎资源。"""
        self._call(self._api.finalize, None, [])

    def start_maintenance(self, full_check: bool = True) -> bool:
        """启动部署维护（编译方案数据）。"""
        return bool(self._call(self._api.start_maintenance, Bool,
                               [Bool], int(full_check)))

    def is_maintenance_mode(self) -> bool:
        """查询是否正在维护中。"""
        return bool(self._call(self._api.is_maintenance_mode, Bool, []))

    def join_maintenance_thread(self):
        """等待维护线程结束。"""
        self._call(self._api.join_maintenance_thread, None, [])

    def deployer_initialize(self, traits: RimeTraits):
        """仅初始化部署器（不启动完整引擎）。"""
        self._call(self._api.deployer_initialize, None,
                   [POINTER(RimeTraits)], byref(traits))

    def prebuild(self) -> bool:
        """预构建。"""
        return bool(self._call(self._api.prebuild, Bool, []))

    def deploy(self) -> bool:
        """触发部署。"""
        return bool(self._call(self._api.deploy, Bool, []))

    def deploy_schema(self, schema_file: str) -> bool:
        """部署指定方案文件。"""
        return bool(self._call(self._api.deploy_schema, Bool,
                               [c_char_p], schema_file.encode("utf-8")))

    def deploy_config_file(self, file_name: str, version_key: str) -> bool:
        """部署配置文件。"""
        return bool(self._call(self._api.deploy_config_file, Bool,
                               [c_char_p, c_char_p],
                               file_name.encode("utf-8"),
                               version_key.encode("utf-8")))

    def sync_user_data(self) -> bool:
        """同步用户数据。"""
        return bool(self._call(self._api.sync_user_data, Bool, []))

    # ──────────────────────────────────────────
    # 会话管理
    # ──────────────────────────────────────────

    def create_session(self) -> int:
        """创建新会话。"""
        return self._call(self._api.create_session, RimeSessionId, [])

    def find_session(self, session_id: int) -> bool:
        """查找会话是否存在。"""
        return bool(self._call(self._api.find_session, Bool,
                               [RimeSessionId], session_id))

    def destroy_session(self, session_id: int) -> bool:
        """销毁会话。"""
        return bool(self._call(self._api.destroy_session, Bool,
                               [RimeSessionId], session_id))

    def cleanup_stale_sessions(self):
        """清理过期会话。"""
        self._call(self._api.cleanup_stale_sessions, None, [])

    def cleanup_all_sessions(self):
        """清理所有会话。"""
        self._call(self._api.cleanup_all_sessions, None, [])

    # ──────────────────────────────────────────
    # T1: 核心输入
    # ──────────────────────────────────────────

    def process_key(self, session_id: int, keycode: int, mask: int = 0) -> bool:
        """处理按键事件。keycode 为 X11 keysym 值。"""
        return bool(self._call(self._api.process_key, Bool,
                               [RimeSessionId, c_int, c_int],
                               session_id, keycode, mask))

    def commit_composition(self, session_id: int) -> bool:
        """提交当前组合文本。"""
        return bool(self._call(self._api.commit_composition, Bool,
                               [RimeSessionId], session_id))

    def clear_composition(self, session_id: int):
        """清空当前组合。"""
        self._call(self._api.clear_composition, None,
                   [RimeSessionId], session_id)

    def get_commit(self, session_id: int) -> str | None:
        """获取已提交的文本（UTF-8 解码）。"""
        commit = RimeCommit()
        rime_struct_init(commit)
        if self._call(self._api.get_commit, Bool,
                      [RimeSessionId, POINTER(RimeCommit)],
                      session_id, byref(commit)):
            text = self._decode(commit.text)
            self._call(self._api.free_commit, Bool,
                       [POINTER(RimeCommit)], byref(commit))
            return text
        return None

    def get_context(self, session_id: int) -> RimeContext | None:
        """获取输入上下文（组合 + 候选词）。

        注意：内部自动设置 data_size，调用者无需关心。
        """
        ctx = RimeContext()
        rime_struct_init(ctx)
        if self._call(self._api.get_context, Bool,
                      [RimeSessionId, POINTER(RimeContext)],
                      session_id, byref(ctx)):
            return ctx
        return None

    def free_context(self, ctx: RimeContext):
        """释放上下文资源。"""
        self._call(self._api.free_context, Bool,
                   [POINTER(RimeContext)], byref(ctx))

    def get_status(self, session_id: int) -> RimeStatus | None:
        """获取引擎状态。"""
        status = RimeStatus()
        rime_struct_init(status)
        if self._call(self._api.get_status, Bool,
                      [RimeSessionId, POINTER(RimeStatus)],
                      session_id, byref(status)):
            return status
        return None

    def free_status(self, status: RimeStatus):
        """释放状态资源。"""
        self._call(self._api.free_status, Bool,
                   [POINTER(RimeStatus)], byref(status))

    def get_input(self, session_id: int) -> str | None:
        """获取原始输入字符串。"""
        raw = self._call(self._api.get_input, c_char_p, [RimeSessionId],
                         session_id)
        return self._decode(raw)

    def get_caret_pos(self, session_id: int) -> int:
        """获取光标位置。"""
        return self._call(self._api.get_caret_pos, c_size_t,
                          [RimeSessionId], session_id)

    def set_caret_pos(self, session_id: int, pos: int):
        """设置光标位置。"""
        self._call(self._api.set_caret_pos, None,
                   [RimeSessionId, c_size_t], session_id, pos)

    def select_candidate(self, session_id: int, index: int) -> bool:
        """按全局索引选择候选词。"""
        return bool(self._call(self._api.select_candidate, Bool,
                               [RimeSessionId, c_size_t],
                               session_id, index))

    def select_candidate_on_current_page(self, session_id: int,
                                          index: int) -> bool:
        """按页内索引选择候选词。"""
        return bool(self._call(
            self._api.select_candidate_on_current_page, Bool,
            [RimeSessionId, c_size_t], session_id, index))

    def delete_candidate(self, session_id: int, index: int) -> bool:
        """按全局索引删除候选词。"""
        return bool(self._call(self._api.delete_candidate, Bool,
                               [RimeSessionId, c_size_t],
                               session_id, index))

    def delete_candidate_on_current_page(self, session_id: int,
                                          index: int) -> bool:
        """按页内索引删除候选词。"""
        return bool(self._call(
            self._api.delete_candidate_on_current_page, Bool,
            [RimeSessionId, c_size_t], session_id, index))

    def highlight_candidate(self, session_id: int, index: int) -> bool:
        """按全局索引高亮候选词。"""
        return bool(self._call(self._api.highlight_candidate, Bool,
                               [RimeSessionId, c_size_t],
                               session_id, index))

    def highlight_candidate_on_current_page(self, session_id: int,
                                             index: int) -> bool:
        """按页内索引高亮候选词。"""
        return bool(self._call(
            self._api.highlight_candidate_on_current_page, Bool,
            [RimeSessionId, c_size_t], session_id, index))

    def change_page(self, session_id: int, backward: bool = False) -> bool:
        """翻页。backward=True 上一页，False 下一页。"""
        return bool(self._call(self._api.change_page, Bool,
                               [RimeSessionId, Bool],
                               session_id, int(backward)))

    def simulate_key_sequence(self, session_id: int,
                               key_sequence: str) -> bool:
        """模拟按键序列（测试用）。"""
        return bool(self._call(self._api.simulate_key_sequence, Bool,
                               [RimeSessionId, c_char_p],
                               session_id, key_sequence.encode("utf-8")))

    def set_input(self, session_id: int, text: str) -> bool:
        """直接设置输入字符串。"""
        return bool(self._call(self._api.set_input, Bool,
                               [RimeSessionId, c_char_p],
                               session_id, text.encode("utf-8")))

    # ──────────────────────────────────────────
    # T3: 选项控制
    # ──────────────────────────────────────────

    def set_option(self, session_id: int, option: str, value: bool):
        """设置布尔选项（如 ascii_mode, zh_hans 等）。"""
        self._call(self._api.set_option, None,
                   [RimeSessionId, c_char_p, Bool],
                   session_id, option.encode("utf-8"), int(value))

    def get_option(self, session_id: int, option: str) -> bool:
        """获取布尔选项值。"""
        return bool(self._call(self._api.get_option, Bool,
                               [RimeSessionId, c_char_p],
                               session_id, option.encode("utf-8")))

    def set_property(self, session_id: int, key: str, value: str):
        """设置字符串属性。"""
        self._call(self._api.set_property, None,
                   [RimeSessionId, c_char_p, c_char_p],
                   session_id, key.encode("utf-8"), value.encode("utf-8"))

    def get_property(self, session_id: int, key: str) -> str | None:
        """获取字符串属性。"""
        buf = ctypes.create_string_buffer(1024)
        if self._call(self._api.get_property, Bool,
                      [RimeSessionId, c_char_p, c_char_p, c_size_t],
                      session_id, key.encode("utf-8"), buf, 1024):
            return self._decode(buf.value)
        return None

    def get_state_label(self, session_id: int, option_name: str,
                         state: bool) -> str | None:
        """获取选项状态的显示标签。"""
        raw = self._call(self._api.get_state_label, c_char_p,
                         [RimeSessionId, c_char_p, Bool],
                         session_id, option_name.encode("utf-8"), int(state))
        return self._decode(raw)

    # ──────────────────────────────────────────
    # T2: 方案管理
    # ──────────────────────────────────────────

    def select_schema(self, session_id: int, schema_id: str) -> bool:
        """切换输入方案。"""
        return bool(self._call(self._api.select_schema, Bool,
                               [RimeSessionId, c_char_p],
                               session_id, schema_id.encode("utf-8")))

    def get_current_schema(self, session_id: int) -> str | None:
        """获取当前方案 ID。"""
        buf = ctypes.create_string_buffer(256)
        if self._call(self._api.get_current_schema, Bool,
                      [RimeSessionId, c_char_p, c_size_t],
                      session_id, buf, 256):
            return self._decode(buf.value)
        return None

    def get_schema_list(self) -> list[dict]:
        """获取所有可用方案列表。"""
        schema_list = RimeSchemaList()
        result = []
        if self._call(self._api.get_schema_list, Bool,
                      [POINTER(RimeSchemaList)], byref(schema_list)):
            for i in range(schema_list.size):
                item = schema_list.list[i]
                result.append({
                    "schema_id": self._decode(item.schema_id),
                    "name": self._decode(item.name),
                })
            self._call(self._api.free_schema_list, None,
                       [POINTER(RimeSchemaList)], byref(schema_list))
        return result

    def schema_open(self, schema_id: str, config: RimeConfig) -> bool:
        """打开方案配置。"""
        return bool(self._call(self._api.schema_open, Bool,
                               [c_char_p, POINTER(RimeConfig)],
                               schema_id.encode("utf-8"), byref(config)))

    # ──────────────────────────────────────────
    # T4: 状态查询
    # ──────────────────────────────────────────

    def get_version(self) -> str | None:
        """获取 librime 版本号。"""
        return self._decode(self._call(self._api.get_version, c_char_p, []))

    # ──────────────────────────────────────────
    # T6: 配置读写
    # ──────────────────────────────────────────

    def config_open(self, config_id: str, config: RimeConfig) -> bool:
        """打开配置文件。"""
        return bool(self._call(self._api.config_open, Bool,
                               [c_char_p, POINTER(RimeConfig)],
                               config_id.encode("utf-8"), byref(config)))

    def config_close(self, config: RimeConfig) -> bool:
        """关闭配置文件。"""
        return bool(self._call(self._api.config_close, Bool,
                               [POINTER(RimeConfig)], byref(config)))

    def config_init(self, config: RimeConfig) -> bool:
        """初始化空配置。"""
        return bool(self._call(self._api.config_init, Bool,
                               [POINTER(RimeConfig)], byref(config)))

    def config_load_string(self, config: RimeConfig, yaml: str) -> bool:
        """从 YAML 字符串加载配置。"""
        return bool(self._call(self._api.config_load_string, Bool,
                               [POINTER(RimeConfig), c_char_p],
                               byref(config), yaml.encode("utf-8")))

    def config_get_bool(self, config: RimeConfig, key: str) -> bool | None:
        """读取布尔配置值。"""
        value = Bool()
        if self._call(self._api.config_get_bool, Bool,
                      [POINTER(RimeConfig), c_char_p, POINTER(Bool)],
                      byref(config), key.encode("utf-8"), byref(value)):
            return bool(value.value)
        return None

    def config_get_int(self, config: RimeConfig, key: str) -> int | None:
        """读取整数配置值。"""
        value = c_int()
        if self._call(self._api.config_get_int, Bool,
                      [POINTER(RimeConfig), c_char_p, POINTER(c_int)],
                      byref(config), key.encode("utf-8"), byref(value)):
            return value.value
        return None

    def config_get_double(self, config: RimeConfig, key: str) -> float | None:
        """读取浮点配置值。"""
        value = c_double()
        if self._call(self._api.config_get_double, Bool,
                      [POINTER(RimeConfig), c_char_p, POINTER(c_double)],
                      byref(config), key.encode("utf-8"), byref(value)):
            return value.value
        return None

    def config_get_string(self, config: RimeConfig,
                           key: str) -> str | None:
        """读取字符串配置值。"""
        buf = ctypes.create_string_buffer(1024)
        if self._call(self._api.config_get_string, Bool,
                      [POINTER(RimeConfig), c_char_p, c_char_p, c_size_t],
                      byref(config), key.encode("utf-8"), buf, 1024):
            return self._decode(buf.value)
        return None

    def config_set_bool(self, config: RimeConfig, key: str, value: bool) -> bool:
        """写入布尔配置值。"""
        return bool(self._call(self._api.config_set_bool, Bool,
                               [POINTER(RimeConfig), c_char_p, Bool],
                               byref(config), key.encode("utf-8"), int(value)))

    def config_set_int(self, config: RimeConfig, key: str, value: int) -> bool:
        """写入整数配置值。"""
        return bool(self._call(self._api.config_set_int, Bool,
                               [POINTER(RimeConfig), c_char_p, c_int],
                               byref(config), key.encode("utf-8"), value))

    def config_set_double(self, config: RimeConfig, key: str,
                           value: float) -> bool:
        """写入浮点配置值。"""
        return bool(self._call(self._api.config_set_double, Bool,
                               [POINTER(RimeConfig), c_char_p, c_double],
                               byref(config), key.encode("utf-8"), value))

    def config_set_string(self, config: RimeConfig, key: str,
                           value: str) -> bool:
        """写入字符串配置值。"""
        return bool(self._call(self._api.config_set_string, Bool,
                               [POINTER(RimeConfig), c_char_p, c_char_p],
                               byref(config), key.encode("utf-8"),
                               value.encode("utf-8")))

    def config_clear(self, config: RimeConfig, key: str) -> bool:
        """清除配置项。"""
        return bool(self._call(self._api.config_clear, Bool,
                               [POINTER(RimeConfig), c_char_p],
                               byref(config), key.encode("utf-8")))

    def config_create_list(self, config: RimeConfig, key: str) -> bool:
        """创建空列表配置项。"""
        return bool(self._call(self._api.config_create_list, Bool,
                               [POINTER(RimeConfig), c_char_p],
                               byref(config), key.encode("utf-8")))

    def config_create_map(self, config: RimeConfig, key: str) -> bool:
        """创建空映射配置项。"""
        return bool(self._call(self._api.config_create_map, Bool,
                               [POINTER(RimeConfig), c_char_p],
                               byref(config), key.encode("utf-8")))

    def config_list_size(self, config: RimeConfig, key: str) -> int:
        """获取列表配置项的大小。"""
        return self._call(self._api.config_list_size, c_size_t,
                          [POINTER(RimeConfig), c_char_p],
                          byref(config), key.encode("utf-8"))

    def config_update_signature(self, config: RimeConfig, signer: str) -> bool:
        """更新配置签名。"""
        return bool(self._call(self._api.config_update_signature, Bool,
                               [POINTER(RimeConfig), c_char_p],
                               byref(config), signer.encode("utf-8")))

    # ──────────────────────────────────────────
    # 目录访问
    # ──────────────────────────────────────────

    def get_shared_data_dir(self) -> str | None:
        """获取共享数据目录路径。"""
        return self._decode(
            self._call(self._api.get_shared_data_dir, c_char_p, []))

    def get_user_data_dir(self) -> str | None:
        """获取用户数据目录路径。"""
        return self._decode(
            self._call(self._api.get_user_data_dir, c_char_p, []))

    # ──────────────────────────────────────────
    # 内部方法
    # ──────────────────────────────────────────

    @staticmethod
    def _decode(raw_bytes: bytes | None) -> str | None:
        """解码 UTF-8 字节串，替换无效字符。"""
        if raw_bytes is None:
            return None
        if isinstance(raw_bytes, bytes):
            return raw_bytes.decode("utf-8", errors="replace")
        return str(raw_bytes)
