@echo off
REM 启动脚本：检查虚拟环境、按需安装依赖并启动应用
chcp 65001 >nul
cls
echo ================= 启动脚本 =================

setlocal enabledelayedexpansion
SET VENV_NAME=venv
SET DEPS_MARK=%VENV_NAME%\.deps_installed

REM 检查 Python 是否安装
where python >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo 未找到 Python，请先安装 Python 并将其添加到 PATH。
    pause
    goto :eof
)

REM 如果虚拟环境不存在则创建
IF NOT EXIST "%VENV_NAME%" (
    echo 正在创建虚拟环境...
    python -m venv %VENV_NAME%
    IF %ERRORLEVEL% NEQ 0 (
        echo 创建虚拟环境失败。
        pause
        goto :eof
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
    pause
    goto :eof
)
echo 虚拟环境已激活。

REM 升级 pip（可选）
echo 正在检查 pip...
python -m pip install --upgrade pip >nul 2>nul

REM 如果没有安装标记，则安装 requirements.txt 中的依赖
IF NOT EXIST "%DEPS_MARK%" (
    if exist requirements.txt (
        echo 未检测到已安装标记，开始安装依赖（requirements.txt）...
        pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
        IF %ERRORLEVEL% NEQ 0 (
            echo 依赖安装失败，请检查网络或 requirements.txt 内容。
            pause
            goto :eof
        )
        REM 创建标记文件，表示已安装依赖
        echo 已安装 > "%DEPS_MARK%"
        echo 依赖安装完成。
    ) ELSE (
        echo 未找到 requirements.txt，跳过依赖安装。
    )
) ELSE (
    echo 已检测到依赖安装标记，跳过安装步骤。
)

REM 启动应用（根据需要修改启动命令）
echo 正在启动应用...
REM 如果你需要在后台运行或使用不同命令，请在这里修改，例如使用: python app.py 或 启动！！！.bat
python app.py

endlocal
