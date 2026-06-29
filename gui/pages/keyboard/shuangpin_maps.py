"""双拼方案 → 26键按键提示映射表

每个方案的 dict: 字母键 → "声母_韵母" 格式的提示文本。
None 表示该方案不需要提示（全拼方案）。
所有键都显式标注声母和韵母，无歧义。

映射数据来源于 rime/_data/ 下各 schema.yaml 的 speller/algebra 规则。
"""

SHUANGPIN_HINT_MAPS: dict[str, dict[str, str] | None] = {
    # ═══════════════════════════════════════════════════════════
    # 小鹤双拼 (double_pinyin_flypy)
    # i=ch u=sh v=zh; a/e/o 为零声母
    # ═══════════════════════════════════════════════════════════
    "double_pinyin_flypy": {
        "q": "q_iu",   "w": "w_ei",   "e": "e_e",    "r": "r_uan",  "t": "t_ue",
        "y": "y_un",   "u": "sh_u",   "i": "ch_i",   "o": "o_uo",   "p": "p_ie",
        "a": "a_a",    "s": "s_ong",  "d": "d_ai",   "f": "f_en",   "g": "g_eng",
        "h": "h_ang",  "j": "j_an",   "k": "k_ing",  "l": "l_uang",
        "z": "z_ou",   "x": "x_ia",   "c": "c_ao",   "v": "zh_ui",  "b": "b_in",
        "n": "n_iao",  "m": "m_ian",
    },

    # ═══════════════════════════════════════════════════════════
    # 微软双拼 (double_pinyin_mspy)
    # i=ch u=sh v=zh; a/e/o 为零声母
    # ═══════════════════════════════════════════════════════════
    "double_pinyin_mspy": {
        "q": "q_iu",   "w": "w_ia",   "e": "e_e",    "r": "r_uan",  "t": "t_ue",
        "y": "y_uai",  "u": "sh_u",   "i": "ch_i",   "o": "o_uo",   "p": "p_un",
        "a": "a_a",    "s": "s_ong",  "d": "d_uang", "f": "f_en",   "g": "g_eng",
        "h": "h_ang",  "j": "j_an",   "k": "k_ao",   "l": "l_ai",
        "z": "z_ei",   "x": "x_ie",   "c": "c_iao",  "v": "zh_ui",  "b": "b_ou",
        "n": "n_in",   "m": "m_ian",
    },

    # ═══════════════════════════════════════════════════════════
    # 搜狗双拼 (double_pinyin_sogou) — 与微软双拼一致
    # ═══════════════════════════════════════════════════════════
    "double_pinyin_sogou": {
        "q": "q_iu",   "w": "w_ia",   "e": "e_e",    "r": "r_uan",  "t": "t_ue",
        "y": "y_uai",  "u": "sh_u",   "i": "ch_i",   "o": "o_uo",   "p": "p_un",
        "a": "a_a",    "s": "s_ong",  "d": "d_uang", "f": "f_en",   "g": "g_eng",
        "h": "h_ang",  "j": "j_an",   "k": "k_ao",   "l": "l_ai",
        "z": "z_ei",   "x": "x_ie",   "c": "c_iao",  "v": "zh_ui",  "b": "b_ou",
        "n": "n_in",   "m": "m_ian",
    },

    # ═══════════════════════════════════════════════════════════
    # 自然码双拼 (double_pinyin)
    # i=ch u=sh v=zh; a/e/o 为零声母; y=ing (与微软不同)
    # ═══════════════════════════════════════════════════════════
    "double_pinyin": {
        "q": "q_iu",   "w": "w_ia",   "e": "e_e",    "r": "r_uan",  "t": "t_ue",
        "y": "y_ing",  "u": "sh_u",   "i": "ch_i",   "o": "o_uo",   "p": "p_un",
        "a": "a_a",    "s": "s_ong",  "d": "d_uang", "f": "f_en",   "g": "g_eng",
        "h": "h_ang",  "j": "j_an",   "k": "k_ao",   "l": "l_ai",
        "z": "z_ei",   "x": "x_ie",   "c": "c_iao",  "v": "zh_ui",  "b": "b_ou",
        "n": "n_in",   "m": "m_ian",
    },

    # ═══════════════════════════════════════════════════════════
    # 智能ABC双拼 (double_pinyin_abc)
    # a=zh e=ch v=sh (与常规方案相反！); i/u 无初始角色
    # ═══════════════════════════════════════════════════════════
    "double_pinyin_abc": {
        "q": "q_ei",   "w": "w_ian",  "e": "ch_e",   "r": "r_iu",   "t": "t_uang",
        "y": "y_ing",  "u": "u_u",    "i": "i_i",    "o": "o_uo",   "p": "p_uan",
        "a": "zh_a",   "s": "s_ong",  "d": "d_ia",   "f": "f_en",   "g": "g_eng",
        "h": "h_ang",  "j": "j_an",   "k": "k_ao",   "l": "l_ai",
        "z": "z_iao",  "x": "x_ie",   "c": "c_in",   "v": "sh_v",   "b": "b_ou",
        "n": "n_un",   "m": "m_ui",
    },

    # ═══════════════════════════════════════════════════════════
    # 紫光双拼 (double_pinyin_ziguang)
    # a=ch u=zh i=sh; c 无韵母角色
    # ═══════════════════════════════════════════════════════════
    "double_pinyin_ziguang": {
        "q": "q_ao",   "w": "w_en",   "e": "e_e",    "r": "r_an",   "t": "t_eng",
        "y": "y_in",   "u": "zh_u",   "i": "sh_i",   "o": "o_uo",   "p": "p_ai",
        "a": "ch_a",   "s": "s_ang",  "d": "d_ie",   "f": "f_ian",  "g": "g_uang",
        "h": "h_ong",  "j": "j_iu",   "k": "k_ei",   "l": "l_uan",
        "z": "z_ou",   "x": "x_ia",   "c": "c_c",    "v": "v_v",    "b": "b_iao",
        "n": "n_ue",   "m": "m_un",
    },

    # ═══════════════════════════════════════════════════════════
    # 拼音加加双拼 (double_pinyin_jiajia)
    # u=ch i=sh v=zh; a/e/o 为零声母
    # ═══════════════════════════════════════════════════════════
    "double_pinyin_jiajia": {
        "q": "q_ing",  "w": "w_ei",   "e": "e_e",    "r": "r_en",   "t": "t_eng",
        "y": "y_ong",  "u": "ch_u",   "i": "sh_i",   "o": "o_uo",   "p": "p_ou",
        "a": "a_a",    "s": "s_ai",   "d": "d_ao",   "f": "f_an",   "g": "g_ang",
        "h": "h_uang", "j": "j_ian",  "k": "k_iao",  "l": "l_in",
        "z": "z_un",   "x": "x_uai",  "c": "c_uan",  "v": "zh_ui",  "b": "b_ia",
        "n": "n_iu",   "m": "m_ie",
    },

    # ═══════════════════════════════════════════════════════════
    # 五笔画 (stroke)
    # h=横 s=竖 p=撇 n=捺 z=折，其余键不参与
    # ═══════════════════════════════════════════════════════════
    "stroke": {
        "h": "h_横", "s": "s_竖", "p": "p_撇", "n": "n_捺", "z": "z_折",
    },

    # ── 全拼方案（不需要提示） ──
    "jyutping": None,        # 囧月拼音
    "terra_pinyin": None,     # 地球拼音
    "rime_melt": None,        # 雾凇拼音
}
