import xml.etree.ElementTree as ET

def svg_rect(parent, x, y, w, h, rx=4, fill="#fff", stroke="#ccc", sw=1.5, dash=None):
    attrs = {"x": str(x), "y": str(y), "width": str(w), "height": str(h),
             "rx": str(rx), "fill": fill, "stroke": stroke, "stroke-width": str(sw)}
    e = ET.SubElement(parent, "rect", attrib=attrs)
    if dash:
        e.set("stroke-dasharray", dash)
    return e

def svg_text(parent, x, y, text, size=12, fill="#333", bold=False, anchor="start", font="monospace"):
    el = ET.SubElement(parent, "text", attrib={
        "x": str(x), "y": str(y), "font-size": str(size), "fill": fill,
        "font-family": font, "font-weight": "bold" if bold else "normal",
        "text-anchor": anchor
    })
    el.text = text
    return el

def svg_line(parent, x1, y1, x2, y2, stroke="#999", sw=1.5, dash=None):
    attrs = {"x1": str(x1), "y1": str(y1), "x2": str(x2), "y2": str(y2),
             "stroke": stroke, "stroke-width": str(sw)}
    e = ET.SubElement(parent, "line", attrib=attrs)
    if dash:
        e.set("stroke-dasharray", dash)
    return e

def arrow_right(parent, x, y, dest_x, color="#58a6ff"):
    svg_line(parent, x, y, dest_x, y, stroke=color, sw=2)
    ET.SubElement(parent, "polygon", attrib={
        "points": f"{dest_x},{y} {dest_x-8},{y-5} {dest_x-8},{y+5}",
        "fill": color
    })

def arrow_left(parent, x, y, dest_x, color="#58a6ff"):
    svg_line(parent, x, y, dest_x, y, stroke=color, sw=2)
    ET.SubElement(parent, "polygon", attrib={
        "points": f"{dest_x},{y} {dest_x+8},{y-5} {dest_x+8},{y+5}",
        "fill": color
    })

def arrow_down(parent, x, y, dest_y, color="#58a6ff"):
    svg_line(parent, x, y, x, dest_y, stroke=color, sw=2)
    ET.SubElement(parent, "polygon", attrib={
        "points": f"{x},{dest_y} {x-5},{dest_y-8} {x+5},{dest_y-8}",
        "fill": color
    })

def arrow_up(parent, x, y, dest_y, color="#58a6ff"):
    svg_line(parent, x, y, x, dest_y, stroke=color, sw=2)
    ET.SubElement(parent, "polygon", attrib={
        "points": f"{x},{dest_y} {x-5},{dest_y+8} {x+5},{dest_y+8}",
        "fill": color
    })

def box(parent, x, y, w, h, color="#58a6ff", title="", subtitle=""):
    svg_rect(parent, x, y, w, h, fill="#161b22", stroke=color, sw=2, rx=8)
    svg_text(parent, x + 14, y + 26, title, size=13, fill=color, bold=True)
    if subtitle:
        svg_text(parent, x + 14, y + 44, subtitle, size=10, fill="#8b949e")

def subbox(parent, x, y, w, h, fill="#1a2332", stroke="#30363d", title=""):
    svg_rect(parent, x, y, w, h, fill=fill, stroke=stroke, sw=1, rx=5)
    if title:
        svg_text(parent, x + 10, y + 18, title, size=10, fill="#c9d1d9")
    return (x, y, w, h)

W, H = 1400, 1050
svg = ET.Element("svg", xmlns="http://www.w3.org/2000/svg", width=str(W), height=str(H),
                  viewBox=f"0 0 {W} {H}")
ET.SubElement(svg, "rect", width=str(W), height=str(H), fill="#0d1117")

