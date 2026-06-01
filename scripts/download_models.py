#!/usr/bin/env python3
"""
模型资源下载脚本 — 校验、下载缺失的模型文件。

支持 HuggingFace 和 ModelScope 双源下载，自动检测网络环境。
ModelScope 缺失的文件会自动从 HuggingFace 补充。

用法:
    python scripts/download_models.py check                          # 检查所有模型状态
    python scripts/download_models.py check --fast                   # 只检查存在性和大小
    python scripts/download_models.py check --engine matcha_tts      # 检查特定引擎
    python scripts/download_models.py download                       # 下载所有缺失模型
    python scripts/download_models.py download --source huggingface  # 强制用 HuggingFace
    python scripts/download_models.py download --source modelscope   # 强制用 ModelScope
    python scripts/download_models.py download --engine qwen3_asr    # 只下载特定引擎
    python scripts/download_models.py download --force               # 强制重新下载
"""

import argparse
import logging
import os
import shutil
import socket
import sys
import tempfile
import time
from pathlib import Path
from typing import Optional

# 将项目根目录加入 sys.path
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.model_registry import ModelFile, ModelRegistry

logger = logging.getLogger("download_models")

# ============================================================
# 网络检测
# ============================================================

_HF_HOST = "huggingface.co"
_HF_PORT = 443
_HF_TIMEOUT = 3  # 秒


