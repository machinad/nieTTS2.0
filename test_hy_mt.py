#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单独测试 HY-MT1.5 翻译服务
"""

import asyncio
import sys
import io
from pathlib import Path

# Windows GBK 兼容: 强制 stdout/stderr 用 utf-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from engines.translate.hy_mt15_translate import HyMT15Translate


async def test_hy_mt():
    """测试 HY-MT 翻译服务"""

    print("=" * 60)
    print("HY-MT1.5 翻译服务测试")
    print("=" * 60)

    # 创建翻译引擎实例（使用正确路径）
    engine = HyMT15Translate(
        model_path="models/HY-mt/Hy-MT2-1.8B-2Bit.gguf",
        server_url="http://127.0.0.1:8081",
        llama_cpp_path="llama-cpp",
    )

    # 1. 检查模型文件是否存在
    print("\n[1/3] 检查模型文件...")
    model_path = Path(engine.model_path)
    if model_path.exists():
        print(f"  [OK] 模型文件存在: {model_path}")
        print(f"    文件大小: {model_path.stat().st_size / 1024 / 1024:.2f} MB")
    else:
        print(f"  [FAIL] 模型文件不存在: {model_path}")
        print("    请确保模型文件已下载到正确位置")
        return False

    # 2. 检查 llama-server 是否已经在运行
    print("\n[2/3] 检查 llama-server 状态...")
    try:
        import httpx
        r = httpx.get(f"{engine.server_url}/health", timeout=3)
        if r.status_code == 200:
            print(f"  [OK] llama-server 已经在运行 ({engine.server_url})")
        else:
            print(f"  [WARN] llama-server 返回异常状态码: {r.status_code}")
    except Exception as e:
        print(f"  [INFO] llama-server 未运行: {e}")
        print("    将在翻译时自动启动服务器")

    # 3. 测试翻译功能
    print("\n[3/3] 测试翻译功能...")
    test_cases = [
        ("你好，世界！", "中文", "英语"),
        ("今天天气真好", "中文", "日语"),
        ("Hello, how are you?", "英语", "中文"),
    ]

    results = []
    for text, source_lang, target_lang in test_cases:
        print(f"\n  测试: '{text}' ({source_lang} -> {target_lang})")
        try:
            result = await engine.translate(text, source_lang, target_lang)
            if result.is_success:
                print(f"    [OK] 翻译成功: {result.text}")
                results.append(True)
            else:
                print(f"    [FAIL] 翻译失败: {result.error}")
                results.append(False)
        except Exception as e:
            print(f"    [FAIL] 翻译异常: {e}")
            results.append(False)

    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"  模型文件: {'OK' if model_path.exists() else 'FAIL'}")
    print(f"  翻译测试: {sum(results)}/{len(results)} 通过")

    if all(results) and model_path.exists():
        print("\n[SUCCESS] HY-MT1.5 翻译服务测试通过！")
        return True
    else:
        print("\n[FAILED] HY-MT1.5 翻译服务测试失败")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_hy_mt())
    sys.exit(0 if success else 1)
