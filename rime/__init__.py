"""
rime-python — librime 的 Python 绑定。

通过 ctypes 调用 librime.dll，提供中文输入法引擎功能。

快速开始：
    from rime import RimeEngine

    engine = RimeEngine(user_data_dir="./rime_user_data")
    engine.deploy()

    result = engine.process_key(ord('z'))
    print(result.candidates)

    result = engine.select_candidate_on_page(0)
    print(result.committed)

    engine.shutdown()
"""

from rime.binding import RimeApiWrapper
from rime.engine import InputResult, RimeEngine, StatusInfo

__version__ = "0.1.0"
__all__ = [
    "RimeEngine",
    "InputResult",
    "StatusInfo",
    "RimeApiWrapper",
]
