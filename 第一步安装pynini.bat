@echo off
REM 设置控制台编码为 UTF-8
chcp 65001
cls

echo 检查并创建/激活 conda 环境...

REM 定义 conda 环境名称
SET CONDA_ENV_NAME=nietts

REM 检查 conda 是否安装
where conda >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo 未找到 conda 命令。请确保已安装 Miniconda 或 Anaconda 并将其添加到 PATH。
    goto end
)

REM 配置 conda 镜像源 (可选，但推荐)
REM echo 正在配置 conda 镜像源...
REM onda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
REM conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
REM conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
REM conda config --set show_channel_urls yes

REM 检查环境是否存在，如果不存在则创建
conda info --envs | findstr /B /C:"%CONDA_ENV_NAME% " >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Conda 环境 "%CONDA_ENV_NAME%" 不存在，正在创建...
    conda create -n %CONDA_ENV_NAME% python=3.10 -y
    IF %ERRORLEVEL% NEQ 0 (
        echo 创建 Conda 环境失败。
        goto end
    )
    echo Conda 环境 "%CONDA_ENV_NAME%" 创建成功。
) ELSE (
    echo Conda 环境 "%CONDA_ENV_NAME%" 已存在。
)

REM 激活 conda 环境
echo 正在激活 Conda 环境 "%CONDA_ENV_NAME%"...
call conda activate %CONDA_ENV_NAME%
IF %ERRORLEVEL% NEQ 0 (
    echo 激活 Conda 环境失败。
    goto end
)
echo Conda 环境 "%CONDA_ENV_NAME%" 已激活。

echo 开始安装依赖...

REM 先使用 conda 安装 pynini
echo 正在使用 conda 安装 pynini...
conda install -c conda-forge pynini=2.1.5
echo pynini 安装完成。