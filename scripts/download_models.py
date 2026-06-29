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
import shutil
import socket
import sys
from pathlib import Path

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
    except TimeoutError, OSError:
        logger.info("HuggingFace 不可达，使用 ModelScope 源")
        return "modelscope"


# ============================================================
# 下载器
# ============================================================


class Downloader:
    """模型文件下载器"""

    def __init__(self, source: str, registry: ModelRegistry, force: bool = False, hf_endpoint: str | None = None):
        """
        Args:
            source: "huggingface", "huggingface_mirror" 或 "modelscope"
            registry: 模型注册表实例
            force: 是否强制重新下载已有文件
            hf_endpoint: HuggingFace 镜像地址，如 "https://hf-mirror.com"
        """
        self.source = source
        self.registry = registry
        self.force = force
        self._hf_endpoint = hf_endpoint or "https://hf-mirror.com"
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

    def _download_single_file_mirror(self, mf: ModelFile) -> bool:
        """从 HuggingFace 镜像直接下载单个文件（绕过 huggingface_hub 库）"""
        import httpx

        url = f"{self._hf_endpoint}/{mf.hf_repo}/resolve/main/{mf.hf_remote_path}"
        local = self.registry.project_root / mf.local_path
        local.parent.mkdir(parents=True, exist_ok=True)

        try:
            with httpx.stream("GET", url, follow_redirects=True, timeout=120) as r:
                r.raise_for_status()
                with open(local, "wb") as f:
                    for chunk in r.iter_bytes(chunk_size=8192):
                        f.write(chunk)
            logger.info("[OK] 已从镜像下载: %s", mf.local_path)
            return True
        except Exception as e:
            logger.error("[FAIL] 镜像下载失败 %s: %s", mf.local_path, e)
            return False

    def _download_directory_mirror(self, mf: ModelFile) -> bool:
        """从 HuggingFace 镜像批量下载目录"""
        import httpx

        local_dir = self.registry.project_root / mf.local_path

        try:
            # 通过 API 获取目录下的文件列表
            api_url = f"{self._hf_endpoint}/api/models/{mf.hf_repo}/tree/main/{mf.hf_remote_path}"
            r = httpx.get(api_url, follow_redirects=True, timeout=30)
            r.raise_for_status()
            files = r.json()
            file_names = [f["path"].split("/")[-1] for f in files if f.get("type") == "file"]

            if not file_names:
                logger.error("[FAIL] 镜像目录为空或不存在: %s", mf.hf_remote_path)
                return False

            local_dir.mkdir(parents=True, exist_ok=True)
            ok, fail = 0, 0
            for name in file_names:
                file_url = f"{self._hf_endpoint}/{mf.hf_repo}/resolve/main/{mf.hf_remote_path}/{name}"
                dest = local_dir / name
                try:
                    with httpx.stream("GET", file_url, follow_redirects=True, timeout=120) as resp:
                        resp.raise_for_status()
                        with open(dest, "wb") as f:
                            for chunk in resp.iter_bytes(chunk_size=8192):
                                f.write(chunk)
                    ok += 1
                except Exception as e:
                    logger.error("[FAIL] 镜像下载失败 %s/%s: %s", mf.hf_remote_path, name, e)
                    fail += 1

            if fail == 0:
                logger.info("[OK] 已从镜像下载目录: %s (%d 个文件)", mf.local_path, ok)
                return True
            else:
                logger.warning("[PARTIAL] 镜像目录下载部分失败: %s (%d 成功, %d 失败)", mf.local_path, ok, fail)
                return ok > 0
        except Exception as e:
            logger.error("[FAIL] 镜像目录下载失败 %s: %s", mf.local_path, e)
            return False

    def _download_from_github(self, mf: ModelFile) -> bool:
        """从 GitHub Release 直接下载文件"""
        import httpx

        if not mf.github_url:
            logger.error("[FAIL] 无 GitHub 下载链接: %s", mf.local_path)
            return False

        local = self.registry.project_root / mf.local_path
        local.parent.mkdir(parents=True, exist_ok=True)

        try:
            logger.info("从 GitHub 下载: %s", mf.github_url)
            with httpx.stream("GET", mf.github_url, follow_redirects=True, timeout=300) as r:
                r.raise_for_status()
                with open(local, "wb") as f:
                    for chunk in r.iter_bytes(chunk_size=8192):
                        f.write(chunk)
            logger.info("[OK] 已从 GitHub 下载: %s", mf.local_path)
            return True
        except Exception as e:
            logger.error("[FAIL] GitHub 下载失败 %s: %s", mf.local_path, e)
            return False

    def _extract_espeak_zip(self, mf: ModelFile) -> bool:
        """从仓库内的 espeak-ng-data.zip 解压，无需网络下载"""
        if not mf.is_directory:
            return False

        local_dir = self.registry.project_root / mf.local_path
        zip_path = local_dir.parent / "espeak-ng-data.zip"

        if not zip_path.exists():
            logger.warning("[SKIP] 未找到 %s，跳过本地解压", zip_path.name)
            return False

        import zipfile

        try:
            local_dir.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(local_dir)
            logger.info("[OK] 已从 %s 解压: %s", zip_path.name, mf.local_path)
            return True
        except Exception as e:
            logger.error("[FAIL] 解压失败 %s: %s", zip_path.name, e)
            return False

    def _extract_zip(self, mf: ModelFile) -> bool:
        """解压带 extract_to 标记的 zip 文件"""
        if not mf.extract_to:
            return False

        zip_path = self.registry.project_root / mf.local_path
        extract_dir = self.registry.project_root / mf.extract_to

        # 如果目标目录已存在且有文件，跳过
        if extract_dir.exists() and any(extract_dir.rglob("*")):
            return True

        if not zip_path.exists():
            logger.warning("[SKIP] 未找到 %s，跳过解压", mf.local_path)
            return False

        import zipfile

        try:
            extract_dir.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(extract_dir)
            file_count = sum(1 for _ in extract_dir.rglob("*") if _.is_file())
            logger.info("[OK] 已解压 %s → %s（%d 个文件）", mf.local_path, mf.extract_to, file_count)
            return True
        except Exception as e:
            logger.error("[FAIL] 解压失败 %s: %s", mf.local_path, e)
            return False

    def download_file(self, mf: ModelFile) -> bool:
        """
        下载单个模型文件。

        根据 source 选择不同的下载通道：
        - huggingface_mirror: 直接从镜像下载（绕过 huggingface_hub 库）
        - huggingface: 使用 huggingface_hub 库下载
        - modelscope: 使用 modelscope 库下载，缺失文件回退到 HuggingFace

        Returns:
            True 成功，False 失败
        """
        local = self.registry.project_root / mf.local_path

        # 带 extract_to 标记的条目：zip 已在 git 中，只需解压
        if mf.extract_to:
            is_valid, _ = self.registry.verify_file(mf, fast=True)
            if is_valid and not self.force:
                logger.info("[SKIP] 跳过（已解压）: %s", mf.extract_to)
                return True
            return self._extract_zip(mf)

        # 检查是否需要下载
        if not self.force and local.exists() and not mf.is_directory:
            is_valid, msg = self.registry.verify_file(mf, fast=True)
            if is_valid:
                logger.info("[SKIP] 跳过（已存在）: %s", mf.local_path)
                return True

        if mf.is_directory:
            # 优先从仓库内的 zip 解压
            if self._extract_espeak_zip(mf):
                return True
            if self.source == "huggingface_mirror":
                return self._download_directory_mirror(mf)
            elif self.source == "huggingface":
                return self._download_directory_hf(mf)
            else:
                # ModelScope 目录下载，缺失时回退到 HuggingFace 官方
                if mf.ms_remote_path is None:
                    logger.info("ModelScope 无 %s，从 HuggingFace 补充", mf.local_path)
                    return self._download_directory_hf(mf)
                return self._download_directory_ms(mf)
        else:
            if self.source == "huggingface_mirror":
                if mf.hf_remote_path is None:
                    return self._download_from_github(mf)
                return self._download_single_file_mirror(mf)
            elif self.source == "huggingface":
                if mf.hf_remote_path is None:
                    return self._download_from_github(mf)
                return self._download_single_file_hf(mf)
            else:
                # ModelScope 单文件下载
                if mf.ms_remote_path is None:
                    if mf.github_url:
                        return self._download_from_github(mf)
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


def get_model_status() -> list[dict]:
    """获取所有引擎的模型文件状态，供 API 使用"""
    registry = ModelRegistry()
    engines = registry.get_engines()
    result = []
    for engine in engines:
        files = registry.get_by_engine(engine)
        total = len(files)
        ok = sum(1 for mf in files if registry.verify_file(mf, fast=True)[0])
        result.append({"engine": engine, "total": total, "ok": ok})
    return result


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
    dl_parser.add_argument(
        "--source", choices=["huggingface", "huggingface_mirror", "modelscope"], help="强制使用指定下载源"
    )
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
