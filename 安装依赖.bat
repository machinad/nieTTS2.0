@echo off
REM 设置控制台编码为 UTF-8
chcp 65001
cls
echo ███╗   ██╗  ██╗  ███████╗  ████████╗  ████████╗  ███████╗
echo ████╗  ██║  ██║  ██╔════╝  ╚══██╔══╝  ╚══██╔══╝  ██╔════╝
echo ██╔██╗ ██║  ██║  █████╗       ██║        ██║     ███████╗
echo ██║╚██╗██║  ██║  ██╔══╝       ██║        ██║     ╚════██║
echo ██║ ╚████║  ██║  ███████╗     ██║        ██║     ███████║
echo ╚═╝  ╚═══╝  ╚═╝  ╚══════╝     ╚═╝        ╚═╝     ╚══════╝
echo 检查并创建/激活 conda 环境...

REM 定义 conda 环境名称
SET CONDA_ENV_NAME=nietts3.0

REM 检查 conda 是否安装
where conda >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo 未找到 conda 命令。请确保已安装 Miniconda 或 Anaconda 并将其添加到 PATH。
    goto end
)

REM 配置 conda 镜像源 (可选，但推荐)
echo 正在配置 conda 镜像源...
call conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
call conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
call conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
call conda config --set show_channel_urls yes

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
REM 先降级 pip 到指定版本
echo 正在将 pip 降级到 23.3.1 版本...
python -m pip install pip==23.3.1 -i https://pypi.tuna.tsinghua.edu.cn/simple
IF %ERRORLEVEL% NEQ 0 (
    echo pip 降级失败。
    goto end
)
echo pip 已降级到 23.3.1。

REM 先使用 conda 安装 pynini
echo 正在使用 conda 安装 pynini...
call conda install -c conda-forge pynini=2.1.5 -y
echo pynini 安装完成。

REM 使用 pip 安装 WeTextProcessing
echo 正在使用 pip 安装 WeTextProcessing...
pip install WeTextProcessing==1.0.3 -i https://mirrors.aliyun.com/pypi/simple
IF %ERRORLEVEL% NEQ 0 (
    echo 使用 pip 安装 WeTextProcessing 失败。
    pause
    goto end
)
echo WeTextProcessing 安装完成。

REM 使用 pip 安装 PyTorch
echo 正在使用 pip 安装 PyTorch...
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
IF %ERRORLEVEL% NEQ 0 (
    echo 使用 pip 安装 PyTorch 失败。
    pause
    goto end
)
echo PyTorch 安装完成。

REM 使用 pip 安装主项目的 requirements.txt 中的其余依赖
echo 正在使用 pip 安装 requirements.txt 中的其余依赖...
pip install dotenv -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install -r requirements.txt --verbose
IF %ERRORLEVEL% NEQ 0 (
    echo 安装 requirements.txt 中的依赖失败。
    goto end
)
echo requirements.txt 中的依赖安装完成。
echo 所有依赖安装完成。

:end
pause