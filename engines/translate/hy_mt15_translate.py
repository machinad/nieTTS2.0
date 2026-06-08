import asyncio
import logging
import re
import subprocess
from pathlib import Path

import httpx

from engines.translate.base import BaseTranslate, TranslateResult

logger = logging.getLogger(__name__)


_ZH_TO_EN = {
    "中文": "Chinese", "英语": "English", "日语": "Japanese",
    "韩语": "Korean", "法语": "French", "德语": "German",
    "西班牙语": "Spanish", "俄语": "Russian",
}


class HyMT15Translate(BaseTranslate):
    engine_name = "HY-MT1.5"

    @classmethod
    def from_config(cls, cfg: dict):
        return cls(
            model_path=cfg.get("model_path", "models/HY-mt/Hy-MT2-1.8B-2Bit.gguf"),
            server_url=cfg.get("server_url", "http://127.0.0.1:8081"),
            llama_cpp_path=cfg.get("llama_cpp_path", "llama-cpp"),
        )

    def __init__(self, model_path: str, server_url: str, llama_cpp_path: str):
        self.model_path = Path(model_path)
        self.server_url = server_url.rstrip("/")
        self.llama_cpp_path = Path(llama_cpp_path)
        self._process: subprocess.Popen | None = None

    def is_available(self) -> bool:
        return self.model_path.exists()

    def _build_prompt(self, text: str, source_lang: str, target_lang: str) -> str:
        is_zh = source_lang == "中文"
        if is_zh:
            return (
                f"将以下文本翻译为{target_lang}，"
                f"注意只需要输出翻译后的结果，不要额外解释：\n\n"
                f"{text}"
            )
        en_name = _ZH_TO_EN.get(target_lang, target_lang)
        return (
            f"Translate the following text into {en_name}. "
            f"Note that you should only output the translated result "
            f"without any additional explanation:\n\n"
            f"{text}"
        )

    def _start_server(self):
        self._stop_server()
        server_exe = self.llama_cpp_path / "llama-server.exe"
        cmd = [
            str(server_exe),
            "-m", str(self.model_path),
            "--host", "127.0.0.1",
            "--port", "8081",
            "-ngl", "99",
            "-c", "4096",
            "--no-warmup",
        ]
        self._process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        logger.info("llama-server 已启动 (PID: %s)", self._process.pid)

    def _stop_server(self):
        proc = self._process
        if proc is not None:
            try:
                proc.kill()
                proc.wait(timeout=5)
            except Exception:
                pass
            self._process = None

    async def close(self):
        """释放 llama-server 子进程资源"""
        self._stop_server()

    async def _wait_ready(self, timeout: int = 15) -> bool:
        async with httpx.AsyncClient(timeout=3) as client:
            for _ in range(int(timeout / 0.5)):
                await asyncio.sleep(0.5)
                try:
                    r = await client.get(f"{self.server_url}/health")
                    if r.status_code == 200:
                        return True
                except Exception:
                    continue
        return False

    async def translate(self, text: str, source_lang: str, target_lang: str, **kwargs) -> TranslateResult:
        try:
            if self._process is None or self._process.poll() is not None:
                await asyncio.to_thread(self._start_server)
                if not await self._wait_ready():
                    return TranslateResult(
                        success=False,
                        source_lang=source_lang,
                        target_lang=target_lang,
                        error="llama-server 启动超时",
                    )

            prompt = self._build_prompt(text, source_lang, target_lang)
            payload = {
                "messages": [
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.7,
                "top_k": 20,
                "top_p": 0.6,
                "repeat_penalty": 1.05,
            }

            async with httpx.AsyncClient(timeout=120) as client:
                resp = await client.post(
                    f"{self.server_url}/v1/chat/completions",
                    json=payload,
                )
                resp.raise_for_status()
                result = resp.json()
                translated = result["choices"][0]["message"]["content"]
                translated = re.sub(r'<[^>]+>', '', translated).strip()

            logger.info("HY-MT1.5 翻译成功: %s -> %s.译文: %s", source_lang, target_lang, translated)
            return TranslateResult(
                success=True,
                text=translated,
                source_lang=source_lang,
                target_lang=target_lang,
            )
        except Exception as e:
            logger.error("HY-MT1.5 翻译失败: %s", e)
            return TranslateResult(
                success=False,
                source_lang=source_lang,
                target_lang=target_lang,
                error=str(e),
            )
