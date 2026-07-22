# -*- coding: utf-8 -*-
"""
PVD Design Studio
==================
โปรแกรมออกแบบ Prefabricated Vertical Drains (PVD)
ตามทฤษฎีของ Barron (1948), Terzaghi และ Carillo (1942)

วิธีรัน:
    pip install streamlit numpy pandas plotly
    streamlit run pvd_design_app.py
"""

import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="PVD Design Studio",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUTE MASCOT (original, hand-drawn SVG — engineering & soil themed)
# ============================================================
def mascot_svg(kind="engineer", size=110):
    """
    Returns an inline SVG of a simple, original cute mascot themed around
    civil engineering / geotechnical work — drawn in a blocky, angular
    (low-poly) cute style.
    kind: 'engineer' | 'soil' | 'drain' | 'surveyor'
    """
    eye_color = "#2E2E38"

    if kind == "engineer":
        # blocky engineer face with a square-ish hard hat + angular vest collar
        skin = "#FFDCB0"
        hat = "#FFC93C"
        hat_shade = "#E8A800"
        vest = "#FF7A3D"
        svg = f'''
        <svg width="{size}" height="{size}" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
            <!-- vest collar (angular) -->
            <polygon points="24,110 60,120 96,110 88,92 60,100 32,92" fill="{vest}"/>
            <rect x="53" y="90" width="14" height="20" fill="#ffffff40"/>
            <!-- face: blocky octagon -->
            <polygon points="34,20 86,20 100,34 100,86 86,100 34,100 20,86 20,34"
                     fill="{skin}"/>
            <!-- hard hat: angular dome + brim -->
            <polygon points="18,46 60,10 102,46" fill="{hat}"/>
            <rect x="14" y="42" width="92" height="12" fill="{hat_shade}"/>
            <rect x="54" y="16" width="12" height="10" fill="{hat_shade}"/>
            <!-- eyes: squares -->
            <rect x="38" y="54" width="12" height="12" fill="{eye_color}"/>
            <rect x="70" y="54" width="12" height="12" fill="{eye_color}"/>
            <rect x="41" y="57" width="4" height="4" fill="white"/>
            <rect x="73" y="57" width="4" height="4" fill="white"/>
            <!-- blush -->
            <polygon points="24,72 36,72 32,82 22,82" fill="#FF9E80" opacity="0.6"/>
            <polygon points="84,72 96,72 98,82 88,82" fill="#FF9E80" opacity="0.6"/>
            <!-- mouth: angular smile -->
            <polyline points="44,80 60,90 76,80" fill="none" stroke="{eye_color}"
                      stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        '''

    elif kind == "soil":
        # blocky layered soil hexagon with a low-poly sprout
        soil1 = "#C08552"
        soil2 = "#A9683A"
        soil3 = "#8B5E34"
        sprout = "#5FBE72"
        svg = f'''
        <svg width="{size}" height="{size}" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
            <!-- sprout leaves (triangles) -->
            <polygon points="60,22 40,8 46,26" fill="{sprout}"/>
            <polygon points="60,22 80,6 76,26" fill="{sprout}"/>
            <rect x="56" y="16" width="8" height="14" fill="#3E8E52"/>
            <!-- hexagonal soil block, layered -->
            <polygon points="60,26 96,44 96,84 60,102 24,84 24,44" fill="{soil1}"/>
            <polygon points="24,68 96,68 96,84 60,102 24,84" fill="{soil2}"/>
            <polygon points="24,84 60,102 96,84 96,92 60,110 24,92" fill="{soil3}"/>
            <!-- eyes: squares -->
            <rect x="42" y="54" width="12" height="12" fill="{eye_color}"/>
            <rect x="66" y="54" width="12" height="12" fill="{eye_color}"/>
            <rect x="45" y="57" width="4" height="4" fill="white"/>
            <rect x="69" y="57" width="4" height="4" fill="white"/>
            <!-- blush -->
            <polygon points="30,66 40,66 37,74 28,74" fill="#FFD9A0" opacity="0.8"/>
            <polygon points="80,66 90,66 92,74 83,74" fill="#FFD9A0" opacity="0.8"/>
            <!-- mouth -->
            <polyline points="48,72 60,80 72,72" fill="none" stroke="{eye_color}"
                      stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        '''

    elif kind == "drain":
        # blocky PVD strip-drain character (angular core + geotextile stripes)
        body = "#4FC3E8"
        body_shade = "#3AA9CC"
        stripe = "#E8F8FF"
        svg = f'''
        <svg width="{size}" height="{size}" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
            <!-- flat drain body: blocky panel with cut corners -->
            <polygon points="34,14 86,14 96,24 96,100 86,110 34,110 24,100 24,24" fill="{body}"/>
            <polygon points="24,24 34,14 34,110 24,100" fill="{body_shade}"/>
            <rect x="42" y="24" width="7" height="76" fill="{stripe}" opacity="0.9"/>
            <rect x="54" y="24" width="7" height="76" fill="{stripe}" opacity="0.9"/>
            <rect x="66" y="24" width="7" height="76" fill="{stripe}" opacity="0.9"/>
            <rect x="78" y="24" width="7" height="76" fill="{stripe}" opacity="0.9"/>
            <!-- face -->
            <rect x="42" y="50" width="11" height="11" fill="{eye_color}"/>
            <rect x="67" y="50" width="11" height="11" fill="{eye_color}"/>
            <rect x="45" y="53" width="4" height="4" fill="white"/>
            <rect x="70" y="53" width="4" height="4" fill="white"/>
            <polygon points="36,64 46,64 43,72 34,72" fill="#FFAFCF" opacity="0.8"/>
            <polygon points="74,64 84,64 86,72 77,72" fill="#FFAFCF" opacity="0.8"/>
            <polyline points="48,66 60,74 72,66" fill="none" stroke="{eye_color}"
                      stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        '''

    else:  # "surveyor" — blocky character with hard hat + angular clipboard
        skin = "#FFDCB0"
        hat = "#3DDC97"
        hat_shade = "#26A876"
        svg = f'''
        <svg width="{size}" height="{size}" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
            <polygon points="34,20 86,20 100,34 100,86 86,100 34,100 20,86 20,34"
                     fill="{skin}"/>
            <polygon points="18,46 60,10 102,46" fill="{hat}"/>
            <rect x="14" y="42" width="92" height="12" fill="{hat_shade}"/>
            <!-- clipboard (angular) -->
            <rect x="80" y="66" width="28" height="34" fill="#ffffff" stroke="{hat_shade}" stroke-width="4"/>
            <rect x="86" y="76" width="16" height="4" fill="{hat_shade}"/>
            <rect x="86" y="84" width="16" height="4" fill="{hat_shade}"/>
            <rect x="86" y="92" width="10" height="4" fill="{hat_shade}"/>
            <rect x="38" y="54" width="12" height="12" fill="{eye_color}"/>
            <rect x="70" y="54" width="12" height="12" fill="{eye_color}"/>
            <rect x="41" y="57" width="4" height="4" fill="white"/>
            <rect x="73" y="57" width="4" height="4" fill="white"/>
            <polygon points="24,72 36,72 32,82 22,82" fill="#FF9E80" opacity="0.6"/>
            <polyline points="44,80 60,90 76,80" fill="none" stroke="{eye_color}"
                      stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        '''
    return svg


