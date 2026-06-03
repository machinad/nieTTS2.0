#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 HY-MT1.5 翻译服务 - GPU 加速检测与性能对比
"""

import asyncio
import sys
import io
import time
import subprocess
import httpx
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent))

SERVER_URL = "http://127.0.0.1:8081"
MODEL_PATH = "models/HY-mt/Hy-MT2-1.8B-2Bit.gguf"
LLAMA_CPP_PATH = Path("llama-cpp")


def stop_server():
    """停止已有的 llama-server"""
    try:
        r = httpx.get(f"{SERVER_URL}/health", timeout=2)
        # 如果能访问说明有服务器在跑，先杀掉
    except Exception:
        return

    # 通过端口查找进程并结束
    try:
        result = subprocess.run(
            ["netstat", "-ano"], capture_output=True, text=True
        )
        for line in result.stdout.splitlines():
            if ":8081" in line and "LISTENING" in line:
                pid = line.strip().split()[-1]
                subprocess.run(["taskkill", "/F", "/PID", pid], capture_output=True)
                print(f"  已停止旧服务器进程 (PID: {pid})")
                time.sleep(1)
                return
    except Exception:
        pass


def start_server(use_gpu=True, gpu_layers=99):
    """启动 llama-server"""
    server_exe = LLAMA_CPP_PATH / "llama-server.exe"
    cmd = [
        str(server_exe),
        "-m", MODEL_PATH,
        "--host", "127.0.0.1",
        "--port", "8081",
        "-c", "4096",
        "--no-warmup",
    ]
    if use_gpu:
        cmd.extend(["-ngl", str(gpu_layers)])
    else:
        cmd.extend(["-ngl", "0"])  # 纯 CPU

    print(f"  启动命令: {' '.join(cmd)}")
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return process


def wait_server_ready(timeout=30):
    """等待服务器就绪"""
    for i in range(int(timeout / 0.5)):
        time.sleep(0.5)
        try:
            r = httpx.get(f"{SERVER_URL}/health", timeout=2)
            if r.status_code == 200:
                return True
        except Exception:
            continue
    return False


def check_gpu_info(process):
    """从服务器启动日志中提取 GPU 信息"""
    gpu_info = {"cuda": False, "vulkan": False, "gpu_name": "", "layers": ""}
    try:
        # 非阻塞读取日志
        import select
        import msvcrt
        # Windows 下用不同方式读取
        time.sleep(2)  # 等待一些日志输出
        # 直接检查进程输出
        pass
    except Exception:
        pass
    return gpu_info


async def translate_test(text, source_lang, target_lang):
    """执行一次翻译并返回用时"""
    from engines.translate.hy_mt15_translate import HyMT15Translate
    engine = HyMT15Translate(
        model_path=MODEL_PATH,
        server_url=SERVER_URL,
        llama_cpp_path=str(LLAMA_CPP_PATH),
    )
    start = time.perf_counter()
    result = await engine.translate(text, source_lang, target_lang)
    elapsed = time.perf_counter() - start
    return result, elapsed


async def run_benchmark(label):
    """运行基准测试"""
    print(f"\n{'=' * 60}")
    print(f"基准测试: {label}")
    print(f"{'=' * 60}")

    test_cases = [
        ("你好，世界！", "中文", "英语"),
        ("今天天气真好", "中文", "英语"),
        ("我喜欢在VRChat里和朋友们一起玩", "中文", "英语"),
        ("这是一段比较长的文本，用来测试翻译引擎处理较长内容时的性能表现，看看需要多长时间才能完成翻译。", "中文", "英语"),
    ]

    times = []
    for text, src, tgt in test_cases:
        result, elapsed = await translate_test(text, src, tgt)
        status = "OK" if result.is_success else "FAIL"
        print(f"  [{status}] {elapsed:.3f}s - {text[:20]}... -> {result.text[:30] if result.is_success else result.error}")
        if result.is_success:
            times.append(elapsed)

    if times:
        print(f"\n  统计:")
        print(f"    最快: {min(times):.3f}s")
        print(f"    最慢: {max(times):.3f}s")
        print(f"    平均: {sum(times)/len(times):.3f}s")
    return times


async def main():
    print("=" * 60)
    print("HY-MT1.5 GPU 加速测试")
    print("=" * 60)
    print(f"  显卡: RTX 2070 Super")
    print(f"  模型: {MODEL_PATH}")

    model = Path(MODEL_PATH)
    if not model.exists():
        print(f"\n[FAIL] 模型文件不存在: {model}")
        return

    print(f"  模型大小: {model.stat().st_size / 1024 / 1024:.2f} MB")

    # ========== 测试 1: GPU 模式 ==========
    print("\n" + "=" * 60)
    print("[测试 1] GPU 模式启动")
    print("=" * 60)

    stop_server()
    print("\n  启动 llama-server (GPU 模式, -ngl 99)...")
    gpu_process = start_server(use_gpu=True, gpu_layers=99)

    # 读取启动日志
    print("  等待服务器启动...")
    time.sleep(3)
    # 尝试读取 stderr 输出
    gpu_log_lines = []
    try:
        import threading
        def read_output(proc, lines):
            for line in proc.stdout:
                lines.append(line.strip())
                if len(lines) > 50:
                    break
        t = threading.Thread(target=read_output, args=(gpu_process, gpu_log_lines), daemon=True)
        t.start()
        t.join(timeout=5)
    except Exception:
        pass

    if wait_server_ready():
        print("  [OK] GPU 模式服务器启动成功！")
        print("\n  启动日志 (关键信息):")
        for line in gpu_log_lines:
            line_lower = line.lower()
            if any(kw in line_lower for kw in ["cuda", "vulkan", "gpu", "layer", "ggml", "model", "loading"]):
                print(f"    {line}")

        gpu_times = await run_benchmark("GPU 模式")
    else:
        print("  [FAIL] GPU 模式服务器启动超时")
        print("  可能原因: CUDA 版本不兼容、显存不足、驱动问题")
        gpu_times = []

        # 打印日志帮助诊断
        print("\n  服务器日志 (用于诊断):")
        for line in gpu_log_lines[:20]:
            print(f"    {line}")

    # 停止 GPU 服务器
    stop_server()
    time.sleep(2)

    # ========== 测试 2: CPU 模式 ==========
    print("\n" + "=" * 60)
    print("[测试 2] CPU 模式启动")
    print("=" * 60)

    print("\n  启动 llama-server (CPU 模式, -ngl 0)...")
    cpu_process = start_server(use_gpu=False)

    print("  等待服务器启动...")
    time.sleep(3)
    cpu_log_lines = []
    try:
        import threading
        def read_output(proc, lines):
            for line in proc.stdout:
                lines.append(line.strip())
                if len(lines) > 50:
                    break
        t = threading.Thread(target=read_output, args=(cpu_process, cpu_log_lines), daemon=True)
        t.start()
        t.join(timeout=5)
    except Exception:
        pass

    if wait_server_ready():
        print("  [OK] CPU 模式服务器启动成功！")
        cpu_times = await run_benchmark("CPU 模式")
    else:
        print("  [FAIL] CPU 模式服务器启动超时")
        cpu_times = []

    # 停止 CPU 服务器
    stop_server()

    # ========== 结果对比 ==========
    print("\n" + "=" * 60)
    print("GPU vs CPU 性能对比")
    print("=" * 60)

    if gpu_times and cpu_times:
        gpu_avg = sum(gpu_times) / len(gpu_times)
        cpu_avg = sum(cpu_times) / len(cpu_times)
        speedup = cpu_avg / gpu_avg if gpu_avg > 0 else 0

        print(f"\n  GPU 模式平均用时: {gpu_avg:.3f}s")
        print(f"  CPU 模式平均用时: {cpu_avg:.3f}s")
        print(f"  加速比: {speedup:.2f}x")

        if speedup > 1.5:
            print(f"\n  [结论] GPU 加速有效，提速 {speedup:.1f} 倍！建议使用 GPU 模式。")
        elif speedup > 1:
            print(f"\n  [结论] GPU 有一定加速效果 ({speedup:.1f}x)，但提升不大。")
        else:
            print(f"\n  [结论] GPU 模式没有明显加速，可能未正确使用 GPU。")
    elif gpu_times:
        print(f"\n  仅 GPU 模式成功，平均: {sum(gpu_times)/len(gpu_times):.3f}s")
    elif cpu_times:
        print(f"\n  仅 CPU 模式成功，平均: {sum(cpu_times)/len(cpu_times):.3f}s")
        print("  建议检查 CUDA 驱动和 llama.cpp 编译版本。")
    else:
        print("\n  两种模式都未能成功启动，请检查 llama-server 和模型文件。")


if __name__ == "__main__":
    asyncio.run(main())
