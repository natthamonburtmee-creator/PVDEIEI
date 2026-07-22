import streamlit as st
import numpy as np
import math

st.set_page_config(page_title="PVD Designer", layout="wide")

st.title("🏗️ Prefabricated Vertical Drain Designer")
st.subheader("Barron Theory (Demo Version)")

st.sidebar.header("Input Data")

pattern = st.sidebar.selectbox(
    "Installation Pattern",
    ["Square", "Triangular"]
)

spacing = st.sidebar.number_input(
    "Spacing S (m)",
    value=1.0,
    step=0.1
)

width = st.sidebar.number_input(
    "PVD Width (mm)",
    value=100.0
)

thickness = st.sidebar.number_input(
    "PVD Thickness (mm)",
    value=5.0
)

Ch = st.sidebar.number_input(
    "Horizontal Consolidation Coefficient Ch (cm²/day)",
    value=20.0
)

time = st.sidebar.number_input(
    "Construction Time (day)",
    value=90.0
)

if st.sidebar.button("Calculate"):

    # Equivalent Diameter (Hansbo)
    dw = 2 * (width + thickness) / np.pi

    dw_cm = dw / 10.0

    if pattern == "Square":
        de = 1.13 * spacing * 100
    else:
        de = 1.05 * spacing * 100

    n = de / dw_cm

    Fn = np.log(n) - 0.75

    Tr = Ch * time / (de**2)

    Ur = 1 - np.exp(-8 * Tr / Fn)

    st.header("Results")

    col1, col2 = st.columns(2)

    col1.metric("Equivalent Diameter dw (cm)", f"{dw_cm:.2f}")

    col1.metric("Effective Diameter de (cm)", f"{de:.2f}")

    col2.metric("Drain Spacing Factor Fn", f"{Fn:.3f}")

    col2.metric("Radial Consolidation Ur", f"{Ur*100:.2f}%")

    if Ur >= 0.90:
        st.success("PASS : Degree of Consolidation ≥ 90%")
    else:
        st.error("FAIL : Degree of Consolidation < 90%")

    st.subheader("Consolidation Curve")

    days = np.arange(1, int(time)+1)

    Tr_curve = Ch * days / (de**2)

    Ur_curve = 1 - np.exp(-8 * Tr_curve / Fn)

    st.line_chart(Ur_curve)
