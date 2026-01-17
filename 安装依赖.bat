@echo off
REM 设置控制台编码为 UTF-8
chcp 65001 >nul
cls
echo ███╗   ██╗  ██╗  ███████╗  ████████╗  ████████╗  ███████╗
echo ████╗  ██║  ██║  ██╔════╝  ╚══██╔══╝  ╚══██╔══╝  ██╔════╝
echo ██╔██╗ ██║  ██║  █████╗       ██║        ██║     ███████║
echo ██║╚██╗██║  ██║  ██╔══╝       ██║        ██║     ╚════██║
echo ██║ ╚████║  ██║  ███████╗     ██║        ██║     ███████║
echo ╚═╝  ╚═══╝  ╚═╝  ╚══════╝     ╚═╝        ╚═╝     ╚══════╝

REM 定义虚拟环境名称
setlocal enabledelayedexpansion
SET VENV_NAME=venv

REM 检查 Python 是否安装
where python >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo 未找到 Python，请安装 Python 并将其添加到 PATH。
    goto end
)

REM 检查虚拟环境是否存在，如果不存在则创建
IF NOT EXIST "%VENV_NAME%" (
    echo 正在创建虚拟环境...
    python -m venv %VENV_NAME%
    IF %ERRORLEVEL% NEQ 0 (
        echo 创建虚拟环境失败。
        goto end
    )
    echo 虚拟环境创建成功。
) ELSE (
    echo 虚拟环境已存在。
)

REM 激活虚拟环境
echo 正在激活虚拟环境...
call %VENV_NAME%\Scripts\activate.bat
IF %ERRORLEVEL% NEQ 0 (
    echo 激活虚拟环境失败。
    goto end
)
echo 虚拟环境已激活。

REM 开始安装依赖
echo 正在升级 pip...
python -m pip install --upgrade pip
IF %ERRORLEVEL% NEQ 0 (
    echo pip 升级失败。
    goto end
)
echo pip 升级完成。
echo 正在安装 requirements.txt 中的依赖...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
IF %ERRORLEVEL% NEQ 0 (
    echo 依赖安装失败。
    goto end
)
echo 所有依赖安装完成。

:end
pause
endlocal