C  = {
    "bg_box":   "#161b22", "border":   "#30363d",
    "accent":   "#58a6ff", "green":    "#3fb950",
    "orange":   "#d2991d", "purple":   "#bc8cff",
    "red":      "#f85149", "text":     "#c9d1d9",
    "muted":    "#8b949e", "yellow":   "#e3b341",
    "queue_bg": "#1a2332", "dark_green": "#0d2818",
    "dark_purple": "#1a1520",
}
g = ET.SubElement(svg, "g")

# Outer border
svg_rect(g, 10, 10, W - 20, H - 20, fill="none", stroke=C["border"], sw=1, rx=4, dash="4,4")

# Title
svg_text(g, W / 2, 46, "nieTTS 2.0  —  Architecture Overview", size=20, fill=C["accent"],
         bold=True, anchor="middle")
svg_text(g, W / 2, 66, "Request Queue (Serial)  →  Parallel Processing  →  Play Queue (FIFO)",
         size=11, fill=C["muted"], anchor="middle")

# ======================== FRONTEND (Vue 3) ========================
x0, y0 = 50, 90
box(g, x0, y0, 240, 180, color=C["green"], title="Vue 3 Frontend", subtitle="localhost:5173")

subbox(g, x0 + 12, y0 + 50, 216, 52, fill=C["dark_green"], stroke=C["green"],
       title="TTS Control Panel")
svg_text(g, x0 + 22, y0 + 72, "Engine · Voice · Translate", size=9, fill=C["green"])
svg_text(g, x0 + 22, y0 + 88, "OSC · PlayTranslation toggles", size=9, fill=C["green"])

subbox(g, x0 + 12, y0 + 112, 100, 52, fill=C["dark_green"], stroke=C["green"],
       title="WebSocket (↑)")
svg_text(g, x0 + 22, y0 + 134, "Audio Stream", size=9, fill=C["green"])
svg_text(g, x0 + 22, y0 + 148, "Int16 44.1kHz mono", size=8, fill=C["muted"])

subbox(g, x0 + 128, y0 + 112, 100, 52, fill=C["dark_green"], stroke=C["green"],
       title="WebSocket (↓)")
svg_text(g, x0 + 138, y0 + 134, "Logs", size=9, fill=C["green"])
svg_text(g, x0 + 138, y0 + 148, "Status · STT result", size=8, fill=C["muted"])

# ======================== VRChat ========================
box(g, x0, y0 + 210, 240, 70, color=C["purple"], title="VRChat OSC", subtitle="127.0.0.1:9000")
svg_text(g, x0 + 14, y0 + 262, "/chatbox/input  [text, True]", size=10, fill=C["purple"])

# ======================== WEBSERVER ========================
x1, y1 = 360, 90
box(g, x1, y1, 260, 340, color=C["accent"], title="WebServer (Quart)", subtitle="0.0.0.0:11451")

routes_y = y1 + 54
routes = [
    ("POST", "/tts", "submit text TTS", C["orange"]),
    ("GET",  "/voices", "engine + voice list", C["orange"]),
    ("WS",   "/ws", "bidirectional", C["purple"]),
    ("GET",  "/config", "read", C["muted"]),
    ("POST", "/config", "write", C["muted"]),
]
for i, (method, path, desc, clr) in enumerate(routes):
    ry = routes_y + i * 18
    svg_text(g, x1 + 14, ry, method, size=9, fill=clr, bold=True)
    svg_text(g, x1 + 52, ry, path, size=9, fill=C["accent"])
    svg_text(g, x1 + 195, ry, desc, size=9, fill=C["muted"])

# WS handler subbox
wsy = routes_y + 5 * 18 + 10
subbox(g, x1 + 14, wsy, 232, 56, title="WebSocket Handler")
svg_text(g, x1 + 24, wsy + 22, "bytes → VAD buffer", size=9, fill=C["green"])
svg_text(g, x1 + 24, wsy + 38, "json  → log / status push", size=9, fill=C["orange"])

