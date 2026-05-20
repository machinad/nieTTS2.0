import logging
from pathlib import Path
import sherpa_onnx
from engines.tts.base import BaseTTS, TTSResult

logger = logging.getLogger(__name__)


class MatchaTTS(BaseTTS):
    engine_name = "MatchaTTS"

    def __init__(self, save_dir: Path, acoustic_model: str = "",
                 vocoder: str = "", tokens_path: str = "", lexicon_path: str = "",
                 data_dir: str = "", dict_dir: str = ""):
        super().__init__(save_dir)
        self.acoustic_model = acoustic_model
        self.vocoder = vocoder
        self.tokens_path = tokens_path
        self.lexicon_path = lexicon_path
        self.data_dir = data_dir
        self.dict_dir = dict_dir
        self._tts = None

    def is_available(self) -> bool:
        am = Path(self.acoustic_model) if self.acoustic_model else None
        vc = Path(self.vocoder) if self.vocoder else None
        tk = Path(self.tokens_path) if self.tokens_path else None
        return (am is not None and vc is not None and tk is not None
                and am.exists() and vc.exists() and tk.exists())

    def _lazy_init(self):
        if self._tts is not None:
            return
        matcha_config = sherpa_onnx.OfflineTtsMatchaModelConfig(
            acoustic_model=self.acoustic_model,
            vocoder=self.vocoder,
            lexicon=self.lexicon_path,
            tokens=self.tokens_path,
            data_dir=self.data_dir,
            dict_dir=self.dict_dir,
        )
        model_config = sherpa_onnx.OfflineTtsModelConfig(
            matcha=matcha_config,
            num_threads=4,
            provider="cpu",
        )
        config = sherpa_onnx.OfflineTtsConfig(model=model_config)
        self._tts = sherpa_onnx.OfflineTts(config)
        logger.info(f"MatchaTTS 初始化完成，samplerate={self._tts.sample_rate}")

    async def synthesize(self, text: str, voice: str = "", **kwargs) -> TTSResult:
        if not self.is_available():
            return TTSResult(
                success=False, text=text,
                error="MatchaTTS 模型文件不存在，请先下载模型",
            )
        try:
            self._lazy_init()
            sid = int(voice) if voice else 0
            if self._tts.num_speakers > 0 and sid >= self._tts.num_speakers:
                sid = 0
            speed = kwargs.get("speed", 1.0)
            num_steps = kwargs.get("num_steps", 0)

            if num_steps > 0:
                gc = sherpa_onnx.GenerationConfig()
                gc.speed = speed
                gc.sid = sid
                gc.num_steps = num_steps
                audio = self._tts.generate(text, config=gc)
            else:
                audio = self._tts.generate(text, sid=sid, speed=speed)

            save_path = self._make_path(".wav")
            sherpa_onnx.write_wave(str(save_path), audio.samples, audio.sample_rate)
            logger.info(f"MatchaTTS 生成成功: {save_path} ({len(audio.samples)} samples)")
            return TTSResult(success=True, path=save_path, voice=str(sid), text=text)
        except Exception as e:
            logger.error(f"MatchaTTS 生成失败: {e}")
            return TTSResult(success=False, text=text, error=str(e))
