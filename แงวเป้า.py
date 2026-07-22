import streamlit as st
import numpy as np

# -----------------------------
# ตั้งค่าหน้าเว็บ
# -----------------------------
st.set_page_config(
    page_title="PVD Designer",
    page_icon="🏗️",
    layout="centered"
)

st.title("🏗️ Prefabricated Vertical Drain (PVD) Designer")
st.write("### โปรแกรมคำนวณเบื้องต้น")

# -----------------------------
# รับข้อมูล
# -----------------------------
st.sidebar.header("ข้อมูลการออกแบบ")

pattern = st.sidebar.selectbox(
    "รูปแบบการติดตั้ง",
    ["Square", "Triangular"]
)

spacing = st.sidebar.number_input(
    "Spacing (m)",
    value=1.20,
    step=0.10
)

width = st.sidebar.number_input(
    "PVD Width (mm)",
    value=100.0
)

thickness = st.sidebar.number_input(
    "PVD Thickness (mm)",
    value=4.0
)

# -----------------------------
# คำนวณ
# -----------------------------
if st.button("🧮 Calculate"):

    # Equivalent Diameter (Hansbo)
    dw = 2 * (width + thickness) / np.pi      # mm
    dw_cm = dw / 10                           # cm

    # Effective Diameter
    if pattern == "Square":
        de = 1.13 * spacing * 100             # cm
    else:
        de = 1.05 * spacing * 100             # cm

    # -------------------------
    # แสดงผล
    # -------------------------
    st.success("Calculation Complete")

    col1, col2 = st.columns(2)

    col1.metric(
        "Equivalent Diameter (dw)",
        f"{dw_cm:.2f} cm"
    )

    col2.metric(
        "Effective Diameter (de)",
        f"{de:.2f} cm"
    )

    st.divider()

    st.subheader("Design Summary")

    st.write(f"**Pattern :** {pattern}")
    st.write(f"**Spacing :** {spacing:.2f} m")
    st.write(f"**Width :** {width:.1f} mm")
    st.write(f"**Thickness :** {thickness:.1f} mm")

    st.info("เวอร์ชันทดลองสำหรับการเรียนรู้")
🏗️ Prefabricated Vertical Drain (PVD) Designer

----------------------------------

Sidebar

Pattern
Square / Triangular

Spacing

Width

Thickness

[ Calculate ]

----------------------------------

Equivalent Diameter (dw)

Effective Diameter (de)

Design Summary
