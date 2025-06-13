@echo off
REM 设置控制台编码为 UTF-8
chcp 65001
cls

echo 检查并激活 Conda 环境...

REM 定义 Conda 环境名称
SET CONDA_ENV_NAME=nietts2.0

REM 激活 Conda 环境
call conda activate %CONDA_ENV_NAME%
IF %ERRORLEVEL% NEQ 0 (
    echo 激活 Conda 环境失败。请确保 Conda 已安装且环境名称正确。
    goto end
)

echo Conda 环境已激活。

echo 正在启动应用...                                
REM 在激活的 Conda 环境中运行 app.py
python app.py

echo 应用已退出。

:end
pause