# Config subbox
cfg_y = wsy + 72
subbox(g, x1 + 14, cfg_y, 232, 82, title="ConfigManager")
svgs = ["TTS Provider · Voice", "Translate · OSC · Playback",
        "STT · VAD models (P2)", "Device · Language · API keys"]
for i, s in enumerate(svgs):
    svg_text(g, x1 + 24, cfg_y + (i + 1) * 14, s, size=8, fill=C["muted"])

# ======================== Engine Layer ========================
ex, ey = 300, 460
box(g, ex, ey, 290, 190, color=C["accent"], title="Engine Layer", subtitle="engines/")

engines = [
    ("tts/service.py",        "TTSService",      C["green"]),
    ("translate/service.py",  "TranslateService", C["purple"]),
    ("stt/service.py",        "STTService (P2)",  C["orange"]),
    ("osc/service.py",        "OSCService",       C["purple"]),
    ("audio/playback.py",     "miniaudio",        C["red"]),
]
for i, (path, name, clr) in enumerate(engines):
    eyy = ey + 46 + i * 20
    svg_text(g, ex + 14, eyy, path, size=10, fill=C["accent"])
    svg_text(g, ex + 155, eyy, name, size=10, fill=clr)

# Config connection
svg_line(g, ex + 290, ey + 100, x1 + 130, ey + 100, stroke=C["accent"], sw=1, dash="4,4")
svg_text(g, ex + 190, ey + 93, "config", size=8, fill=C["muted"])

# ======================== CORE PIPELINE ========================
x2, y2 = 680, 90
box(g, x2, y2, 670, 680, color=C["orange"], title="RequestPipeline",
    subtitle="engines/pipeline.py — 核心调度器")

# --- RequestQueue ---
rq_y = y2 + 56
subbox(g, x2 + 16, rq_y, 638, 70, fill=C["queue_bg"], stroke=C["orange"],
       title="RequestQueue  (asyncio.Queue, FIFO, 串行消费)")

# Animated queue items
for i in range(5):
    qx = x2 + 30 + i * 52
    svg_rect(g, qx, rq_y + 32, 42, 18, rx=4, fill=C["orange"], stroke="none")
    svg_text(g, qx + 21, rq_y + 46, f"R{i + 1}", size=8, fill="#0d1117",
             bold=True, anchor="middle")
svg_text(g, x2 + 320, rq_y + 46, "···", size=10, fill=C["muted"])

svg_text(g, x2 + 26, rq_y + 66, "同一时间只处理一个请求，完成后才取下一个", size=9, fill=C["muted"])

# --- _process() ---
pr_y = rq_y + 90
subbox(g, x2 + 16, pr_y, 638, 210, fill=C["queue_bg"], stroke=C["green"],
       title="_process() — asyncio.gather 并行执行")

bx, by = x2 + 36, pr_y + 34

# Left branch: TTS Original
subbox(g, bx, by, 290, 132, fill=C["dark_green"], stroke=C["green"],
       title="TTS(原文)")
svg_text(g, bx + 10, by + 22, "TTSService.synthesize()", size=9, fill=C["green"])
svg_text(g, bx + 10, by + 40, "EdgeTTS / MatchaTTS / CosyVoice / Sambert", size=8, fill=C["muted"])
svg_text(g, bx + 10, by + 102, "▶  audio_original  (.mp3 / .wav)", size=10, fill=C["accent"])

# gather label
gather_x = bx + 145
svg_text(g, gather_x, by + 40, "asyncio", size=12, fill=C["green"], bold=True, anchor="middle")
svg_text(g, gather_x, by + 56, ".gather()", size=12, fill=C["green"], bold=True, anchor="middle")
svg_text(g, gather_x, by + 72, "// 并行", size=9, fill=C["muted"], anchor="middle")

# Right branch: Translate + OSC
bx2 = bx + 310
subbox(g, bx2, by, 308, 132, fill=C["dark_purple"], stroke=C["purple"],
       title="[if translate] 翻译 + OSC + 译文TTS")