def detect_source() -> str:
    """
    检测网络环境，返回推荐的下载源。

    尝试 TCP 连接 huggingface.co:443，成功则返回 "huggingface"，
    失败则返回 "modelscope"。

    Returns:
        "huggingface" 或 "modelscope"
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(_HF_TIMEOUT)
        sock.connect((_HF_HOST, _HF_PORT))
        sock.close()
        logger.info("检测到 HuggingFace 网络可达，使用 HuggingFace 源")
        return "huggingface"
    except (socket.timeout, OSError):
        logger.info("HuggingFace 不可达，使用 ModelScope 源")
        return "modelscope"


# ============================================================
# 下载器
# ============================================================

class Downloader:
    """模型文件下载器"""

    def __init__(self, source: str, registry: ModelRegistry, force: bool = False):
        """
        Args:
            source: "huggingface" 或 "modelscope"
            registry: 模型注册表实例
            force: 是否强制重新下载已有文件
        """
        self.source = source
        self.registry = registry
        self.force = force
        self._hf_available = False
        self._ms_available = False
        self._check_libraries()

    def _check_libraries(self):
        """检查下载库是否可用"""
        try:
            import huggingface_hub  # noqa: F401
            self._hf_available = True
        except ImportError:
            logger.warning("huggingface_hub 未安装，HuggingFace 源不可用。请运行: pip install huggingface_hub")

        try:
            import modelscope  # noqa: F401
            self._ms_available = True
        except ImportError:
            logger.warning("modelscope 未安装，ModelScope 源不可用。请运行: pip install modelscope")

    def _download_single_file_hf(self, mf: ModelFile) -> bool:
        """从 HuggingFace 下载单个文件"""
        if not self._hf_available:
            logger.error("huggingface_hub 未安装，无法从 HuggingFace 下载")
            return False

        from huggingface_hub import hf_hub_download

        local = self.registry.project_root / mf.local_path
        local.parent.mkdir(parents=True, exist_ok=True)

        try:
            # hf_hub_download 下载到缓存，我们再复制到目标路径
            cached = hf_hub_download(
                repo_id=mf.hf_repo,
                filename=mf.hf_remote_path,
                local_dir=str(local.parent),
                local_dir_use_symlinks=False,
            )
            # hf_hub_download 会把文件下载到 local_dir/repo_subpath
            # 需要移动到正确的位置
            cached_path = Path(cached)
            if cached_path.resolve() != local.resolve():
                # 文件不在目标位置，移动过去（支持跨驱动器）
                if local.exists():
                    local.unlink()
                shutil.move(str(cached_path), str(local))
            logger.info("[OK] 已从 HuggingFace 下载: %s", mf.local_path)
            return True
        except Exception as e:
            logger.error("[FAIL] HuggingFace 下载失败 %s: %s", mf.local_path, e)
            return False

    def _download_single_file_ms(self, mf: ModelFile) -> bool:
        """从 ModelScope 下载单个文件"""
        if not self._ms_available:
            logger.error("modelscope 未安装，无法从 ModelScope 下载")
            return False

        from modelscope import snapshot_download

        if mf.ms_remote_path is None:
            logger.warning("ModelScope 无此文件: %s，需从 HuggingFace 补充", mf.local_path)
            return False

        local = self.registry.project_root / mf.local_path
        local.parent.mkdir(parents=True, exist_ok=True)

        try:
            # snapshot_download 下载到缓存目录
            # 用 allow_patterns 只下载需要的文件
            pattern = mf.ms_remote_path
            downloaded_dir = snapshot_download(
                model_id=mf.ms_repo,
                allow_patterns=[pattern],
            )
            # 找到下载的文件并移动到目标位置
            downloaded_file = Path(downloaded_dir) / mf.ms_remote_path
            if downloaded_file.exists():
                if local.exists():
                    local.unlink()
                shutil.move(str(downloaded_file), str(local))
                logger.info("[OK] 已从 ModelScope 下载: %s", mf.local_path)
                return True
            else:
                logger.error("[FAIL] ModelScope 下载后未找到文件: %s", downloaded_file)
                return False
        except Exception as e:
            logger.error("[FAIL] ModelScope 下载失败 %s: %s", mf.local_path, e)
            return False

    def _download_directory_hf(self, mf: ModelFile) -> bool:
        """从 HuggingFace 批量下载目录"""
        if not self._hf_available:
            logger.error("huggingface_hub 未安装")
            return False

        from huggingface_hub import snapshot_download

        local_dir = self.registry.project_root / mf.local_path
        local_dir.parent.mkdir(parents=True, exist_ok=True)

        try:
            # snapshot_download 下载整个仓库的匹配文件到 local_dir
            # 仓库中的文件在根目录，目标是 local_dir
            # 需要将仓库文件映射到 local_dir 子目录
            pattern = f"{mf.hf_remote_path}/*"
            downloaded = snapshot_download(
                repo_id=mf.hf_repo,
                allow_patterns=[pattern],
                local_dir=str(self.registry.project_root / "models" / "_hf_tmp"),
            )
            # 移动文件到目标位置
            src_dir = Path(downloaded) / mf.hf_remote_path
            if src_dir.exists():
                if local_dir.exists():
                    shutil.rmtree(local_dir)
                shutil.move(str(src_dir), str(local_dir))
                # 清理临时目录
                tmp_root = Path(downloaded).parent.parent
                tmp_hf = self.registry.project_root / "models" / "_hf_tmp"
                if tmp_hf.exists():
                    shutil.rmtree(tmp_hf)
            logger.info("[OK] 已从 HuggingFace 下载目录: %s", mf.local_path)
            return True
        except Exception as e:
            logger.error("[FAIL] HuggingFace 目录下载失败 %s: %s", mf.local_path, e)
            return False

    def _download_directory_ms(self, mf: ModelFile) -> bool:
        """从 ModelScope 批量下载目录"""
        if not self._ms_available:
            logger.error("modelscope 未安装")
            return False

        if mf.ms_remote_path is None:
            logger.warning("ModelScope 无此目录: %s", mf.local_path)
            return False

        from modelscope import snapshot_download

        local_dir = self.registry.project_root / mf.local_path

        try:
            pattern = f"{mf.ms_remote_path}/*"
            downloaded = snapshot_download(
                model_id=mf.ms_repo,
                allow_patterns=[pattern],
            )
            src_dir = Path(downloaded) / mf.ms_remote_path
            if src_dir.exists():
                if local_dir.exists():
                    shutil.rmtree(local_dir)
                shutil.move(str(src_dir), str(local_dir))
                logger.info("[OK] 已从 ModelScope 下载目录: %s", mf.local_path)
                return True
            else:
                logger.error("[FAIL] ModelScope 下载后未找到目录: %s", src_dir)
                return False
        except Exception as e:
            logger.error("[FAIL] ModelScope 目录下载失败 %s: %s", mf.local_path, e)
            return False

    def download_file(self, mf: ModelFile) -> bool:
        """
        下载单个模型文件。

        如果当前源不可用（ModelScope 缺失文件），自动回退到 HuggingFace。

        Returns:
            True 成功，False 失败
        """
        local = self.registry.project_root / mf.local_path

        # 检查是否需要下载
        if not self.force and local.exists() and not mf.is_directory:
            is_valid, msg = self.registry.verify_file(mf, fast=True)
            if is_valid:
                logger.info("[SKIP] 跳过（已存在）: %s", mf.local_path)
                return True

        if mf.is_directory:
            if self.source == "huggingface":
                return self._download_directory_hf(mf)
            else:
                # ModelScope 目录下载，缺失时回退到 HuggingFace
                if mf.ms_remote_path is None:
                    logger.info("ModelScope 无 %s，从 HuggingFace 补充", mf.local_path)
                    return self._download_directory_hf(mf)
                return self._download_directory_ms(mf)
        else:
            if self.source == "huggingface":
                return self._download_single_file_hf(mf)
            else:
                # ModelScope 单文件下载，缺失时回退到 HuggingFace
                if mf.ms_remote_path is None:
                    logger.info("ModelScope 无 %s，从 HuggingFace 补充", mf.local_path)
                    return self._download_single_file_hf(mf)
                return self._download_single_file_ms(mf)

    def download_engine(self, engine: str) -> tuple[int, int]:
        """
        下载指定引擎的所有模型文件。

        Returns:
            (成功数, 失败数)
        """
        files = self.registry.get_by_engine(engine)
        if not files:
            logger.warning("未找到引擎: %s", engine)
            return 0, 0

        ok, fail = 0, 0
        for mf in files:
            if self.download_file(mf):
                ok += 1
            else:
                fail += 1
        return ok, fail

    def download_all(self) -> tuple[int, int]:
        """
        下载所有缺失的模型文件。

        Returns:
            (成功数, 失败数)
        """
        engines = self.registry.get_engines()
        total_ok, total_fail = 0, 0
        for engine in engines:
            logger.info("\n开始下载引擎: %s", engine)
            ok, fail = self.download_engine(engine)
            total_ok += ok
            total_fail += fail
        return total_ok, total_fail


# ============================================================
# CLI
# ============================================================

def cmd_check(args):
    """check 子命令"""
    registry = ModelRegistry()
    if args.engine:
        files = registry.get_by_engine(args.engine)
        if not files:
            print(f"未找到引擎: {args.engine}")
            print(f"可用引擎: {', '.join(registry.get_engines())}")
            return 1
        for mf in files:
            is_valid, msg = registry.verify_file(mf, fast=args.fast)
            status = "[OK]" if is_valid else "[!!]"
            print(f"  {status} {mf.local_path:50s} {msg}")
        return 0

    all_ok = registry.print_status(fast=args.fast)
    return 0 if all_ok else 1


def cmd_download(args):
    """download 子命令"""
    # 检测下载源
    if args.source:
        source = args.source
    else:
        source = detect_source()

    print(f"使用下载源: {source}")

    registry = ModelRegistry()
    downloader = Downloader(source=source, registry=registry, force=args.force)

    if args.engine:
        files = registry.get_by_engine(args.engine)
        if not files:
            print(f"未找到引擎: {args.engine}")
            print(f"可用引擎: {', '.join(registry.get_engines())}")
            return 1

        # 先检查哪些需要下载
        to_download = []
        for mf in files:
            if args.force:
                to_download.append(mf)
            else:
                is_valid, msg = registry.verify_file(mf, fast=True)
                if not is_valid:
                    to_download.append(mf)

        if not to_download:
            print(f"引擎 {args.engine} 的所有模型文件已就绪")
            return 0

        print(f"需要下载 {len(to_download)} 个文件:")
        for mf in to_download:
            size_mb = mf.size / (1024 * 1024) if mf.size > 0 else 0
            print(f"  - {mf.local_path} ({size_mb:.1f} MB)")

        ok, fail = downloader.download_engine(args.engine)
    else:
        # 先检查哪些需要下载
        missing = registry.get_missing()
        if not missing:
            print("所有模型文件已就绪，无需下载")
            return 0

        print(f"需要下载 {len(missing)} 个文件/目录:")
        for mf, msg in missing:
            size_mb = mf.size / (1024 * 1024) if mf.size > 0 else 0
            print(f"  - {mf.local_path} ({size_mb:.1f} MB) — {msg}")

        ok, fail = downloader.download_all()

    print(f"\n下载完成: {ok} 成功, {fail} 失败")
    return 0 if fail == 0 else 1


def main():
    parser = argparse.ArgumentParser(
        description="nieTTS 2.0 模型资源下载工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/download_models.py check                     检查所有模型状态
  python scripts/download_models.py check --fast              快速检查（跳过 SHA256）
  python scripts/download_models.py check --engine matcha_tts 检查特定引擎
  python scripts/download_models.py download                  下载所有缺失模型
  python scripts/download_models.py download --source modelscope  强制用 ModelScope
  python scripts/download_models.py download --engine qwen3_asr   只下载 Qwen3 ASR
  python scripts/download_models.py download --force          强制重新下载
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # check 子命令
    check_parser = subparsers.add_parser("check", help="检查模型文件状态")
    check_parser.add_argument("--fast", action="store_true", help="快速模式：只检查存在性和大小，跳过 SHA256")
    check_parser.add_argument("--engine", type=str, help="只检查指定引擎 (silero_vad/matcha_tts/qwen3_asr/hy_mt15)")

    # download 子命令
    dl_parser = subparsers.add_parser("download", help="下载缺失的模型文件")
    dl_parser.add_argument("--source", choices=["huggingface", "modelscope"], help="强制使用指定下载源")
    dl_parser.add_argument("--engine", type=str, help="只下载指定引擎的模型")
    dl_parser.add_argument("--force", action="store_true", help="强制重新下载（忽略已有文件）")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # 设置日志
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
    )

    if args.command == "check":
        return cmd_check(args)
    elif args.command == "download":
        return cmd_download(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