def mascot_bubble(kind, message, size=64, align="left"):
    """Renders a cute mascot next to a speech-bubble message."""
    svg = mascot_svg(kind, size)
    direction = "row" if align == "left" else "row-reverse"
    radius = "6px 18px 18px 18px" if align == "left" else "18px 6px 18px 18px"
    st.markdown(f"""
    <div style="display:flex; flex-direction:{direction}; align-items:center; gap:10px; margin:10px 0;">
        <div style="flex-shrink:0;">{svg}</div>
        <div style="background:#FFFCF6; border-radius:{radius}; padding:10px 16px;
                    box-shadow:0 4px 14px rgba(107,66,38,0.12); font-size:0.92rem; color:#4A3624;
                    border:1px solid rgba(139,94,52,0.16);">
            {message}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# CUSTOM CSS — THEME
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Kanit', sans-serif;
}

/* App background — warm sand / paper tone */
.stApp {
    background: linear-gradient(180deg, #FBF6EC 0%, #F3E7D3 100%);
}

/* Hero header — soil strata gradient: bark brown → clay terracotta → moss green */
.hero {
    background: linear-gradient(120deg, #6B4226 0%, #BF6B4D 48%, #7C9459 100%);
    padding: 2.2rem 2.4rem;
    border-radius: 22px;
    color: #FFF9F0;
    margin-bottom: 1.6rem;
    box-shadow: 0 12px 30px rgba(107, 66, 38, 0.30);
}
.hero h1 {
    font-size: 2.1rem;
    font-weight: 700;
    margin: 0 0 0.3rem 0;
}
.hero p {
    font-size: 1.02rem;
    opacity: 0.94;
    margin: 0;
}
.hero .badge {
    display: inline-block;
    background: rgba(255,249,240,0.25);
    padding: 4px 14px;
    border-radius: 999px;
    font-size: 0.8rem;
    margin-bottom: 10px;
    letter-spacing: 0.5px;
}

/* Section header pill (mimics slide title bars) — earthy palette */
.section-pill {
    display: inline-block;
    padding: 8px 22px;
    border-radius: 14px;
    font-weight: 600;
    font-size: 1.05rem;
    color: #FFF9F0;
    margin-bottom: 14px;
}
.pill-purple  { background: linear-gradient(90deg,#8B5E34,#B98B4E); }   /* clay / earth brown */
.pill-orange  { background: linear-gradient(90deg,#D9834F,#E8B84B); }   /* terracotta / ochre */
.pill-green   { background: linear-gradient(90deg,#6E8B3D,#A3B565); }   /* moss / sprout green */
.pill-pink    { background: linear-gradient(90deg,#C1694F,#E8A87C); }   /* rust clay */
.pill-blue    { background: linear-gradient(90deg,#4A7C6F,#8FA694); }   /* slate / groundwater teal */

/* Metric cards */
.metric-card {
    background: #FFFCF6;
    border-radius: 18px;
    padding: 1.1rem 1.3rem;
    box-shadow: 0 6px 18px rgba(107,66,38,0.10);
    border: 1px solid rgba(139,94,52,0.14);
    height: 100%;
}
.metric-card .label {
    font-size: 0.82rem;
    color: #8A7458;
    font-weight: 500;
    margin-bottom: 4px;
}
.metric-card .value {
    font-size: 1.6rem;
    font-weight: 700;
    color: #4A2E1E;
}
.metric-card .sub {
    font-size: 0.78rem;
    color: #A08A6E;
    margin-top: 2px;
}

.ok-tag {
    display:inline-block; padding: 3px 12px; border-radius: 999px;
    font-size: 0.82rem; font-weight:600;
    background:#DCE9C8; color:#4C6B23;
}
.warn-tag {
    display:inline-block; padding: 3px 12px; border-radius: 999px;
    font-size: 0.82rem; font-weight:600;
    background:#F5E1B8; color:#8A5A00;
}
.bad-tag {
    display:inline-block; padding: 3px 12px; border-radius: 999px;
    font-size: 0.82rem; font-weight:600;
    background:#F3D4C4; color:#8B3A1E;
}

/* Sidebar — deep soil earth tone */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #3E2A1E 0%, #4E3524 100%);
}
section[data-testid="stSidebar"] * {
    color: #F3E9DA !important;
}
section[data-testid="stSidebar"] .stSlider label, 
section[data-testid="stSidebar"] .stNumberInput label,
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stRadio label {
    color: #E3C9A3 !important;
    font-weight: 500;
}

.footer-note {
    text-align:center; color:#A08A6E; font-size:0.8rem; margin-top: 2.5rem;
    padding-top: 1rem; border-top: 1px solid #E3D4BC;
}

div[data-testid="stMetricValue"] { color:#4A2E1E; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HERO HEADER
# ============================================================
st.markdown(f"""
_hero_mascot = mascot_svg("engineer",92)
<div class="hero" style="position:relative; overflow:visible;">
    <div class="badge">GROUND IMPROVEMENT • GEOTECHNICAL DESIGN TOOL</div>
    <h1>🧊 PVD Design Studio</h1>
    <p>โปรแกรมออกแบบท่อระบายน้ำแนวดิ่งสำเร็จรูป (Prefabricated Vertical Drains)
    ตามวิธีของ Barron (1948) • Terzaghi • Carillo (1942)</p>
    <div style="position:absolute; top:-14px; right:22px; background:#FFFCF6; border-radius:16px;
                padding:6px; box-shadow:0 8px 20px rgba(107,66,38,0.30); transform: rotate(-3deg);">
        {_hero_mascot}
    </div>
</div>
""", unsafe_allow_html=True)

mascot_bubble("engineer", "สวัสดีครับ! 👷‍♂️ ผมวิศวกรผู้ช่วย กรอกพารามิเตอร์ทางซ้ายมือ แล้วมาออกแบบ PVD กันเลย!", size=58)


# ============================================================
# CORE ENGINEERING FUNCTIONS
# ============================================================
def dw_hansbo(a, b):
    """Equivalent diameter of PVD (flat drain) - Hansbo method, cm"""
    return 2.0 * (a + b) / np.pi


def dw_rixner(a, b):
    """Equivalent diameter of PVD - Rixner method, cm"""
    return (a + b) / 2.0


def de_from_spacing(S_m, pattern):
    """Effective diameter of drainage zone (m) from spacing S (m)"""
    S_cm = S_m * 100.0
    if pattern == "สี่เหลี่ยม (Square)":
        return 1.13 * S_cm
    else:
        return 1.05 * S_cm


def Fn_barron(n):
    """Drain spacing factor F(n) - Barron (1948), no smear effect"""
    n2 = n ** 2
    return (n2 / (n2 - 1.0)) * np.log(n) - (3 * n2 - 1) / (4 * n2)


def Ur_barron(Tr, Fn):
    return 1 - np.exp(-8 * Tr / Fn)


def Tv_from_Uv(Uv):
    """Time factor Tv from Uv (Terzaghi), valid for Uv <= 60% (Atkinson & Eldred 1981)"""
    return (np.pi / 4.0) * (Uv ** 2)


def Uv_from_Tv(Tv):
    """Degree of consolidation Uv from Tv, Uv <= 60% relation"""
    Uv = np.sqrt(4 * Tv / np.pi)
    return min(Uv, 1.0)


def Uav_carillo(Ur, Uv):
    return 1 - (1 - Ur) * (1 - Uv)


def resistance_index_L(n, H_cm, Hm_cm, kc, km, B_cm, dw_cm):
    """Resistance index of sand mat, L (Barron / Hansbo-type formula from slide 30)"""
    return (32 / np.pi**2) * (1.0 / n**2) * (H_cm / Hm_cm) * (kc / km) * (B_cm / dw_cm) ** 2


def final_settlement(H_cm, Cc, e0, sigma0, dsigma):
    """Ultimate primary consolidation settlement, cm"""
    return H_cm * (Cc / (1 + e0)) * np.log10((sigma0 + dsigma) / sigma0)


# ============================================================
# SIDEBAR — INPUT PARAMETERS
# ============================================================
with st.sidebar:
    st.markdown(f"""
        <div style="color:#E3C9A3; font-size:0.82rem; margin-top:4px;">น้องดินอ่อน ผู้ช่วยออกแบบ 🌱</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("## ⚙️ พารามิเตอร์ออกแบบ")

    st.markdown("### 🧱 ชั้นดิน (Soil Layer)")
    H = st.number_input("ความหนาชั้นดินเหนียวอ่อน, H (m)", 1.0, 100.0, 12.0, 0.5)
    drainage_cond = st.radio("เงื่อนไขการระบายน้ำ (แนวดิ่ง)", ["ระบายสองทาง (Double)", "ระบายทางเดียว (Single)"], index=0)
    Cv = st.number_input("สปส. การอัดตัวคายน้ำแนวดิ่ง, Cv (cm²/day)", 0.1, 500.0, 20.0, 0.1)
    kr_kv = st.number_input("อัตราส่วน kr/kv", 1.0, 20.0, 7.0, 0.5,
                             help="ค่าที่ใช้ทั่วไปในกรุงเทพ ~4-10 (Bergado et al., 1992)")

    st.markdown("### 📐 แผ่นระบายน้ำ (PVD)")
    pvd_a = st.number_input("ความกว้าง a (mm)", 50.0, 200.0, 100.0, 1.0)
    pvd_b = st.number_input("ความหนา b (mm)", 2.0, 15.0, 5.0, 0.5)
    dw_method = st.selectbox("วิธีคำนวณ dw", ["Hansbo", "Rixner"])
    smear_extra_cm = st.number_input("เพิ่มผลกระทบ Smear (เพิ่ม dw, cm) — ใช้ตามแนวปฏิบัติ", 0.0, 10.0, 0.0, 0.5,
                                      help="ในทางปฏิบัติมักใช้ dw ~5 cm เนื่องจาก shrinkage ของหน้าตัด PVD")

    st.markdown("### 🔺 รูปแบบการติดตั้ง")
    pattern = st.selectbox("รูปแบบ (Pattern)", ["สี่เหลี่ยม (Square)", "สามเหลี่ยม (Triangular)"], index=1)
    S = st.slider("ระยะห่างระหว่างท่อ PVD, S (m)", 0.6, 2.0, 1.0, 0.05)

    st.markdown("### ⏱️ เป้าหมายการออกแบบ")
    t_design = st.number_input("ระยะเวลาที่ต้องการ, t (วัน)", 1, 2000, 90, 1)
    U_target = st.slider("ระดับการอัดตัวเป้าหมาย, U_target (%)", 50, 99, 90, 1)

    st.markdown("### 🏗️ การทรุดตัว (Settlement)")
    Cc = st.number_input("Compression Index, Cc", 0.01, 5.0, 0.29, 0.01)
    e0 = st.number_input("Void Ratio เริ่มต้น, e0", 0.1, 5.0, 1.10, 0.01)
    sigma0 = st.number_input("Effective Overburden Stress เดิม, σ'0 (kN/m²)", 1.0, 500.0, 40.0, 1.0)
    dsigma = st.number_input("ความดันเพิ่มขึ้นจาก Preload, Δσ (kN/m²)", 0.0, 500.0, 80.0, 1.0)

    st.markdown("### 🏖️ ชั้นทรายรอง (Sand Mat)")
    check_sandmat = st.checkbox("ตรวจสอบ Sand Mat", value=True)
    if check_sandmat:
        Hm = st.number_input("ความหนา Sand Mat, Hm (cm)", 30.0, 200.0, 50.0, 5.0)
        B_full = st.number_input("ความกว้างเต็มของพื้นที่ถม/สนาม, 2B (m)", 1.0, 500.0, 80.0, 1.0)
        km = st.number_input("สปส. การซึมน้ำของทราย, km (cm/s)", 1e-5, 1.0, 1e-3, format="%.1e")
        kc = st.number_input("สปส. การซึมน้ำของดินเหนียว, kc (cm/s)", 1e-9, 1.0, 1e-7, format="%.1e")


# ============================================================
# CALCULATIONS
# ============================================================
# --- dw ---
if dw_method == "Hansbo":
    dw = dw_hansbo(pvd_a / 10.0, pvd_b / 10.0)  # mm -> cm inside function expects same units; a,b in cm
else:
    dw = dw_rixner(pvd_a / 10.0, pvd_b / 10.0)
dw += smear_extra_cm
dw = max(dw, 0.1)

# --- de, n, F(n) ---
de = de_from_spacing(S, pattern)     # cm
n = de / dw
Fn = Fn_barron(n)

# --- Cr, Tr, Ur ---
Cr = kr_kv * Cv
Tr = (Cr * t_design) / (de ** 2)
Ur = Ur_barron(Tr, Fn)

# --- Hd, Tv, Uv ---
Hd_m = H / 2.0 if drainage_cond.startswith("ระบายสองทาง") else H
Hd_cm = Hd_m * 100.0
Tv = (Cv * t_design) / (Hd_cm ** 2)
Uv = Uv_from_Tv(Tv) if Tv <= (np.pi / 4 * 0.6 ** 2) else min(1 - (8/np.pi**2)*np.exp(-(np.pi**2/4)*Tv), 1.0)

# --- Combined Uav (Carillo) ---
Uav = Uav_carillo(Ur, Uv)

# --- Settlement ---
Sfinal_cm = final_settlement(H * 100.0, Cc, e0, sigma0, dsigma)
St_cm = Uav * Sfinal_cm

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📊 สรุปผลออกแบบ", "🌀 Barron & Terzaghi", "📈 กราฟ U-t", "🏗️ การทรุดตัว", "🏖️ Sand Mat"]
)

