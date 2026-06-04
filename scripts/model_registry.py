"""
模型资源注册表 — 定义所有需要下载的模型文件元数据。

每个 ModelFile 记录：
- 本地路径、文件大小、SHA256 校验值
- HuggingFace 和 ModelScope 的仓库 ID 及仓库内文件路径
- 所属引擎、是否为目录、描述信息
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import hashlib
import logging

logger = logging.getLogger(__name__)


@dataclass
class ModelFile:
    local_path: str          # 相对于项目根目录的本地路径
    size: int                # 文件大小（字节），0 表示目录
    sha256: str              # SHA256 校验值（文件），空字符串表示目录
    hf_repo: Optional[str]   # HuggingFace 仓库 ID（None = HF 无此文件）
    hf_remote_path: Optional[str]  # 仓库内文件路径（None = HF 无此文件）
    ms_repo: str             # ModelScope 仓库 ID
    ms_remote_path: Optional[str] = None  # 仓库内文件路径（None = ModelScope 无此文件）
    github_url: Optional[str] = None  # GitHub 直接下载链接（备用源）
    engine: str = ""         # 所属引擎: silero_vad / matcha_tts / qwen3_asr / hy_mt15
    is_directory: bool = False  # 是否为目录（如 espeak-ng-data）
    description: str = ""    # 文件描述


# ============================================================
# 注册表：所有需要下载的模型资源文件
# SHA256 已从本地 models11/ 目录实际文件计算得出
# ============================================================

MODEL_REGISTRY: list[ModelFile] = [

    # --------------------------------------------------------
    # Silero VAD
    # --------------------------------------------------------
    ModelFile(
        local_path="models/silero_vad.onnx",
        size=2243022,
        sha256="a4a068cd6cf1ea8355b84327595838ca748ec29a25bc91fc82e6c299ccdc5808",
        hf_repo="onnx-community/silero-vad",
        hf_remote_path="onnx/model.onnx",
        ms_repo="onnx-community/silero-vad",
        ms_remote_path="onnx/model.onnx",
        engine="silero_vad",
        description="Silero VAD 语音活动检测模型",
    ),

    # --------------------------------------------------------
    # MatchaTTS — 声学模型
    # --------------------------------------------------------
    ModelFile(
        local_path="models/matcha-icefall-zh-en/model-steps-3.onnx",
        size=75717082,
        sha256="524286bf6cf11be74329ae1c682ac69e34d6860c2ea9fd1290319d561540b16a",
        hf_repo="csukuangfj/matcha-icefall-zh-en",
        hf_remote_path="model-steps-3.onnx",
        ms_repo="dengcunqin/matcha_tts_zh_en_20251010",
        ms_remote_path="model-steps-3.onnx",
        engine="matcha_tts",
        description="MatchaTTS 声学模型（中英双语）",
    ),
    ModelFile(
        local_path="models/vocos-16khz-univ.onnx",
        size=53882848,
        sha256="b599142a1fb8ff03de3e84ac35ff537c619e56f4267a6fe894851a42844acf9e",
        hf_repo=None,
        hf_remote_path=None,
        ms_repo="dengcunqin/matcha_tts_zh_en_20251010",
        ms_remote_path="vocos-16khz-univ.onnx",
        github_url="https://github.com/k2-fsa/sherpa-onnx/releases/download/vocoder-models/vocos-16khz-univ.onnx",
        engine="matcha_tts",
        description="MatchaTTS Vocos 声码器模型",
    ),
    ModelFile(
        local_path="models/matcha-icefall-zh-en/tokens.txt",
        size=21146,
        sha256="77fee8e5e5dd96b3547119e6159292c648e99e065c54c97777722e3ce710b9a4",
        hf_repo="csukuangfj/matcha-icefall-zh-en",
        hf_remote_path="tokens.txt",
        ms_repo="dengcunqin/matcha_tts_zh_en_20251010",
        ms_remote_path=None,  # ModelScope 无此文件
        engine="matcha_tts",
        description="MatchaTTS 词表文件",
    ),
    ModelFile(
        local_path="models/matcha-icefall-zh-en/lexicon.txt",
        size=1400278,
        sha256="599efdcdaff4df2a123ce988c2cb90abcd59b919ef609ce36eb587d68b7ca2c0",
        hf_repo="csukuangfj/matcha-icefall-zh-en",
        hf_remote_path="lexicon.txt",
        ms_repo="dengcunqin/matcha_tts_zh_en_20251010",
        ms_remote_path=None,
        engine="matcha_tts",
        description="MatchaTTS 词典文件",
    ),
    ModelFile(
        local_path="models/matcha-icefall-zh-en/date-zh.fst",
        size=59154,
        sha256="eb8aa079ae3cb81d8f4404992f39d61a0cb990947512b5b8d1e54d1f6980e718",
        hf_repo="csukuangfj/matcha-icefall-zh-en",
        hf_remote_path="date-zh.fst",
        ms_repo="dengcunqin/matcha_tts_zh_en_20251010",
        ms_remote_path=None,
        engine="matcha_tts",
        description="MatchaTTS 日期 FST 语法文件（中文）",
    ),
    ModelFile(
        local_path="models/matcha-icefall-zh-en/number-zh.fst",
        size=64482,
        sha256="743f402181fcfebf76cc2f0546b71fa26476e626fbe4e460fb7b4c3a7a8bd5bd",
        hf_repo="csukuangfj/matcha-icefall-zh-en",
        hf_remote_path="number-zh.fst",
        ms_repo="dengcunqin/matcha_tts_zh_en_20251010",
        ms_remote_path=None,
        engine="matcha_tts",
        description="MatchaTTS 数字 FST 语法文件（中文）",
    ),
    ModelFile(
        local_path="models/matcha-icefall-zh-en/phone-zh.fst",
        size=88630,
        sha256="1ac2b6fa56b1442320c4de7db08353bab8963a2b57f365eebcdd3a2d3562f8d7",
        hf_repo="csukuangfj/matcha-icefall-zh-en",
        hf_remote_path="phone-zh.fst",
        ms_repo="dengcunqin/matcha_tts_zh_en_20251010",
        ms_remote_path=None,
        engine="matcha_tts",
        description="MatchaTTS 音素 FST 语法文件（中文）",
    ),
    # espeak-ng-data 作为目录条目，下载时用 allow_patterns 批量获取
    ModelFile(
        local_path="models/matcha-icefall-zh-en/espeak-ng-data",
        size=0,  # 目录不校验大小
        sha256="",  # 目录不校验 SHA256
        hf_repo="csukuangfj/matcha-icefall-zh-en",
        hf_remote_path="espeak-ng-data",
        ms_repo="dengcunqin/matcha_tts_zh_en_20251010",
        ms_remote_path=None,  # ModelScope 无此目录
        engine="matcha_tts",
        is_directory=True,
        description="eSpeak NG 语音数据目录（含 355 个文件）",
    ),

    # --------------------------------------------------------
    # Qwen3 ASR — 语音识别
    # --------------------------------------------------------
    ModelFile(
        local_path="models/qwen3-asr-0.6B-int8/conv_frontend.onnx",
        size=44148281,
        sha256="d22dc4423e0940e49884e903d2ea2f7e5567c14fc1aed97e4e26d6b8f208ef9e",
        hf_repo="csukuangfj2/sherpa-onnx-qwen3-asr-0.6B-int8-2026-03-25",
        hf_remote_path="conv_frontend.onnx",
        ms_repo="zengshuishui/Qwen3-ASR-onnx",
        ms_remote_path="model_0.6B/conv_frontend.onnx",
        engine="qwen3_asr",
        description="Qwen3 ASR 卷积前端模型",
    ),
    ModelFile(
        local_path="models/qwen3-asr-0.6B-int8/encoder.int8.onnx",
        size=182491662,
        sha256="60748d3e6744a57c9c91e1b17424a6c2990567e8adceb0783940c03ed98fa9d9",
        hf_repo="csukuangfj2/sherpa-onnx-qwen3-asr-0.6B-int8-2026-03-25",
        hf_remote_path="encoder.int8.onnx",
        ms_repo="zengshuishui/Qwen3-ASR-onnx",
        ms_remote_path="model_0.6B/encoder.int8.onnx",
        engine="qwen3_asr",
        description="Qwen3 ASR 编码器模型（INT8 量化）",
    ),
    ModelFile(
        local_path="models/qwen3-asr-0.6B-int8/decoder.int8.onnx",
        size=755914231,
        sha256="4f6885be5959ae26af3089d38ee7972c5fafbeeb1cf8d5e76eab6d8b61ca5771",
        hf_repo="csukuangfj2/sherpa-onnx-qwen3-asr-0.6B-int8-2026-03-25",
        hf_remote_path="decoder.int8.onnx",
        ms_repo="zengshuishui/Qwen3-ASR-onnx",
        ms_remote_path="model_0.6B/decoder.int8.onnx",
        engine="qwen3_asr",
        description="Qwen3 ASR 解码器模型（INT8 量化）",
    ),
    ModelFile(
        local_path="models/qwen3-asr-0.6B-int8/tokenizer/merges.txt",
        size=1671853,
        sha256="8831e4f1a044471340f7c0a83d7bd71306a5b867e95fd870f74d0c5308a904d5",
        hf_repo="csukuangfj2/sherpa-onnx-qwen3-asr-0.6B-int8-2026-03-25",
        hf_remote_path="tokenizer/merges.txt",
        ms_repo="zengshuishui/Qwen3-ASR-onnx",
        ms_remote_path="tokenizer/merges.txt",
        engine="qwen3_asr",
        description="Qwen3 ASR tokenizer 合并规则",
    ),
    ModelFile(
        local_path="models/qwen3-asr-0.6B-int8/tokenizer/tokenizer_config.json",
        size=12487,
        sha256="4942d005604266809309cabc9f4e9cb89ce855d59b14681fdc0e1cc62ea26c4c",
        hf_repo="csukuangfj2/sherpa-onnx-qwen3-asr-0.6B-int8-2026-03-25",
        hf_remote_path="tokenizer/tokenizer_config.json",
        ms_repo="zengshuishui/Qwen3-ASR-onnx",
        ms_remote_path="tokenizer/tokenizer_config.json",
        engine="qwen3_asr",
        description="Qwen3 ASR tokenizer 配置",
    ),
    ModelFile(
        local_path="models/qwen3-asr-0.6B-int8/tokenizer/vocab.json",
        size=2776833,
        sha256="ca10d7e9fb3ed18575dd1e277a2579c16d108e32f27439684afa0e10b1440910",
        hf_repo="csukuangfj2/sherpa-onnx-qwen3-asr-0.6B-int8-2026-03-25",
        hf_remote_path="tokenizer/vocab.json",
        ms_repo="zengshuishui/Qwen3-ASR-onnx",
        ms_remote_path="tokenizer/vocab.json",
        engine="qwen3_asr",
        description="Qwen3 ASR tokenizer 词表",
    ),

    # --------------------------------------------------------
    # HY-MT2 — 翻译模型
    # --------------------------------------------------------
    ModelFile(
        local_path="models/HY-mt/Hy-MT2-1.8B-2Bit.gguf",
        size=600534880,
        sha256="dcc33bbae9b28d923c8c76a64f6157840841d26f8774f3dfd770d5fabeeb1cd7",
        hf_repo="tencent/Hy-MT2-1.8B-2Bit-GGUF",
        hf_remote_path="Hy-MT2-1.8B-2Bit.gguf",
        ms_repo="Tencent-Hunyuan/Hy-MT2-1.8B-2Bit-GGUF",
        ms_remote_path="Hy-MT2-1.8B-2Bit.gguf",
        engine="hy_mt15",
        description="HY-MT2 翻译模型（1.8B 参数，2Bit 量化）",
    ),
]


class ModelRegistry:
    """模型资源注册表管理器"""

    def __init__(self, project_root: Optional[str] = None):
        self.project_root = Path(project_root) if project_root else Path(__file__).parent.parent.resolve()

    def get_all(self) -> list[ModelFile]:
        """获取所有注册的模型文件"""
        return MODEL_REGISTRY

    def get_by_engine(self, engine: str) -> list[ModelFile]:
        """按引擎名称筛选模型文件"""
        return [f for f in MODEL_REGISTRY if f.engine == engine]

    def get_engines(self) -> list[str]:
        """获取所有引擎名称"""
        return list(dict.fromkeys(f.engine for f in MODEL_REGISTRY))

    def verify_file(self, mf: ModelFile, fast: bool = False) -> tuple[bool, str]:
        """
        校验单个模型文件。

        Args:
            mf: 模型文件条目
            fast: True 时只检查存在性和大小，跳过 SHA256

        Returns:
            (is_valid, message)
        """
        local = self.project_root / mf.local_path

        if mf.is_directory:
            if not local.exists() or not local.is_dir():
                return False, "目录不存在"
            file_count = sum(1 for _ in local.rglob("*") if _.is_file())
            if file_count == 0:
                return False, "目录为空"
            return True, f"目录存在，含 {file_count} 个文件"

        if not local.exists():
            return False, "文件不存在"

        actual_size = local.stat().st_size
        if actual_size != mf.size:
            return False, f"大小不匹配: 期望 {mf.size}, 实际 {actual_size}"

        if fast:
            return True, f"文件存在，大小正确 ({actual_size} bytes)"

        # SHA256 校验
        sha256 = hashlib.sha256()
        with open(local, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        actual_hash = sha256.hexdigest()
        if actual_hash != mf.sha256:
            return False, f"SHA256 不匹配: 期望 {mf.sha256[:16]}..., 实际 {actual_hash[:16]}..."

        return True, "校验通过"

    def get_missing(self, fast: bool = False) -> list[tuple[ModelFile, str]]:
        """
        获取所有缺失或损坏的模型文件。

        Returns:
            [(ModelFile, error_message), ...]
        """
        missing = []
        for mf in MODEL_REGISTRY:
            is_valid, msg = self.verify_file(mf, fast=fast)
            if not is_valid:
                missing.append((mf, msg))
        return missing

    def print_status(self, fast: bool = False):
        """打印所有模型文件的状态"""
        engines = self.get_engines()
        total_ok = 0
        total_fail = 0

        for engine in engines:
            files = self.get_by_engine(engine)
            print(f"\n{'='*60}")
            print(f"  Engine: {engine}")
            print(f"{'='*60}")

            for mf in files:
                is_valid, msg = self.verify_file(mf, fast=fast)
                status = "[OK]" if is_valid else "[!!]"
                name = Path(mf.local_path).name if not mf.is_directory else Path(mf.local_path).name + "/"
                print(f"  {status:6s} {name:40s} {msg}")
                if is_valid:
                    total_ok += 1
                else:
                    total_fail += 1

        print(f"\n{'='*60}")
        print(f"  Total: {total_ok} OK, {total_fail} missing/corrupted")
        print(f"{'='*60}")
        return total_fail == 0
