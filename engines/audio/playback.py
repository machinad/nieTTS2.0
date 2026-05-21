import asyncio
import threading
import logging
from pathlib import Path
from typing import Optional

import miniaudio

logger = logging.getLogger(__name__)

_SUPPORTED_SUFFIXES = frozenset({".wav", ".mp3", ".ogg", ".flac", ".opus"})


def _find_device_id(device_name: str) -> Optional[int]:
    devices = miniaudio.Devices()
    for pb in devices.get_playbacks():
        if pb["name"] == device_name:
            return pb["id"]
    return None


def get_playback_devices() -> list[dict]:
    devices = miniaudio.Devices()
    return devices.get_playbacks()


def _play_file_sync(path: Path, device_id=None) -> None:
    finished = threading.Event()

    stream = miniaudio.stream_file(str(path))
    device = miniaudio.PlaybackDevice(device_id=device_id)
    device.stop_callback = finished.set
    device.start(stream)
    finished.wait()
    device.close()


async def play_file(path: Path, device_name: str = "") -> None:
    if not path.exists():
        logger.error(f"音频文件不存在: {path}")
        return
    suffix = path.suffix.lower()
    if suffix not in _SUPPORTED_SUFFIXES:
        logger.warning(f"不支持的音频格式: {suffix}")

    device_id = None
    if device_name:
        device_id = _find_device_id(device_name)
        if device_id is None:
            logger.warning(f"未找到播放设备 '{device_name}'，使用默认设备")

    logger.info(f"开始播放: {path.name}")
    await asyncio.to_thread(_play_file_sync, path, device_id)
    logger.info(f"播放完成: {path.name}")
