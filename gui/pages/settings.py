import asyncio
import logging
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QFrame,
    QComboBox, QLineEdit, QPushButton, QDoubleSpinBox,
    QSpinBox, QRadioButton, QButtonGroup, QProgressBar, QScrollArea,
    QGridLayout,
)
from gui.widgets.toggle import ToggleSwitch

logger = logging.getLogger(__name__)


def _label(text: str, style: str = "") -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet(style or "background: transparent;")
    return lbl


def _field_col(label_text: str, widget, save_callback=None) -> QVBoxLayout:
    col = QVBoxLayout()
    col.setSpacing(6)
    lbl = _label(label_text, "font-size: 12px; font-weight: 600; color: #9b9a98; background: transparent;")
    col.addWidget(lbl)
    if save_callback:
        row = QHBoxLayout()
        row.setSpacing(8)
        row.addWidget(widget)
        save_btn = QPushButton("保存")
        save_btn.setFixedHeight(32)
        save_btn.setStyleSheet(
            "QPushButton { border: 1px solid #d6608a; border-radius: 6px;"
            "background: rgba(214,96,138,0.1); color: #d6608a; font-size: 13px; font-weight: 500; padding: 0 12px; }"
            "QPushButton:hover { background: #d6608a; color: white; }"
        )
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(save_callback)
        row.addWidget(save_btn)
        col.addLayout(row)
    else:
        col.addWidget(widget)
    return col


def _desc_box(text: str) -> QLabel:
    lbl = _label(text)
    lbl.setWordWrap(True)
    lbl.setStyleSheet(
        "color: #6b6a68; font-size: 13px; padding: 12px 16px;"
        "background: #ffffff; border-radius: 10px; border-left: 3px solid #d6608a;"
    )
    return lbl


def _engine_tab_panel(
    desc: str,
    is_default: bool,
    on_set_default,
    fields: list,
) -> tuple[QWidget, ToggleSwitch]:
    """Build a single engine tab panel matching the Vue frontend layout."""
    panel = QWidget()
    layout = QVBoxLayout(panel)
    layout.setContentsMargins(0, 12, 0, 0)
    layout.setSpacing(20)

    if desc:
        layout.addWidget(_desc_box(desc))

    # "设为默认引擎" toggle row
    default_row = QHBoxLayout()
    default_row.setSpacing(12)
    default_label = _label("设为默认引擎", "font-size: 14px; color: #1a1a1a; background: transparent;")
    default_row.addWidget(default_label)
    default_row.addStretch()
    switch = ToggleSwitch(checked=is_default)
    def _on_switch(checked, sw=switch):
        if checked:
            on_set_default()
        else:
            sw.blockSignals(True)
            sw.setChecked(True)
            sw.blockSignals(False)
    switch.toggled.connect(_on_switch)
    default_row.addWidget(switch)
    layout.addLayout(default_row)

    # Dynamic fields
    for field in fields:
        layout.addLayout(field)

    layout.addStretch()
    return panel, switch