subbox(g, bx2 + 10, by + 22, 288, 20, fill="#0d1117", stroke="none", title="")
svg_text(g, bx2 + 16, by + 38, "1. TranslateService.translate()", size=9, fill=C["purple"])

subbox(g, bx2 + 10, by + 48, 288, 20, fill="#0d1117", stroke="none", title="")
svg_text(g, bx2 + 16, by + 64,
         "2. OSCService.send(原文 + \"\\n\" + 译文)", size=9, fill=C["purple"])

subbox(g, bx2 + 10, by + 74, 288, 20, fill="#0d1117", stroke="none", title="")
svg_text(g, bx2 + 16, by + 90, "3. [if playTranslation] TTS(译文)", size=9, fill=C["muted"])

svg_text(g, bx2 + 16, by + 115, "▶  audio_translated", size=10, fill=C["accent"])

# --- Push order ---
push_y = pr_y + 226
subbox(g, x2 + 16, push_y, 638, 54, fill=C["queue_bg"], stroke=C["accent"],
       title="按序 push 到 PlayQueue")
svg_text(g, x2 + 26, push_y + 36, "#1  audio_original", size=11, fill=C["accent"])
svg_text(g, x2 + 170, push_y + 36, "▶", size=11, fill=C["accent"])
svg_text(g, x2 + 190, push_y + 36, "#2  audio_translated", size=11, fill=C["muted"])
svg_text(g, x2 + 340, push_y + 36, "(如有，保证原文先于译文入队)", size=9, fill=C["muted"])

# --- PlayQueue ---
pq_y = push_y + 74
subbox(g, x2 + 16, pq_y, 638, 50, fill=C["queue_bg"], stroke=C["red"],
       title="PlayQueue  (asyncio.Queue, FIFO, 纯播放)")

# Animated queue items in playqueue
for i in range(6):
    qx = x2 + 30 + i * 52
    clr_item = C["accent"] if i % 2 == 0 else C["muted"]
    svg_rect(g, qx, pq_y + 26, 42, 16, rx=4, fill=clr_item, stroke="none")
    svg_text(g, qx + 21, pq_y + 38, ".mp3", size=7, fill="#0d1117",
             bold=True, anchor="middle")
svg_text(g, x2 + 370, pq_y + 38, "··· 不关心来源", size=9, fill=C["muted"])

# --- PlayWorker ---
pw_y = pq_y + 70
subbox(g, x2 + 16, pw_y, 638, 48, fill=C["dark_purple"], stroke=C["purple"],
       title="PlayWorker  (asyncio.Task) — miniaudio → 播完删除临时文件")
svg_text(g, x2 + 26, pw_y + 30, "原生 WAV / MP3 / OGG / FLAC · 无需 ffmpeg · asyncio.to_thread 避免阻塞",
         size=9, fill=C["muted"])

# --- Phase 2 preview ---
ph2_y = pw_y + 68
subbox(g, x2 + 16, ph2_y, 638, 44, fill=C["dark_purple"], stroke=C["red"],
       title="Phase 2: Voice Input Pipeline")
nodes = ["WS Audio Stream", "VAD (Silero)", "STT (SenseVoice)", "→ 文本送入 RequestQueue"]
nx = x2 + 26
for i, node in enumerate(nodes):
    clr_n = C["purple"] if i < 3 else C["orange"]
    svg_text(g, nx, ph2_y + 28, node, size=9, fill=clr_n)
    nx += 10 + len(node) * 8
    if i < len(nodes) - 1:
        svg_text(g, nx - 8, ph2_y + 28, "▸", size=8, fill=C["red"])

# ======================== ARROWS ========================
# Frontend → WebServer (HTTP)
arrow_right(g, x0 + 240, y0 + 180, x1 - 10, color=C["green"])
svg_text(g, x0 + 245, y0 + 172, "HTTP POST /tts", size=8, fill=C["green"])

