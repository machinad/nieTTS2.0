"""内部工具函数：资源路径查找。"""

from pathlib import Path


def get_lib_dir() -> Path:
    """获取 librime.dll 所在目录（包内 _lib/）。"""
    return Path(__file__).parent / "_lib"


def get_data_dir() -> Path:
    """获取 RIME 方案数据目录（包内 _data/）。"""
    return Path(__file__).parent / "_data"


def find_dll() -> str:
    """查找 librime.dll 的完整路径。

    搜索顺序：
    1. 包内 _lib/librime.dll
    2. 包所在目录的 lib/librime.dll

    Returns:
        librime.dll 的绝对路径

    Raises:
        FileNotFoundError: 找不到 DLL
    """
    candidates = [
        get_lib_dir() / "librime.dll",
        Path(__file__).parent.parent.parent / "lib" / "librime.dll",
    ]
    for p in candidates:
        if p.exists():
            return str(p.resolve())
    raise FileNotFoundError(
        "找不到 librime.dll，请确认包安装正确或手动指定 dll_path"
    )


def find_data_dir() -> str:
    """查找 RIME 方案数据目录。

    搜索顺序：
    1. 包内 _data/
    2. 包所在目录的 rime_data/

    Returns:
        数据目录的绝对路径

    Raises:
        FileNotFoundError: 找不到数据目录
    """
    candidates = [
        get_data_dir(),
        Path(__file__).parent.parent.parent / "rime_data",
    ]
    for p in candidates:
        if p.is_dir() and any(p.glob("*.yaml")):
            return str(p.resolve())
    raise FileNotFoundError(
        "找不到 RIME 方案数据目录，请确认包安装正确或手动指定 shared_data_dir"
    )