class SettingsPage(QWidget):
    def __init__(self, bridge, parent=None):
        super().__init__(parent)
        self.bridge = bridge
        self._tts_switches: dict[str, ToggleSwitch] = {}
        self._stt_switches: dict[str, ToggleSwitch] = {}
        self._translate_switches: dict[str, ToggleSwitch] = {}
        self._setup_ui()

    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        title = _label("设置", "font-size: 20px; font-weight: 700; color: #1a1a1a; background: transparent;")
        title.setObjectName("page_title")
        root.addWidget(title)

        self._tabs = QTabWidget()
        self._tabs.addTab(self._build_tts_tab(), "语音合成")
        self._tabs.addTab(self._build_stt_tab(), "语音识别")
        self._tabs.addTab(self._build_translate_tab(), "翻译")
        self._tabs.addTab(self._build_audio_tab(), "音频 & OSC")
        self._tabs.addTab(self._build_download_tab(), "模型下载")
        root.addWidget(self._tabs)

    # ---- TTS ----
    def _build_tts_tab(self) -> QWidget:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        container = QWidget()
        outer = QVBoxLayout(container)
        outer.setContentsMargins(0, 0, 8, 0)
        outer.setSpacing(0)

        cfg = self.bridge.get_config()
        providers = cfg.get("tts_provider", {}).get("providers", [])
        active = cfg.get("tts_provider", {}).get("provider", "edge_tts")
        voices_map = cfg.get("voices", {})

        engine_tabs = QTabWidget()
        for prov in providers:
            name = prov.get("name", "")
            if not isinstance(name, str) or not name:
                logger.warning("跳过无效 TTS provider: %r", prov)
                continue
            desc = prov.get("description", "")
            is_default = (name == active)
            voices = voices_map.get(name, [])

            fields = []

            # Voice combo
            voice_combo = QComboBox()
            voice_combo.setEditable(True)
            voice_combo.blockSignals(True)
            voice_combo.addItems(voices)
            current_voice = prov.get("voice", "")
            if current_voice:
                idx = voice_combo.findText(current_voice)
                if idx >= 0:
                    voice_combo.setCurrentIndex(idx)
                else:
                    voice_combo.setCurrentText(current_voice)
            voice_combo.blockSignals(False)
            voice_combo.currentTextChanged.connect(
                lambda v, n=name: self._update_tts_provider_field(n, "voice", v)
            )
            fields.append(_field_col("音色", voice_combo))

            # API Key for cosyvoice / sambert
            if name in ("cosyvoice", "sambert"):
                api_key_edit = QLineEdit()
                api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
                api_key_edit.setPlaceholderText("请输入 API Key")
                api_key_edit.setText(prov.get("ali_api_key", ""))
                fields.append(_field_col(
                    "阿里 API Key", api_key_edit,
                    lambda checked, n=name, w=api_key_edit: self._update_tts_provider_field(n, "ali_api_key", w.text(), reload=True)
                ))

            # MatchaTTS fields
            if name == "MatchaTTS":
                for key in ("acoustic_model", "vocoder", "tokens", "lexicon", "data_dir", "dict_dir"):
                    edit = QLineEdit()
                    edit.setPlaceholderText(f"请输入 {key}")
                    edit.setText(prov.get(f"matcha_{key}", ""))
                    fields.append(_field_col(
                        key, edit,
                        lambda checked, n=name, k=key, w=edit: self._update_tts_provider_field(n, f"matcha_{k}", w.text(), reload=True)
                    ))

            panel, switch = _engine_tab_panel(
                desc, is_default,
                lambda n=name: self._set_default_tts(n),
                fields,
            )
            self._tts_switches[name] = switch
            engine_tabs.addTab(panel, name)

        outer.addWidget(engine_tabs)
        scroll.setWidget(container)
        return scroll

    # ---- STT ----
    def _build_stt_tab(self) -> QWidget:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        container = QWidget()
        outer = QVBoxLayout(container)
        outer.setContentsMargins(0, 0, 8, 0)
        outer.setSpacing(0)

        cfg = self.bridge.get_config()
        providers = cfg.get("stt_provider", {}).get("providers", [])
        active = cfg.get("stt_provider", {}).get("provider", "")

        engine_tabs = QTabWidget()
        for prov in providers:
            name = prov.get("name", "")
            if not isinstance(name, str) or not name:
                logger.warning("跳过无效 STT provider: %r", prov)
                continue
            desc = prov.get("description", "")
            is_default = (name == active)
            fields = []

            model_fields = ["conv_frontend", "encoder", "decoder", "tokenizer"]
            has_model = any(prov.get(k) for k in model_fields)
            if has_model:
                for key in model_fields:
                    val = prov.get(key, "")
                    if val:
                        read_edit = QLineEdit(val)
                        read_edit.setReadOnly(True)
                        read_edit.setStyleSheet("color: #9b9a98;")
                        fields.append(_field_col(key, read_edit))

            panel, switch = _engine_tab_panel(
                desc, is_default,
                lambda n=name: self._set_default_stt(n),
                fields,
            )
            self._stt_switches[name] = switch
            engine_tabs.addTab(panel, name)

        # VAD settings as a separate tab
        vad_widget = self._build_vad_panel()
        engine_tabs.addTab(vad_widget, "VAD 参数")

        outer.addWidget(engine_tabs)
        scroll.setWidget(container)
        return scroll

    def _build_vad_panel(self) -> QWidget:
        cfg = self.bridge.get_config()
        vad = cfg.get("vad", {})

        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 12, 0, 0)
        layout.setSpacing(16)

        grid = QGridLayout()
        grid.setSpacing(12)
        vad_params = [
            ("Threshold", "threshold", 0, 1, 0.05, 0.5),
            ("Min Silence", "min_silence_duration", 0, 10, 0.05, 0.25),
            ("Min Speech", "min_speech_duration", 0, 10, 0.05, 0.25),
            ("Max Speech", "max_speech_duration", 0, 60, 0.5, 15.0),
        ]
        for i, (label, key, mn, mx, step, default) in enumerate(vad_params):
            vbox = QVBoxLayout()
            vbox.setSpacing(4)
            lbl = _label(label, "font-size: 14px; font-weight: 500; color: #1a1a1a; background: transparent;")
            vbox.addWidget(lbl)
            range_lbl = _label(
                f"{mn} — {mx}",
                "font-size: 11px; color: #9b9a98; font-family: 'Consolas', monospace; background: transparent;"
            )
            vbox.addWidget(range_lbl)
            spin = QDoubleSpinBox()
            spin.setRange(mn, mx)
            spin.setSingleStep(step)
            spin.setValue(vad.get(key, default))
            spin.valueChanged.connect(lambda v, k=key: self._on_vad_change(k, v))
            vbox.addWidget(spin)
            grid.addLayout(vbox, i // 2, i % 2)
        layout.addLayout(grid)
        layout.addStretch()
        return panel

    # ---- Translate ----
    def _build_translate_tab(self) -> QWidget:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        container = QWidget()
        outer = QVBoxLayout(container)
        outer.setContentsMargins(0, 0, 8, 0)
        outer.setSpacing(0)

        cfg = self.bridge.get_config()
        providers = cfg.get("translation_provider", {}).get("providers", [])
        active = cfg.get("translation_provider", {}).get("provider", "")

        engine_tabs = QTabWidget()
        for prov in providers:
            name = prov.get("name", "")
            if not isinstance(name, str) or not name:
                logger.warning("跳过无效翻译 provider: %r", prov)
                continue
            desc = prov.get("description", "")
            is_default = (name == active)
            fields = []

            if name == "openai":
                for field_key, field_label in [("api_key", "API Key"), ("url", "API URL"), ("model", "Model")]:
                    edit = QLineEdit()
                    edit.setPlaceholderText(f"请输入 {field_label}")
                    if field_key == "api_key":
                        edit.setEchoMode(QLineEdit.EchoMode.Password)
                    edit.setText(prov.get(field_key, ""))
                    fields.append(_field_col(
                        field_label, edit,
                        lambda checked, n=name, k=field_key, w=edit: self._update_translate_provider_field(n, k, w.text(), reload=True)
                    ))

            elif name == "hy_mt15":
                for field_key, field_label in [("server_url", "Server URL"), ("model_path", "Model Path"), ("llama_cpp_path", "Llama.cpp Path")]:
                    edit = QLineEdit()
                    edit.setPlaceholderText(f"请输入 {field_label}")
                    edit.setText(prov.get(field_key, ""))
                    fields.append(_field_col(
                        field_label, edit,
                        lambda checked, n=name, k=field_key, w=edit: self._update_translate_provider_field(n, k, w.text(), reload=True)
                    ))

            panel, switch = _engine_tab_panel(
                desc, is_default,
                lambda n=name: self._set_default_translate(n),
                fields,
            )
            self._translate_switches[name] = switch
            engine_tabs.addTab(panel, name)

        outer.addWidget(engine_tabs)
        scroll.setWidget(container)
        return scroll

    # ---- Audio & OSC ----
    def _build_audio_tab(self) -> QWidget:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 8, 0)
        layout.setSpacing(16)

        cfg = self.bridge.get_config()

        # Playback device
        dev_card = QFrame()
        dev_card.setObjectName("card")
        dev_card.setProperty("class", "card")
        dev_l = QVBoxLayout(dev_card)
        dev_l.setContentsMargins(20, 16, 20, 20)
        dev_l.setSpacing(12)
        dev_l.addWidget(_label("播放设备", "font-size: 15px; font-weight: 600; color: #1a1a1a; background: transparent;"))
        self._playback_combo = QComboBox()
        devices = self.bridge.get_playback_devices()
        for d in devices:
            self._playback_combo.addItem(d["name"])
        current_device = cfg.get("device", "")
        if current_device:
            idx = self._playback_combo.findText(current_device)
            if idx >= 0:
                self._playback_combo.setCurrentIndex(idx)
        self._playback_combo.currentTextChanged.connect(
            lambda v: self.bridge.update_config({"device": v})
        )
        dev_l.addWidget(self._playback_combo)
        layout.addWidget(dev_card)

        # Input device
        input_card = QFrame()
        input_card.setObjectName("card")
        input_card.setProperty("class", "card")
        input_l = QVBoxLayout(input_card)
        input_l.setContentsMargins(20, 16, 20, 20)
        input_l.setSpacing(12)
        input_l.addWidget(_label("输入设备（麦克风）", "font-size: 15px; font-weight: 600; color: #1a1a1a; background: transparent;"))
        self._input_combo = QComboBox()
        self._input_combo.setPlaceholderText("选择麦克风设备")
        self._refresh_input_devices()
        input_l.addWidget(self._input_combo)
        hint = _label("选择 GUI 录音使用的麦克风设备", "font-size: 13px; color: #9b9a98; background: transparent;")
        input_l.addWidget(hint)
        layout.addWidget(input_card)

        # Default behavior
        beh_card = QFrame()
        beh_card.setObjectName("card")
        beh_card.setProperty("class", "card")
        beh_l = QVBoxLayout(beh_card)
        beh_l.setContentsMargins(20, 16, 20, 20)
        beh_l.setSpacing(0)
        beh_l.addWidget(_label("默认行为", "font-size: 15px; font-weight: 600; color: #1a1a1a; background: transparent; padding-bottom: 8px;"))
        for label, key in [("播放音频", "isPlayAudio"), ("翻译", "isTranslate"), ("播放译文", "isPlayTranslation")]:
            row = QFrame()
            row.setProperty("class", "toggle_row")
            rlay = QHBoxLayout(row)
            rlay.setContentsMargins(0, 10, 0, 10)
            lbl = _label(label, "font-size: 14px; color: #1a1a1a; background: transparent;")
            rlay.addWidget(lbl)
            rlay.addStretch()
            toggle = ToggleSwitch(checked=cfg.get(key, True))
            toggle.toggled.connect(lambda checked, k=key: self.bridge.update_config({k: checked}))
            rlay.addWidget(toggle)
            beh_l.addWidget(row)
        layout.addWidget(beh_card)

        # OSC settings
        osc_card = QFrame()
        osc_card.setObjectName("card")
        osc_card.setProperty("class", "card")
        osc_l = QVBoxLayout(osc_card)
        osc_l.setContentsMargins(20, 16, 20, 20)
        osc_l.setSpacing(12)
        osc_l.addWidget(_label("OSC 设置", "font-size: 15px; font-weight: 600; color: #1a1a1a; background: transparent;"))
        osc_l.addWidget(_label("启用 OSC", "font-size: 14px; color: #1a1a1a; background: transparent;"))
        osc_toggle = ToggleSwitch(checked=cfg.get("osc_enabled", True))
        osc_toggle.toggled.connect(lambda checked: self.bridge.update_config({"osc_enabled": checked}))
        osc_l.addWidget(osc_toggle)

        osc_host_edit = QLineEdit(cfg.get("osc_host", "127.0.0.1"))
        osc_l.addLayout(_field_col("OSC Host", osc_host_edit, lambda: self.bridge.update_config({"osc_host": osc_host_edit.text()})))
        osc_port_spin = QSpinBox()
        osc_port_spin.setRange(1, 65535)
        osc_port_spin.setValue(cfg.get("osc_port", 9000))
        osc_l.addLayout(_field_col("OSC Port", osc_port_spin, lambda: self.bridge.update_config({"osc_port": osc_port_spin.value()})))
        layout.addWidget(osc_card)

        layout.addStretch()
        scroll.setWidget(container)
        return scroll

    # ---- Model Download ----
    def _build_download_tab(self) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        src_card = QFrame()
        src_card.setObjectName("card")
        src_card.setProperty("class", "card")
        src_l = QVBoxLayout(src_card)
        src_l.setContentsMargins(20, 16, 20, 20)
        src_l.setSpacing(12)
        src_l.addWidget(_label("下载源", "font-size: 15px; font-weight: 600; color: #1a1a1a; background: transparent;"))
        self._download_source_group = QButtonGroup(self)
        sources = [
            ("huggingface", "HuggingFace 官方源"),
            ("huggingface_mirror", "HuggingFace 镜像源（国内推荐）"),
            ("modelscope", "ModelScope 源（国内推荐）"),
        ]
        for i, (val, label) in enumerate(sources):
            rb = QRadioButton(label)
            rb.setStyleSheet("font-size: 14px; color: #1a1a1a; spacing: 8px; background: transparent;")
            self._download_source_group.addButton(rb, i)
            if val == "huggingface_mirror":
                rb.setChecked(True)
            src_l.addWidget(rb)
        layout.addWidget(src_card)

        self._download_btn = QPushButton("开始下载")
        self._download_btn.setObjectName("primary_btn")
        self._download_btn.setFixedHeight(48)
        self._download_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._download_btn.clicked.connect(self._on_download)
        layout.addWidget(self._download_btn)

        self._engines_card = QFrame()
        self._engines_card.setObjectName("card")
        self._engines_card.setProperty("class", "card")
        self._engines_l = QVBoxLayout(self._engines_card)
        self._engines_l.setContentsMargins(20, 16, 20, 20)
        self._engines_l.setSpacing(12)
        self._engines_l.addWidget(_label("引擎状态", "font-size: 15px; font-weight: 600; color: #1a1a1a; background: transparent;"))
        self._engines_container = QVBoxLayout()
        self._engines_l.addLayout(self._engines_container)
        self._loading_label = _label("加载中...", "text-align: center; color: #9b9a98; font-size: 13px; background: transparent;")
        self._engines_l.addWidget(self._loading_label)
        layout.addWidget(self._engines_card)

        layout.addStretch()
        return container

    # ---- Helpers ----
    def _refresh_input_devices(self):
        from PySide6.QtMultimedia import QMediaDevices
        devices = QMediaDevices.audioInputs()
        self._input_combo.clear()
        for d in devices:
            self._input_combo.addItem(d.description())
        cfg = self.bridge.get_config()
        saved = cfg.get("gui_input_device", "")
        if saved:
            idx = self._input_combo.findText(saved)
            if idx >= 0:
                self._input_combo.setCurrentIndex(idx)
        self._input_combo.currentTextChanged.connect(
            lambda v: self.bridge.update_config({"gui_input_device": v})
        )

    def _set_default_tts(self, name: str):
        for n, sw in self._tts_switches.items():
            sw.blockSignals(True)
            sw.setChecked(n == name)
            sw.blockSignals(False)
        self.bridge.update_config({"tts_provider": {"provider": name}})

    def _set_default_stt(self, name: str):
        for n, sw in self._stt_switches.items():
            sw.blockSignals(True)
            sw.setChecked(n == name)
            sw.blockSignals(False)
        self.bridge.update_config({"stt_provider": {"provider": name}})

    def _set_default_translate(self, name: str):
        for n, sw in self._translate_switches.items():
            sw.blockSignals(True)
            sw.setChecked(n == name)
            sw.blockSignals(False)
        self.bridge.update_config({"translation_provider": {"provider": name}})
        self._reload_async()

    def _update_tts_provider_field(self, provider_name: str, key: str, value, reload: bool = False):
        if not isinstance(provider_name, str) or not provider_name:
            logger.error("无效的 TTS provider_name: %r, 跳过保存", provider_name)
            return
        cfg = self.bridge.get_config()
        providers = list(cfg.get("tts_provider", {}).get("providers", []))
        matched = False
        for p in providers:
            if p.get("name") == provider_name:
                p[key] = value
                matched = True
                break
        if not matched:
            logger.error("TTS provider '%s' 未找到, providers: %s", provider_name, [p.get("name") for p in providers])
            return
        ok = self.bridge.update_config({"tts_provider": {"providers": providers}})
        logger.info("保存 TTS [%s].%s = %r → %s", provider_name, key, value, "成功" if ok else "失败")
        if reload:
            self._reload_async()

    def _update_translate_provider_field(self, provider_name: str, key: str, value, reload: bool = False):
        if not isinstance(provider_name, str) or not provider_name:
            logger.error("无效的 Translate provider_name: %r, 跳过保存", provider_name)
            return
        cfg = self.bridge.get_config()
        providers = list(cfg.get("translation_provider", {}).get("providers", []))
        matched = False
        for p in providers:
            if p.get("name") == provider_name:
                p[key] = value
                matched = True
                break
        if not matched:
            logger.error("Translate provider '%s' 未找到, providers: %s", provider_name, [p.get("name") for p in providers])
            return
        ok = self.bridge.update_config({"translation_provider": {"providers": providers}})
        logger.info("保存 Translate [%s].%s = %r → %s", provider_name, key, value, "成功" if ok else "失败")
        if reload:
            self._reload_async()

    def _on_vad_change(self, key: str, value: float):
        cfg = self.bridge.get_config()
        vad = dict(cfg.get("vad", {}))
        vad[key] = value
        self.bridge.update_config({"vad": vad})

    def _reload_async(self):
        try:
            asyncio.create_task(self.bridge.reload_engines())
        except RuntimeError:
            pass

    def _on_download(self):
        btn_id = self._download_source_group.checkedId()
        source_map = {0: "huggingface", 1: "huggingface_mirror", 2: "modelscope"}
        source = source_map.get(btn_id, "huggingface_mirror")
        self._download_btn.setEnabled(False)
        self._download_btn.setText("下载中...")

        async def _do_download():
            try:
                ok, fail = await self.bridge.download_models(source)
                self._download_btn.setEnabled(True)
                self._download_btn.setText("开始下载")
            except Exception as e:
                logger.error("下载失败: %s", e)
                self._download_btn.setEnabled(True)
                self._download_btn.setText("开始下载")

        asyncio.create_task(_do_download())

    def refresh_models_status(self):
        from scripts.download_models import get_model_status
        try:
            engines = get_model_status()
        except Exception:
            engines = []

        while self._engines_container.count():
            item = self._engines_container.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()
        self._loading_label.hide()

        for e in engines:
            engine = e.get("engine", "")
            total = e.get("total", 0)
            ok = e.get("ok", 0)
            pct = round(ok / total * 100) if total > 0 else 0

            row = QVBoxLayout()
            row.setSpacing(6)
            info = QHBoxLayout()
            name_lbl = _label(engine, "font-size: 14px; font-weight: 500; color: #1a1a1a; background: transparent;")
            info.addWidget(name_lbl)
            info.addStretch()
            count_lbl = _label(
                f"{ok} / {total}",
                "font-family: 'Consolas', monospace; font-size: 13px; color: #6b6a68; background: transparent;"
            )
            info.addWidget(count_lbl)
            row.addLayout(info)

            bar = QProgressBar()
            bar.setRange(0, 100)
            bar.setValue(pct)
            bar.setFixedHeight(6)
            if pct == 100:
                bar.setStyleSheet("QProgressBar::chunk { background: #3da85c; border-radius: 3px; }")
            elif pct > 0:
                bar.setStyleSheet("QProgressBar::chunk { background: #d6608a; border-radius: 3px; }")
            else:
                bar.setStyleSheet("QProgressBar::chunk { background: #9b9a98; border-radius: 3px; }")
            row.addWidget(bar)
            self._engines_container.addLayout(row)
