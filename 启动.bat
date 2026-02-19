@echo off
REM 启动脚本：使用 uv 管理依赖并启动应用
chcp 65001 >nul
cls
echo ================= nieTTS2.0 启动脚本 =================
echo 使用 uv 管理 Python 环境
echo.

setlocal enabledelayedexpansion

REM 检查 uv 是否安装
where uv >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo [错误] 未找到 uv，请先安装 uv。
    echo 安装方法: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    pause
    goto :eof
)
echo [OK] uv 已安装

REM 同步依赖（根据 pyproject.toml）
echo 正在同步依赖...
uv sync
IF %ERRORLEVEL% NEQ 0 (
    echo [错误] 依赖同步失败。
    pause
    goto :eof
)
echo [OK] 依赖同步完成

REM 启动应用
echo.
echo 正在启动 nieTTS2.0...
echo.
uv run python app.py

endlocal