# ------------------------------------------------------------
# TAB 1: SUMMARY
# ------------------------------------------------------------
with tab1:
    st.markdown('<div class="section-pill pill-purple">🎯 ผลการออกแบบโดยสรุป</div>', unsafe_allow_html=True)

    status_ok = Uav * 100 >= U_target
    status_html = (
        '<span class="ok-tag">✔ ผ่านเกณฑ์เป้าหมาย</span>' if status_ok
        else '<span class="bad-tag">✘ ยังไม่ผ่านเกณฑ์ — ลดระยะห่าง S</span>'
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-card">
            <div class="label">ระดับการอัดตัวรวม (Uav)</div>
            <div class="value">{Uav*100:.2f}%</div>
            <div class="sub">ที่เวลา {t_design} วัน</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card">
            <div class="label">Ur (แนวรัศมี, Barron)</div>
            <div class="value">{Ur*100:.2f}%</div>
            <div class="sub">S = {S:.2f} m</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card">
            <div class="label">Uv (แนวดิ่ง, Terzaghi)</div>
            <div class="value">{Uv*100:.2f}%</div>
            <div class="sub">Hd = {Hd_m:.2f} m</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="metric-card">
            <div class="label">การทรุดตัว ณ เวลา t</div>
            <div class="value">{St_cm:.1f} cm</div>
            <div class="sub">จากสูงสุด {Sfinal_cm:.1f} cm</div>
        </div>""", unsafe_allow_html=True)

    st.write("")
    st.markdown(f"**สถานะการออกแบบเทียบเป้าหมาย {U_target}%:** {status_html}", unsafe_allow_html=True)

    if status_ok:
        mascot_bubble("drain", f"เย้! 🎉 ระยะห่าง S = {S:.2f} m ให้ Uav = {Uav*100:.1f}% ผ่านเป้าหมายแล้วครับ เก่งมาก!", size=58)
    else:
        mascot_bubble("engineer", f"อุ๊ปส์ 👷 ตอนนี้ได้แค่ {Uav*100:.1f}% ยังไม่ถึง {U_target}% ลองลดระยะห่าง S ดูนะครับ", size=58)

    st.write("")
    colA, colB = st.columns([1.1, 1])
    with colA:
        st.markdown('<div class="section-pill pill-green">📐 พารามิเตอร์เรขาคณิต</div>', unsafe_allow_html=True)
        geo_df = pd.DataFrame({
            "พารามิเตอร์": ["dw (เส้นผ่านศูนย์กลางสมมูล PVD)", "de (เส้นผ่านศูนย์กลางบริเวณระบายน้ำ)",
                             "n = de/dw", "F(n) — Drain spacing factor", "รูปแบบติดตั้ง", "ระยะห่าง S"],
            "ค่า": [f"{dw:.2f} cm", f"{de:.2f} cm", f"{n:.2f}", f"{Fn:.4f}", pattern, f"{S:.2f} m"]
        })
        st.dataframe(geo_df, hide_index=True, use_container_width=True)

    with colB:
        st.markdown('<div class="section-pill pill-blue">⏱️ พารามิเตอร์เวลา</div>', unsafe_allow_html=True)
        time_df = pd.DataFrame({
            "พารามิเตอร์": ["Cr (แนวรัศมี)", "Tr (Time factor รัศมี)", "Hd (ระยะระบายน้ำไกลสุด)", "Tv (Time factor แนวดิ่ง)"],
            "ค่า": [f"{Cr:.2f} cm²/day", f"{Tr:.4f}", f"{Hd_m:.2f} m", f"{Tv:.4f}"]
        })
        st.dataframe(time_df, hide_index=True, use_container_width=True)

    st.info("💡 **แนวทางปรับแบบ:** หาก Uav ยังไม่ถึงเป้าหมาย ลองลดระยะห่าง S ระหว่างท่อ PVD "
            "(เพิ่มความหนาแน่นของการติดตั้ง) หรือเปลี่ยนรูปแบบเป็นสามเหลี่ยมซึ่งมีประสิทธิภาพกว่าแบบสี่เหลี่ยม")

# ------------------------------------------------------------
# TAB 2: BARRON & TERZAGHI STEP-BY-STEP
# ------------------------------------------------------------
with tab2:
    mascot_bubble("surveyor", "มาดูขั้นตอนการคำนวณทีละสูตรกันครับ จะได้เข้าใจที่มาของตัวเลขแต่ละตัว 📋", size=56)
    st.markdown('<div class="section-pill pill-orange">🌀 วิธีของ Barron (การอัดตัวแนวรัศมี)</div>', unsafe_allow_html=True)
    st.latex(r"U_r = 1 - \exp\left(\frac{-8T_r}{F(n)}\right)")
    st.latex(r"F(n) = \frac{n^2}{n^2-1}\ln(n) - \frac{3n^2-1}{4n^2} \qquad n = \frac{d_e}{d_w} \qquad T_r = \frac{C_r \cdot t}{d_e^2}")

    st.markdown(f"""
    | ขั้นตอน | สูตร | ผลลัพธ์ |
    |---|---|---|
    | 1. คำนวณ dw | Hansbo: 2(a+b)/π | **{dw:.3f} cm** |
    | 2. คำนวณ de | {'1.13S' if pattern.startswith('สี่') else '1.05S'} | **{de:.2f} cm** |
    | 3. คำนวณ n | de / dw | **{n:.2f}** |
    | 4. คำนวณ F(n) | Barron (ไม่คิด smear) | **{Fn:.4f}** |
    | 5. คำนวณ Cr | (kr/kv) × Cv = {kr_kv:.1f} × {Cv:.1f} | **{Cr:.2f} cm²/day** |
    | 6. คำนวณ Tr | Cr·t / de² | **{Tr:.4f}** |
    | 7. คำนวณ Ur | 1 − exp(−8Tr/F(n)) | **{Ur*100:.2f}%** |
    """)

    st.markdown("---")
    st.markdown('<div class="section-pill pill-pink">📏 วิธีของ Terzaghi (การอัดตัวแนวดิ่ง)</div>', unsafe_allow_html=True)
    st.latex(r"U_v = \frac{\sqrt{4 \times T_v}}{\pi} \qquad T_v = \frac{C_v \times t}{H_d^2} \qquad (U_v \le 60\%)")
    st.markdown(f"""
    | ขั้นตอน | สูตร | ผลลัพธ์ |
    |---|---|---|
    | 1. กำหนด Hd | {drainage_cond} → H/2 หรือ H | **{Hd_m:.2f} m** ({Hd_cm:.0f} cm) |
    | 2. คำนวณ Tv | Cv·t / Hd² | **{Tv:.4f}** |
    | 3. คำนวณ Uv | √(4Tv/π) | **{Uv*100:.2f}%** |
    """)

    st.markdown("---")
    st.markdown('<div class="section-pill pill-purple">🔗 รวมผลด้วยวิธี Carillo (1942)</div>', unsafe_allow_html=True)
    st.latex(r"U_{av} = 1 - (1-U_r)(1-U_v)")
    st.success(f"**Uav = 1 − (1 − {Ur:.4f}) × (1 − {Uv:.4f}) = {Uav*100:.2f}%**")

# ------------------------------------------------------------
# TAB 3: U-t CHART
# ------------------------------------------------------------
with tab3:
    st.markdown('<div class="section-pill pill-blue">📈 ความสัมพันธ์ระหว่างระดับการอัดตัวกับเวลา</div>', unsafe_allow_html=True)

    t_max = max(t_design * 3, 30)
    t_arr = np.linspace(1, t_max, 300)

    Tr_arr = (Cr * t_arr) / (de ** 2)
    Ur_arr = Ur_barron(Tr_arr, Fn)

    Tv_arr = (Cv * t_arr) / (Hd_cm ** 2)
    Uv_arr = np.array([Uv_from_Tv(x) if x <= 0.283 else min(1 - (8/np.pi**2)*np.exp(-(np.pi**2/4)*x), 1.0) for x in Tv_arr])

    Uav_arr = Uav_carillo(Ur_arr, Uv_arr)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_arr, y=Ur_arr * 100, name="Ur (แนวรัศมี - Barron)",
                              line=dict(color="#8B5E34", width=3)))
    fig.add_trace(go.Scatter(x=t_arr, y=Uv_arr * 100, name="Uv (แนวดิ่ง - Terzaghi)",
                              line=dict(color="#C1694F", width=3, dash="dot")))
    fig.add_trace(go.Scatter(x=t_arr, y=Uav_arr * 100, name="Uav (รวม - Carillo)",
                              line=dict(color="#6E8B3D", width=4)))
    fig.add_hline(y=U_target, line_dash="dash", line_color="#8B3A1E",
                  annotation_text=f"เป้าหมาย {U_target}%", annotation_position="bottom right")
    fig.add_vline(x=t_design, line_dash="dash", line_color="#A08A6E",
                  annotation_text=f"t = {t_design} วัน", annotation_position="top left")

    fig.update_layout(
        template="plotly_white",
        xaxis_title="เวลา (วัน)",
        yaxis_title="ระดับการอัดตัว, U (%)",
        yaxis_range=[0, 105],
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=480,
        margin=dict(t=40, l=10, r=10, b=10),
        font=dict(family="Kanit"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFCF6",
    )
    st.plotly_chart(fig, use_container_width=True)

    # settlement over time chart
    St_arr = Uav_arr * Sfinal_cm
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=t_arr, y=St_arr, fill='tozeroy', name="การทรุดตัว",
                               line=dict(color="#4A7C6F", width=3), fillcolor="rgba(74,124,111,0.18)"))
    fig2.add_hline(y=Sfinal_cm, line_dash="dash", line_color="#8B3A1E",
                   annotation_text=f"Sfinal = {Sfinal_cm:.1f} cm")
    fig2.update_layout(
        template="plotly_white",
        xaxis_title="เวลา (วัน)",
        yaxis_title="การทรุดตัว, S (cm)",
        height=420,
        margin=dict(t=30, l=10, r=10, b=10),
        font=dict(family="Kanit"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFCF6",
    )
    st.markdown('<div class="section-pill pill-green">🏗️ การทรุดตัวตามเวลา</div>', unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True)

# ------------------------------------------------------------
# TAB 4: SETTLEMENT
# ------------------------------------------------------------
with tab4:
    mascot_bubble("soil", "ดินหนักแค่ไหน ยุบตัวไปเท่าไหร่แล้ว มาดูตัวเลขกันครับ 🌱", size=56)
    st.markdown('<div class="section-pill pill-pink">🏗️ การคำนวณระดับการยุบตัวของดิน</div>', unsafe_allow_html=True)
    st.latex(r"S_{final} = H \cdot \frac{C_c}{1+e_0} \cdot \log\left(\frac{\sigma_0' + \Delta\sigma}{\sigma_0'}\right)")
    st.latex(r"S_t = U_{av} \times S_{final}")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="metric-card">
            <div class="label">การทรุดตัวสูงสุด, S_final</div>
            <div class="value">{Sfinal_cm:.1f} cm</div>
            <div class="sub">{Sfinal_cm/100:.2f} m</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card">
            <div class="label">การทรุดตัว ณ t = {t_design} วัน</div>
            <div class="value">{St_cm:.1f} cm</div>
            <div class="sub">{St_cm/100:.2f} m</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card">
            <div class="label">Uav ที่ใช้คำนวณ</div>
            <div class="value">{Uav*100:.1f}%</div>
            <div class="sub">จาก Carillo</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("##### รายละเอียดการคำนวณ")
    st.markdown(f"""
    - H = {H:.2f} m = {H*100:.0f} cm  
    - Cc = {Cc:.3f}, e0 = {e0:.3f}  
    - σ'0 = {sigma0:.1f} kN/m², Δσ = {dsigma:.1f} kN/m²  
    - S_final = {H*100:.0f} × ({Cc:.3f}/(1+{e0:.3f})) × log10(({sigma0:.1f}+{dsigma:.1f})/{sigma0:.1f}) = **{Sfinal_cm:.2f} cm**  
    - S_t = {Uav:.4f} × {Sfinal_cm:.2f} = **{St_cm:.2f} cm**
    """)

# ------------------------------------------------------------
# TAB 5: SAND MAT
# ------------------------------------------------------------
with tab5:
    st.markdown('<div class="section-pill pill-green">🏖️ ดัชนีความต้านทานต่อการระบายน้ำของ Sand Mat</div>', unsafe_allow_html=True)
    st.latex(r"L = \frac{32}{\pi^2} \cdot \frac{1}{n^2} \cdot \frac{H}{H_m} \cdot \frac{k_c}{k_m} \cdot \left(\frac{B}{d_w}\right)^2")

    if check_sandmat:
        B_cm = (B_full / 2.0) * 100.0   # B = ครึ่งหนึ่งของความกว้าง, m -> cm
        H_cm = H * 100.0
        L = resistance_index_L(n, H_cm, Hm, kc, km, B_cm, dw)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""<div class="metric-card">
                <div class="label">ดัชนีความต้านทาน, L</div>
                <div class="value">{L:.4f}</div>
                <div class="sub">ยิ่งค่าน้อย ยิ่งระบายน้ำได้ดี</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            tag = '<span class="ok-tag">✔ L ต่ำ — Sand Mat เพียงพอ</span>' if L < 0.1 else \
                  ('<span class="warn-tag">⚠ L ปานกลาง — ควรพิจารณาเพิ่ม Hm</span>' if L < 1 else
                   '<span class="bad-tag">✘ L สูง — Sand Mat ไม่เพียงพอ อาจทำให้อัดตัวช้าลง</span>')
            st.markdown(f"""<div class="metric-card">
                <div class="label">ผลการประเมิน</div>
                <div class="value" style="font-size:1.1rem;">{tag}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("##### รายละเอียดตัวแปร")
        sm_df = pd.DataFrame({
            "ตัวแปร": ["n (de/dw)", "H (ความหนาดินเหนียว)", "Hm (ความหนาทราย)",
                       "kc (ซึมน้ำดินเหนียว)", "km (ซึมน้ำทราย)", "B (ครึ่งความกว้าง)", "dw"],
            "ค่า": [f"{n:.2f}", f"{H_cm:.0f} cm", f"{Hm:.0f} cm",
                    f"{kc:.1e} cm/s", f"{km:.1e} cm/s", f"{B_cm:.0f} cm", f"{dw:.2f} cm"]
        })
        st.dataframe(sm_df, hide_index=True, use_container_width=True)

        st.info("💡 หาก L สูงเกินไป ให้พิจารณา: เพิ่มความหนา Sand Mat (Hm), ลดความกว้างแผ่นทราย (B), "
                "หรือใช้วัสดุที่มีค่าการซึมน้ำสูงขึ้น (เพิ่ม km)")

        if L < 0.1:
            mascot_bubble("drain", "ชั้นทรายระบายน้ำได้คล่องมาก น้ำจาก PVD ขึ้นมาถึงผิวดินได้ไว ✨", size=56)
        elif L < 1:
            mascot_bubble("soil", "พอไหวอยู่ครับ แต่ลองเพิ่มความหนาทรายอีกนิดจะยิ่งชัวร์ 🌱", size=56)
        else:
            mascot_bubble("engineer", "โอ้โห L สูงไปหน่อยนะครับ 👷 น้ำอาจระบายไม่ทัน ลองปรับ Sand Mat ก่อนนะ", size=56)
    else:
        st.warning("ติ๊กเลือก 'ตรวจสอบ Sand Mat' ในแถบด้านซ้ายเพื่อคำนวณ")

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="footer-note">
    PVD Design Studio — อ้างอิงทฤษฎีจาก Barron (1948), Terzaghi, Carillo (1942), Bergado et al. (1992), Bo et al. (2003)<br>
    จัดทำเพื่อการศึกษา ภาควิชาครุศาสตร์โยธา คณะครุศาสตร์อุตสาหกรรม มจพ.
</div>
""", unsafe_allow_html=True)
