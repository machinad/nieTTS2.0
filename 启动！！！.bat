@echo off
REM 设置控制台编码为 UTF-8
chcp 65001
cls

echo 检查并激活虚拟环境...

REM 定义虚拟环境路径
SET VENV_PATH=.\venv

REM 检查虚拟环境激活脚本是否存在
IF EXIST "%VENV_PATH%\Scripts\activate.bat" (
    echo 找到虚拟环境，正在激活...
    call "%VENV_PATH%\Scripts\activate.bat"
    echo 虚拟环境已激活。
) ELSE (
    echo 未找到虚拟环境 "%VENV_PATH%"。请先运行 安装依赖.bat 创建并安装依赖。
    goto end
)

echo 正在启动应用...
REM 在激活的虚拟环境中运行 app.py
python app.py

echo 应用已退出。

:end
pause