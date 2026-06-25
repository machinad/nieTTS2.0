import logging
from dataclasses import asdict

from rime import RimeEngine, InputResult

logger = logging.getLogger(__name__)


class RimeService:
    """Rime 输入法服务，懒加载引擎。

    注意：librime 的 ctypes 绑定不是线程安全的，
    所有操作必须在主线程执行（qasync 环境下不会阻塞 Qt 事件循环）。
    """

    def __init__(self):
        self._engine: RimeEngine | None = None

    def _ensure_engine(self) -> RimeEngine:
        if self._engine is None:
            logger.info("正在初始化 Rime 引擎...")
            self._engine = RimeEngine(
                user_data_dir="./rime_user_data",
                schema_id="luna_pinyin",
            )
            self._engine.deploy(timeout=60.0)
            logger.info("Rime 引擎初始化完成")
        return self._engine

    def process_key(self, keycode: int, mask: int = 0) -> dict:
        engine = self._ensure_engine()
        result = engine.process_key(keycode, mask)
        return self._to_dict(result)

    def select_candidate(self, index: int) -> dict:
        engine = self._ensure_engine()
        result = engine.select_candidate_on_page(index)
        return self._to_dict(result)

    def change_page(self, backward: bool = False) -> dict:
        engine = self._ensure_engine()
        result = engine.change_page(backward)
        return self._to_dict(result)

    def toggle_ascii_mode(self) -> dict:
        engine = self._ensure_engine()
        engine.toggle_ascii_mode()
        status = engine.get_status()
        return {"is_ascii_mode": status.is_ascii_mode}

    def clear(self):
        engine = self._ensure_engine()
        engine.clear()

    def get_status(self) -> dict:
        engine = self._ensure_engine()
        status = engine.get_status()
        return asdict(status)

    def shutdown(self):
        if self._engine:
            self._engine.shutdown()
            self._engine = None
            logger.info("Rime 引擎已关闭")

    @staticmethod
    def _to_dict(result: InputResult) -> dict:
        return {
            "committed": result.committed,
            "preedit": result.preedit,
            "candidates": result.candidates,
            "page_no": result.page_no,
            "is_last_page": result.is_last_page,
            "highlighted": result.highlighted,
        }
