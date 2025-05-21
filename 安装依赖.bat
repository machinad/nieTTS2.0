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
    echo 未找到虚拟环境 "%VENV_PATH%"，正在创建...
    REM 使用当前系统安装的 python 创建虚拟环境
    python -m venv %VENV_PATH%
    IF %ERRORLEVEL% NEQ 0 (
        echo 创建虚拟环境失败。请确保已安装 Python 并将其添加到 PATH。
        goto end
    )
    echo 虚拟环境创建成功，正在激活...
    call "%VENV_PATH%\Scripts\activate.bat"
    echo 虚拟环境已激活。
)

echo 使用镜像源安装依赖...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo 依赖安装完成。

:end
pause