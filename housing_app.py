import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Stockholm Housing Statistics", page_icon="🏠", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #FAFAFA; }
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Lora:ital@0;1&display=swap');
    .block-container { padding-top: 3rem; max-width: 900px; }
    h1 { font-family: 'Inter', sans-serif !important; color: #111; font-weight: 800; font-size: 2.5rem; margin-bottom: 1rem; }
    h2 { font-family: 'Inter', sans-serif !important; color: #111; font-weight: 700; font-size: 1.6rem; border-bottom: 2px solid #E5E7EB; padding-bottom: 0.5rem; margin-top: 3rem; }
    p, li { font-family: 'Lora', serif !important; color: #333; font-size: 1.1rem; line-height: 1.8; }
    .metric-box { background-color: #FFF; padding: 1.5rem; border-radius: 8px; border: 1px solid #E5E7EB; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>Stockholm Housing Market: Statistical Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p>A comprehensive statistical report on 647 housing units in Stockholm County, analyzing pricing determinants through hypothesis testing and multivariate regression.</p>", unsafe_allow_html=True)

st.markdown("<h2>Part 1: Hypothesis Testing</h2>", unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["1. Balcony Proportion (Z-Test)", "2. Average Area (T-Test)", "3. Final Regression Model"])

with tab1:
    st.markdown("### Testing the Proportion of Balconies")
    st.markdown("**Hypothesis:** Is the proportion of houses with a balcony exactly 50%?")
    # Using \mathrm instead of \text to prevent Python from reading \t as a tab
    st.latex(r"H_0: p = 0.5 \quad \mathrm{vs} \quad H_1: p \neq 0.5")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**R Script Output:**")
        st.code("prop.test(x= has_bal, n=n, p=0.5, conf.level = 0.99)\n# X-squared = 18.028, df = 1, p-value = 2.177e-05\n# 99 percent confidence interval: 0.5329390 0.6337944\n# sample estimates: p = 0.5842349", language="r")
    with col2:
        st.markdown("**Interpretation:**")
        st.markdown("With a p-value of \(1.825 \\times 10^{-5}\) (which is < 0.01), we **reject the null hypothesis**. There is strong evidence that the proportion of houses with a balcony is not 50%.")
        st.info("**99% Confidence Interval:** (53.4%, 63.4%)")

with tab2:
    st.markdown("### Testing the Average Area")
    st.markdown("**Hypothesis:** Is the average size of a housing unit 75 \(m^2\)?")
    st.latex(r"H_0: \mu = 75 \quad \mathrm{vs} \quad H_1: \mu \neq 75")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**R Script Output:**")
        st.code("t.test(DataSet$AREA, mu = 75, conf.level = 0.95)\n# t = 1.3775, df = 646, p-value = 0.1688\n# 95 percent confidence interval: 74.16363 79.76747\n# sample estimates: mean of x = 76.96555", language="r")
    with col2:
        st.markdown("**Interpretation:**")
        st.markdown("With a p-value of 0.1688 (which is > 0.05), we **fail to reject the null hypothesis**. The average area is statistically indistinguishable from 75 \(m^2\).")
        st.info("**95% Confidence Interval:** (74.16, 79.77)")

with tab3:
    st.markdown("### Multivariate Regression Modeling")
    st.markdown("Started with simple linear regression (\(R^2 = 0.385\)) and multiple regression (\(R^2 = 0.563\)). Observed heteroscedasticity (funnel shape in residuals), so we applied a **log-transformation** and an interaction term (`Rooms * Area`).")
    st.markdown("**Final Model Equation (from R `lm` output):**")
    st.latex(r"\log(Price) = 13.899 + 0.185 \cdot Region_{NW} - 0.197 \cdot Region_{SE} + 0.377 \cdot Region_{STHLM} - 0.418 \cdot Region_{W} - 0.076 \cdot Terrace + 0.183 \cdot Villa + 0.110 \cdot Rooms - 0.070 \cdot Balcony + 0.014 \cdot Area - 0.001 \cdot (Rooms \times Area)")
    st.success("This model achieved an **\(R^2\) of 0.6113**, with the residuals satisfying normality and constant variance assumptions.")

st.markdown("<h2>Part 2: Live Valuation Engine</h2>", unsafe_allow_html=True)
def predict_price(region, h_type, balcony, rooms, area):
    log_price = 13.8988571 
    if region == "Northwest": log_price += 0.1850940
    elif region == "Southeast": log_price += -0.1972418
    elif region == "Stockholm": log_price += 0.3768469
    elif region == "West": log_price += -0.4179828
    if h_type == "Terrace": log_price += -0.0762431
    elif h_type == "Villa": log_price += 0.1829979
    if balcony == "Yes": log_price += -0.0697553
    log_price += 0.1103812 * rooms + 0.0138216 * area - 0.0010429 * (rooms * area)
    price = np.exp(log_price)
    lower = np.exp(log_price - (1.96 * 0.3525))
    upper = np.exp(log_price + (1.96 * 0.3525))
    return price, lower, upper

col1, col2 = st.columns(2)
with col1:
    region = st.selectbox("Region", ["Northeast", "Northwest", "Southeast", "Stockholm", "West"])
    h_type = st.selectbox("Housing Type", ["Apartment", "Terrace", "Villa"])
    balcony = st.radio("Balcony", ["No", "Yes"], horizontal=True)
with col2:
    area = st.slider("Area (m²)", min_value=15.0, max_value=250.0, value=75.0, step=1.0)
    rooms = st.slider("Number of Rooms", min_value=1.0, max_value=8.0, value=3.0, step=0.5)

price, lower, upper = predict_price(region, h_type, balcony, rooms, area)
st.markdown("---")
col_r1, col_r2, col_r3 = st.columns([2, 1, 1])
with col_r1:
    st.markdown(f"<div class='metric-box'><p style='margin:0; font-size: 1rem; text-transform: uppercase; color: #666;'>Estimated Starting Price</p><p style='margin:0; font-size: 2.5rem; font-weight: 800; color: #004b87;'>{price:,.0f} SEK</p></div>", unsafe_allow_html=True)
with col_r2:
    st.metric("Lower Bound (95% PI)", f"{lower:,.0f} SEK")
with col_r3:
    st.metric("Upper Bound (95% PI)", f"{upper:,.0f} SEK")

st.markdown("### Explainable AI: Why this price?")
contributions = {"Base": 13.8988571, "Area": 0.0138216 * area, "Rooms": 0.1103812 * rooms, "Interaction": -0.0010429 * (rooms * area)}
if region != "Northeast": contributions[f"Region ({region})"] = 0.1850940 if region=="Northwest" else -0.1972418 if region=="Southeast" else 0.3768469 if region=="Stockholm" else -0.4179828
if h_type != "Apartment": contributions[f"Type ({h_type})"] = -0.0762431 if h_type=="Terrace" else 0.1829979
if balcony == "Yes": contributions["Balcony"] = -0.0697553

sorted_contribs = sorted(contributions.items(), key=lambda x: abs(x[1]), reverse=True)
fig = go.Figure(go.Bar(x=[x[1] for x in sorted_contribs], y=[x[0] for x in sorted_contribs], orientation='h', marker_color=['#004b87' if x[1] > 0 else '#e07a5f' for x in sorted_contribs], text=[f"{x[1]:+.3f}" for x in sorted_contribs], textposition='auto'))
fig.update_layout(template="plotly_white", height=300, margin=dict(l=0, r=0, t=10, b=0))
st.plotly_chart(fig, use_container_width=True)
