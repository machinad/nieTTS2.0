# 腾讯混元 HY-MT1.5-1.8B 翻译模型接入指南

> 基于实际项目踩坑经验整理，适用于任何需要接入该模型的新项目。

---

## 一、模型概述

| 项目 | 说明 |
|------|------|
| 模型名称 | HY-MT1.5-1.8B（腾讯混元翻译模型 1.5 版） |
| 参数规模 | 1.8B |
| 量化格式 | Q8_0（GGUF，约 1.9GB） |
| 支持语种 | 33 种语言 + 5 种方言变体 |
| 推理引擎 | llama.cpp（b9209 或更新版本） |
| 推理方式 | llama-server（HTTP API） |
| 下载源 | HuggingFace / ModelScope |

---

## 二、环境搭建

### 2.1 获取 llama.cpp 二进制

从 GitHub Releases 下载预编译包（Windows 为例）：

```
https://github.com/ggml-org/llama.cpp/releases/download/b9209/
├── llama-server.exe      # HTTP 服务（核心）
├── ggml.dll / ggml-base.dll / ggml-cpu-*.dll  # 运行时依赖
├── llama.dll
└── llama-common.dll
```

> **注意**：所有 DLL 文件必须与 `llama-server.exe` 在同一目录，缺一不可。

### 2.2 获取 GGUF 模型文件

从 ModelScope 下载（国内推荐，速度快）：

```
https://modelscope.cn/models/Tencent-Hunyuan/HY-MT1.5-1.8B-GGUF/resolve/master/HY-MT1.5-1.8B-Q8_0.gguf
```

或从 HuggingFace 下载：

```
https://huggingface.co/tencent/HY-MT1.5-1.8B-GGUF/resolve/main/HY-MT1.5-1.8B-Q8_0.gguf
```

**SHA256 校验**（Q8_0）：
```
6789b06d0902f2f5312c0e1703d56ccbddfcfb6c653d22519b7c720f7db9a98e
```

### 2.3 启动 llama-server

```bash
llama-server.exe \
  -m ./models/HY-MT1.5-1.8B-Q8_0.gguf \
  --host 127.0.0.1 \
  --port 8081 \
  -ngl 99 \
  -c 4096 \
  --no-warmup
```

| 参数 | 说明 |
|------|------|
| `-ngl 99` | GPU 加速层数（纯 CPU 环境会自动忽略，设为 99 即可） |
| `-c 4096` | 上下文长度（模型训练上下文 262144，但 4096 够翻译用） |
| `--no-warmup` | **必须**，否则 warmup 会影响推理结果 |

---

## 三、核心雷点（按重要性排序）

### 雷点 1：必须使用 Chat Completions 端点（致命）

**现象**：翻译结果完全无关，输出随机文本续写（如 C++ 教程、Linux 教程），而非翻译内容。术语叫"答非所问"。

**根因**：HY-MT1.5-1.8B 的 GGUF 文件中内置了 **Chat Template**，包含特殊格式标记：

```
<｜hy_begin▁of▁sentence｜>You are a helpful assistant<｜hy_place▁holder▁no▁3｜><｜hy_User｜>{用户输入}<｜hy_Assistant｜>
```

- 使用 `/completion` 端点 → 裸文本入模，模型不识别指令结构 → 当作文本续写 → **输出随机垃圾**
- 使用 `/v1/chat/completions` 端点 → 自动套用 Chat Template → **翻译正确**

**正确做法**：

```python
# ❌ 错误：用 /completion 端点
resp = httpx.post("http://127.0.0.1:8081/completion", json={
    "prompt": "将以下文本翻译为中文...",
    ...
})

# ✅ 正确：用 /v1/chat/completions 端点
resp = httpx.post("http://127.0.0.1:8081/v1/chat/completions", json={
    "messages": [
        {"role": "user", "content": "将以下文本翻译为中文..."}
    ],
    ...
})
```

**Chat Completions 响应格式**：

```python
result = resp.json()
translated = result["choices"][0]["message"]["content"]
```