# WebServer → Pipeline
arrow_right(g, x1 + 260, pr_y + 105, x2 - 5, color=C["accent"])
svg_text(g, x1 + 262, pr_y + 97, "submit_tts()", size=8, fill=C["accent"])

# WebSocket arrows (frontend ↔ webserver)
svg_line(g, x0 + 240, y0 + 140, x1 - 5, y0 + 112, stroke=C["green"], sw=1.5)
ET.SubElement(g, "polygon",
              points=f"{x1 - 5},{y0 + 112} {x1 - 13},{y0 + 107} {x1 - 13},{y0 + 117}",
              fill=C["green"])
svg_text(g, x0 + 245, y0 + 128, "audio(↑)", size=8, fill=C["green"])

svg_line(g, x1 - 5, y0 + 158, x0 + 240, y0 + 158, stroke=C["purple"], sw=1.5)
ET.SubElement(g, "polygon",
              points=f"{x0 + 240},{y0 + 158} {x0 + 248},{y0 + 153} {x0 + 248},{y0 + 163}",
              fill=C["purple"])
svg_text(g, x1 + 10, y0 + 150, "log/status(↓)", size=8, fill=C["purple"])

# Pipeline internal arrows
arrow_down(g, x2 + 335, rq_y + 70, pr_y - 4, color=C["orange"])
arrow_down(g, x2 + 335, pr_y + 210, push_y - 4, color=C["green"])
arrow_down(g, x2 + 335, push_y + 54, pq_y - 4, color=C["accent"])
arrow_down(g, x2 + 335, pq_y + 50, pw_y - 4, color=C["red"])

# OSC arrow (pipeline → VRChat)
# Draw from translate section to VRChat
svg_line(g, x2, y0 + 250, x0 + 240, y0 + 250, stroke=C["purple"], sw=1.5, dash="4,4")
ET.SubElement(g, "polygon",
              points=f"{x0 + 240},{y0 + 250} {x0 + 248},{y0 + 245} {x0 + 248},{y0 + 255}",
              fill=C["purple"])
svg_text(g, x0 + 245, y0 + 242, "OSC send", size=8, fill=C["purple"])

# ======================== LEGEND ========================
lx, ly = 50, 330
svg_text(g, lx, ly, "Legend", size=12, fill=C["text"], bold=True)
legend = [
    (C["green"],  "Frontend / TTS"),
    (C["accent"], "Core / Config"),
    (C["orange"], "Queue / Route"),
    (C["purple"], "OSC / External"),
    (C["red"],    "Async Workers"),
]
for i, (clr, label) in enumerate(legend):
    llx = lx + (i % 3) * 120
    lly = ly + 22 + (i // 3) * 24
    svg_rect(g, llx, lly - 6, 14, 14, rx=3, fill=clr, stroke="none")
    svg_text(g, llx + 20, lly + 6, label, size=10, fill=C["muted"])

# ======================== PHASE INDICATORS ========================
px0, py0 = 50, 700
phases = [
    ("Phase 1", C["green"], "TTS + Translate + OSC + Playback"),
    ("Phase 2", C["orange"], "STT + VAD + Voice Input Pipeline"),
    ("Phase 3", C["purple"], "HY-MT1.5 / Devices / Tests / Packaging"),
]
for i, (name, clr, desc) in enumerate(phases):
    py = py0 + i * 50
    svg_rect(g, px0, py, 12, 12, rx=3, fill=clr, stroke="none")
    svg_text(g, px0 + 20, py + 12, name, size=13, fill=clr, bold=True)
    svg_text(g, px0 + 90, py + 12, desc, size=10, fill=C["muted"])

# ======================== SAVE ========================
from pathlib import Path
out = Path(__file__).parent.parent / "docs" / "architecture.svg"
out.parent.mkdir(exist_ok=True)
tree = ET.ElementTree(svg)
tree.write(str(out), encoding="utf-8", xml_declaration=True)
print(f"Saved: {out}")
