REM 设置镜像地址
set HF_ENDPOINT=https://hf-mirror.com

REM 激活虚拟环境
call conda activate nietts2.0
REM 或者使用 venv
REM call your_env_path\Scripts\activate

REM 创建本地目录 
mkdir checkpoints

REM 下载模型文件（确保你已安装 huggingface_hub）
huggingface-cli download IndexTeam/IndexTTS-1.5 config.yaml bigvgan_discriminator.pth bigvgan_generator.pth bpe.model dvae.pth gpt.pth unigram_12000.vocab --local-dir checkpoints --revision main