### 雷点 2：Prompt 格式必须与训练时一致（严重）

**官方 Prompt 模板**分为两类：

#### 中文 ↔ 其他语言（ZH ↔ XX）

```
将以下文本翻译为{target_language}，注意只需要输出翻译后的结果，不要额外解释：

{source_text}
```

#### 非中文语言之间（XX ↔ XX，不含中文）

```
Translate the following segment into {target_language}, without additional explanation.

{source_text}
```

**注意两个关键点**：

1. **必须有空行分隔**：指令和待翻译文本之间必须有一个空行（`\n\n`），
   写成 `...不要额外解释：{text}`（无换行）会导致模型无法区分指令和内容。

2. **根据语言对切换模板**：
   - 涉及中文 → 用中文模板
   - 不涉及中文 → 用英文模板
   - 源语言为 `auto` 时可默认中文模板

```python
# ✅ 正确：有空行 + 按语言对选模板
is_zh = source_lang in ("zh", "zh-Hant", "auto") or target_lang in ("zh", "zh-Hant")

if is_zh:
    prompt = f"将以下文本翻译为{target_name}，注意只需要输出翻译后的结果，不要额外解释：\n\n{text}"
else:
    prompt = f"Translate the following segment into {target_name}, without additional explanation.\n\n{text}"
```

3. **目标语言用全名而非代码**：模型训练时用的语言全名，不是 ISO 代码。
   ```
   ✅ "中文" / "English" / "日本語"
   ❌ "zh"   / "en"      / "ja"
   ```

### 雷点 3：必须加 --no-warmup（重要）

llama-server 默认会执行 warmup 推理来预热 GPU。官方文档明确指出该模型需加 `--no-warmup`。

不加此标志时，warmup 的 KV cache 残留可能导致后续真实请求的推理质量下降或输出异常（即使请求在被分配了不同 slot 的情况下）。

### 雷点 4：推理参数需按官方推荐（重要）

```json
{
  "temperature": 0.7,
  "top_k": 20,
  "top_p": 0.6,
  "repeat_penalty": 1.05
}
```

**不要在请求中添加额外的采样参数**（如 `min_p: 0.05`、`dry_*` 等），llama-server 的默认值已足够。擅自添加可能干扰翻译质量。

### 雷点 5：不要加 system prompt

官方明确说明："Note that our model does not have the default system_prompt."

在 `/v1/chat/completions` 请求中，`messages` 数组只放 `{"role": "user", "content": "..."}` 一条消息即可，不要添加 `{"role": "system", "content": "..."}`。

### 雷点 6：输出清理

模型偶尔会输出特殊的占位符或 XML 风格的标签，建议做后处理：

```python
import re
translated = re.sub(r'<[^>]+>', '', translated)  # 去掉 <tag> 类标记
translated = translated.strip()
```

### 雷点 7：温度参数不应放在服务端启动参数中

llama-server 启动时如果通过 CLI 传入了 `--temp` 等参数，它们将成为**默认值**，但每个请求仍可覆盖。建议不要在启动命令中设置采样参数，而是在每个请求的 JSON body 中指定，保持灵活性。

`--no-warmup` 以外的采样参数（`--temp`、`--top-k`、`--top-p`、`--repeat-penalty`）都应从启动命令中移除，改在请求中传递。

---

## 四、完整工作代码（Python 后端参考）

### 4.1 服务端启动

```python
import subprocess
from pathlib import Path

LLAMA_EXE = Path("./llama-cpp/llama-server.exe")
MODEL_PATH = Path("./models/HY-MT1.5-1.8B-Q8_0.gguf")
LLAMA_PORT = 8081

cmd = [
    str(LLAMA_EXE),
    "-m", str(MODEL_PATH),
    "--host", "127.0.0.1",
    "--port", str(LLAMA_PORT),
    "-ngl", "99",
    "-c", "4096",
    "--no-warmup",       # 关键！
]

process = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)

# 等待就绪
import httpx, asyncio

async def wait_ready(timeout=15):
    for _ in range(int(timeout / 0.5)):
        await asyncio.sleep(0.5)
        try:
            r = httpx.get(f"http://127.0.0.1:{LLAMA_PORT}/health", timeout=3)
            if r.status_code == 200:
                return True
        except Exception:
            continue
    return False
```

