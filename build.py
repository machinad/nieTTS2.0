#!/usr/bin/env python3
"""
nieTTS 2.0 打包脚本 — 使用 PyInstaller 构建 Windows 可执行文件。

用法:
    python build.py              # 完整打包（跳过前端构建）
    python build.py --frontend   # 先构建前端，再打包
    python build.py --clean      # 清理构建目录后重新打包
"""

import argparse
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
BUILD_DIR = os.path.join(ROOT, "build")
DIST_DIR = os.path.join(ROOT, "dist")
SPEC_FILE = os.path.join(ROOT, "nietts.spec")
FRONTEND_DIR = os.path.join(ROOT, "frontend")


def clean():
    """清理构建产物"""
    for d in [BUILD_DIR, DIST_DIR]:
        if os.path.exists(d):
            print(f"  清理 {d}")
            shutil.rmtree(d)
    print("  清理完成")


def build_frontend():
    """构建前端 SPA"""
    if not os.path.exists(os.path.join(FRONTEND_DIR, "node_modules")):
        print("  安装前端依赖...")
        subprocess.check_call(["npm.cmd", "install"], cwd=FRONTEND_DIR)

    print("  构建前端...")
    subprocess.check_call(["npm.cmd", "run", "build"], cwd=FRONTEND_DIR)
    print("  前端构建完成")


def build_app():
    """运行 PyInstaller 打包"""
    print("  运行 PyInstaller...")
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        SPEC_FILE,
        "--distpath",
        DIST_DIR,
        "--workpath",
        BUILD_DIR,
        "--noconfirm",
        "--clean",
    ]
    subprocess.check_call(cmd, cwd=ROOT)

    out_dir = os.path.join(DIST_DIR, "nieTTS")
    if os.path.exists(out_dir):
        exe_path = os.path.join(out_dir, "nieTTS.exe")
        size_mb = 0
        for dirpath, _, filenames in os.walk(out_dir):
            for f in filenames:
                size_mb += os.path.getsize(os.path.join(dirpath, f))
        size_mb /= 1024 * 1024
        print("\n  打包完成!")
        print(f"  输出目录: {out_dir}")
        print(f"  可执行文件: {exe_path}")
        print(f"  总大小: {size_mb:.1f} MB")
    else:
        print("  错误: 打包输出目录不存在")
        return 1

    return 0


def main():
    parser = argparse.ArgumentParser(description="nieTTS 2.0 打包脚本")
    parser.add_argument("--frontend", action="store_true", help="打包前先构建前端")
    parser.add_argument("--clean", action="store_true", help="清理构建目录后重新打包")
    args = parser.parse_args()

    print("=" * 50)
    print("  nieTTS 2.0 打包工具")
    print("=" * 50)

    if args.clean:
        print("\n[1/3] 清理构建目录...")
        clean()

    step = 2 if args.clean else 1
    total = 2 if not args.frontend else 3

    if args.frontend:
        print(f"\n[{step}/{total}] 构建前端...")
        build_frontend()
        step += 1

    print(f"\n[{step}/{total}] PyInstaller 打包...")
    rc = build_app()

    return rc


if __name__ == "__main__":
    sys.exit(main())
