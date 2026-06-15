# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec 文件 — nieTTS 2.0 打包配置（文件夹模式）"""

import os
import sys

from PyInstaller.utils.hooks import collect_data_files, collect_all

block_cipher = None
ROOT = os.path.abspath(SPECPATH)

# 收集 sherpa_onnx 全部文件（含 DLL、Python 模块、数据文件）
sherpa_datas, sherpa_binaries, sherpa_hiddenimports = collect_all('sherpa_onnx')

a = Analysis(
    [os.path.join(ROOT, 'gui_main.py')],
    pathex=[ROOT],
    binaries=sherpa_binaries,
    datas=[
        # 前端构建产物（Quart SPA 服务）
        (os.path.join(ROOT, 'templates'), 'templates'),
        # GUI 图标资源（QSS 主题引用）
        (os.path.join(ROOT, 'gui', 'assets'), os.path.join('gui', 'assets')),
        # 版本文件
        (os.path.join(ROOT, 'version.py'), '.'),
    ] + sherpa_datas,
    hiddenimports=[
        'qasync',
        'edge_tts',
        'dashscope',
        'pythonosc',
        'pythonosc.osc_bundle_builder',
        'pythonosc.osc_message',
        'pythonosc.osc_message_builder',
        'httpx',
        'openai',
        'cryptography',
        'miniaudio',
        'numpy',
        'huggingface_hub',
        'modelscope',
        'quart',
        'quart_cors',
        'engines.tts.service',
        'engines.tts.edge_tts',
        'engines.tts.matcha_tts',
        'engines.tts.cosyvoice_tts',
        'engines.tts.sambert_tts',
        'engines.translate.service',
        'engines.translate.openai_translate',
        'engines.translate.hy_mt15_translate',
        'engines.stt.service',
        'engines.stt.qwen3_stt',
        'engines.stt.vad.silero_vad',
        'engines.osc.service',
        'engines.audio.playback',
        'engines.pipeline',
        'scripts.download_models',
        'scripts.model_registry',
    ] + sherpa_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'PIL',
        'pandas',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='nieTTS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,           # GUI 模式，不显示控制台
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,               # 可替换为 .ico 图标文件
    contents_directory='.',  # 平铺模式：所有文件与 exe 同级，不嵌套 _internal/
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='nieTTS',
)