### 4.2 翻译请求

```python
import httpx, re

LANGUAGES = {
    "zh": "中文", "en": "English", "ja": "日本語",
    "ko": "한국어", "fr": "Français", "de": "Deutsch",
    "es": "Español", "ru": "Русский", "ar": "العربية",
    # ... 完整列表见官方 README
}

async def translate(text: str, source_lang: str, target_lang: str) -> str:
    target_name = LANGUAGES.get(target_lang, target_lang)

    # 按语言对选择正确的提示模板
    is_zh = source_lang in ("zh", "zh-Hant", "auto") or target_lang in ("zh", "zh-Hant")
    if is_zh:
        prompt = (
            f"将以下文本翻译为{target_name}，"
            f"注意只需要输出翻译后的结果，不要额外解释：\n\n"
            f"{text}"
        )
    else:
        prompt = (
            f"Translate the following segment into {target_name}, "
            f"without additional explanation.\n\n"
            f"{text}"
        )

    payload = {
        "messages": [
            {"role": "user", "content": prompt}  # 无 system 消息！
        ],
        "temperature": 0.7,
        "top_k": 20,
        "top_p": 0.6,
        "repeat_penalty": 1.05,
    }

    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(
            f"http://127.0.0.1:{LLAMA_PORT}/v1/chat/completions",
            json=payload,
        )
        resp.raise_for_status()
        result = resp.json()
        translated = result["choices"][0]["message"]["content"]
        translated = re.sub(r'<[^>]+>', '', translated)
        return translated.strip()
```

### 4.3 健康检查

```python
async def check_health() -> bool:
    try:
        r = httpx.get(f"http://127.0.0.1:{LLAMA_PORT}/health", timeout=3)
        return r.status_code == 200
    except Exception:
        return False
```

---

## 五、排查清单（出现问题时逐项检查）

| # | 检查项 | 正确值 |
|---|--------|--------|
| 1 | 调用的是 `/v1/chat/completions` 而非 `/completion`？ | ✅ `/v1/chat/completions` |
| 2 | 启动命令有 `--no-warmup` 吗？ | ✅ 有 |
| 3 | 指令和待翻译文本之间有 `\n\n` 空行吗？ | ✅ 有空行 |
| 4 | 非中文语言对用的是英文模板吗？ | ✅ `Translate the following segment into...` |
| 5 | `messages` 中没有 system 消息吗？ | ✅ 只有 `role: "user"` |
| 6 | 目标语言用的是全名而非 ISO 代码吗？ | ✅ "中文" / "English"，不是 "zh" / "en" |
| 7 | 推理参数是官方推荐的 4 个吗？ | ✅ temp=0.7, top_k=20, top_p=0.6, repeat_penalty=1.05 |
| 8 | 采样参数只在请求 body 传，不在启动 CLI 传吗？ | ✅ CLI 不传采样参数 |
| 9 | 模型文件 SHA256 匹配吗？ | ✅ 校验哈希 |
| 10 | 输出做了 `re.sub(r'<[^>]+>', '', ...)` 清理吗？ | ✅ 有清理 |

---

## 六、语言代码对照表（常用）

| 代码 | 全名 | 代码 | 全名 |
|------|------|------|------|
| zh | 中文 | zh-Hant | 繁體中文 |
| en | English | ja | 日本語 |
| ko | 한국어 | fr | Français |
| de | Deutsch | es | Español |
| ru | Русский | ar | العربية |
| pt | Português | it | Italiano |
| th | ไทย | vi | Tiếng Việt |
| tr | Türkçe | pl | Polski |
| nl | Nederlands | id | Bahasa Indonesia |
| yue | 粤语 | | |

完整 33 种语言见官方 README。
