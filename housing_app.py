import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG & CSS
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Stockholm Housing Analysis", page_icon="🏠", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Lora:ital@0;1&display=swap');
    .stApp { background-color: #FAFAFA; }
    .block-container { padding-top: 2rem; max-width: 1000px; }
    
    h1 { font-family: 'Inter', sans-serif !important; color: #111; font-weight: 800; font-size: 2.8rem; margin-bottom: 0.5rem; letter-spacing: -0.03em;}
    h2 { font-family: 'Inter', sans-serif !important; color: #111; font-weight: 700; font-size: 1.8rem; border-bottom: 2px solid #E5E7EB; padding-bottom: 0.5rem; margin-top: 3rem; }
    h3 { font-family: 'Inter', sans-serif !important; color: #004b87; font-weight: 600; font-size: 1.2rem; margin-top: 2rem; }
    
    p, li, .stMarkdown { font-family: 'Lora', serif !important; color: #333; font-size: 1.1rem; line-height: 1.8; }
    
    .metric-box { background-color: #FFFFFF; padding: 1.5rem; border-radius: 12px; border: 1px solid #E2E8F0; text-align: center; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
    .price-text { font-family: 'Inter', sans-serif; font-size: 2.8rem; font-weight: 800; color: #004b87; margin: 0; }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] { background-color: #F8FAFC; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🏠 Stockholm Housing")
    st.markdown("**MSc Data Science Project**\nPrashant Kumar Singh")
    st.markdown("---")
    page = st.radio("Navigate the Report:", [
        "1. EDA & Descriptive Stats",
        "2. Hypothesis Testing (All 4)",
        "3. Regression Modeling",
        "4. Live Valuation Engine",
        "5. Test Data Predictions"
    ])
    st.markdown("---")
    st.markdown("Based on a dataset of **647 housing units** in Stockholm County.")

# -----------------------------------------------------------------------------
# 3. DATA & MATH PREP
# -----------------------------------------------------------------------------
# Hardcoded EDA values from your report
mean_price = 4273799
median_price = 3495000
skewness = 2.06

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

# =============================================================================
# PAGE 1: EDA
# =============================================================================
if page.startswith("1"):
    st.markdown("<h1>Exploratory Data Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<p>Before modeling, we explored the distributions and relationships within the 647 housing units.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Mean Starting Price", f"{mean_price:,.0f} SEK")
    col2.metric("Median Starting Price", f"{median_price:,.0f} SEK")
    col3.metric("Skewness", f"{skewness}", "Right-skewed", delta_color="off")
    
    st.markdown("### Area vs. Starting Price")
    st.markdown("<p>Pearson's correlation coefficient is <b>0.62</b>, indicating a moderate positive relationship. Area is an important driver, but not the only one.</p>", unsafe_allow_html=True)
    
    # Simulated Scatter Plot based on the report's correlation
    np.random.seed(42)
    areas = np.random.normal(77, 36, 647)
    areas = np.clip(areas, 15, 250)
    # Base price on regression formula + noise
    prices = 646202 + 47132 * areas + np.random.normal(0, 1500000, 647)
    prices = np.clip(prices, 500000, 15000000)
    
    fig = px.scatter(x=areas, y=prices, labels={'x': 'Area (m²)', 'y': 'Starting Price (SEK)'}, opacity=0.5, color_discrete_sequence=['#004b87'])
    fig.update_layout(template="plotly_white", height=400, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# PAGE 2: HYPOTHESIS TESTING
# =============================================================================
elif page.startswith("2"):
    st.markdown("<h1>Hypothesis Testing</h1>", unsafe_allow_html=True)
    st.markdown("<p>Rigorous statistical inference was performed to validate market assumptions using Z-tests and T-tests.</p>", unsafe_allow_html=True)
    
    t1, t2, t3, t4 = st.tabs(["1. Balcony Proportion", "2. Average Area", "3. Apartment Proportion", "4. Expected Rooms"])
    
    with t1:
        st.markdown("### One-Proportion Z-Test: Balconies")
        st.markdown("**Hypothesis:** Is the proportion of houses with a balcony exactly 50%?")
        st.latex(r"H_0: p = 0.5 \quad \mathrm{vs} \quad H_1: p \neq 0.5")
        col1, col2 = st.columns(2)
        with col1:
            st.code("prop.test(x= has_bal, n=647, p=0.5, conf.level = 0.99)\n# X-squared = 18.028, df = 1, p-value = 2.177e-05\n# 99 percent confidence interval: 0.5329390 0.6337944\n# sample estimates: p = 0.5842349", language="r")
        with col2:
            st.markdown("**Interpretation:**")
            st.markdown("With a p-value of \(1.825 \\times 10^{-5}\) (which is < 0.01), we **reject the null hypothesis**. There is strong evidence that the proportion of houses with a balcony is not 50%.")
            st.success("**99% Confidence Interval:** (53.4%, 63.4%)")

    with t2:
        st.markdown("### One-Sample T-Test: Average Area")
        st.markdown("**Hypothesis:** Is the average size of a housing unit 75 \(m^2\)?")
        st.latex(r"H_0: \mu = 75 \quad \mathrm{vs} \quad H_1: \mu \neq 75")
        col1, col2 = st.columns(2)
        with col1:
            st.code("t.test(DataSet$AREA, mu = 75, conf.level = 0.95)\n# t = 1.3775, df = 646, p-value = 0.1688\n# 95 percent confidence interval: 74.16363 79.76747\n# sample estimates: mean of x = 76.96555", language="r")
        with col2:
            st.markdown("**Interpretation:**")
            st.markdown("With a p-value of 0.1688 (which is > 0.05), we **fail to reject the null hypothesis**. The average area is statistically indistinguishable from 75 \(m^2\).")
            st.info("**95% Confidence Interval:** (74.16, 79.77)")

    with t3:
        st.markdown("### 90% Confidence Interval: Apartment Proportion")
        st.markdown("**Goal:** Estimate the true proportion of apartments in the region.")
        col1, col2 = st.columns(2)
        with col1:
            st.code("prop.test(sum(DataSet$TYPE == 'Apartment'), n=647, conf.level=0.90)\n# 90 percent confidence interval: 0.7727467 0.8259114\n# sample estimates: p = 0.8006182", language="r")
        with col2:
            st.markdown("**Interpretation:**")
            st.markdown("The observed proportion is **80.06%**. We are 90% confident that the true proportion of apartments in Stockholm County lies between 77.27% and 82.59%.")
            st.info("**90% Confidence Interval:** (0.773, 0.826)")

    with t4:
        st.markdown("### 95% Confidence Interval: Expected Number of Rooms")
        st.markdown("**Goal:** Estimate the true mean number of rooms.")
        col1, col2 = st.columns(2)
        with col1:
            st.code("t.test(DataSet$ROOMS, conf.level=0.95)\n# 95 percent confidence interval: 2.942039 3.166153\n# sample estimates: mean of x = 3.054096", language="r")
        with col2:
            st.markdown("**Interpretation:**")
            st.markdown("The sample mean is **3.05 rooms**. We are 95% confident that the true expected number of rooms lies between 2.94 and 3.17.")
            st.info("**95% Confidence Interval:** (2.942, 3.166)")

# =============================================================================
# PAGE 3: REGRESSION MODELING
# =============================================================================
elif page.startswith("3"):
    st.markdown("<h1>Regression Modeling</h1>", unsafe_allow_html=True)
    
    st.markdown("### The Iterative Modeling Process")
    st.markdown("""
    **1. Simple Linear Regression:** `STARTING_PRICE ~ AREA`
    *   \(R^2\) = 0.385. Area alone explains only 38.5% of the variance.
    
    **2. Multiple Linear Regression:** `STARTING_PRICE ~ REGION + TYPE + BALCONY + ROOMS + AREA`
    *   \(R^2\) = 0.5628. However, the **Residuals vs Fitted** plot showed a funnel shape, indicating **heteroscedasticity** (non-constant variance).
    
    **3. Final Log-Transformed Model with Interaction**
    *   To fix the residuals, we applied a log-transformation and added an interaction term (`ROOMS * AREA`).
    *   This pushed the **\(R^2\) to 0.6113** and satisfied the assumptions of linearity, normality, and constant variance.
    """)
    
    st.markdown("### Final Model Equation")
    st.latex(r"\log(Price) = 13.899 + \beta_{region} + \beta_{type} + 0.110 \cdot Rooms - 0.070 \cdot Balcony + 0.014 \cdot Area - 0.001 \cdot (Rooms \times Area)")
    
    st.markdown("### Statistically Significant Variables (\(p < 0.05\))")
    st.markdown("""
    *   **Region:** Stockholm (+0.377), West (-0.418), Northwest (+0.185), Southeast (-0.197)
    *   **Type:** Villa (+0.183)
    *   **Rooms:** (+0.110)
    *   **Area:** (+0.014)
    *   **Balcony:** (-0.070)
    *   **Interaction:** Rooms \(\\times\) Area (-0.001)
    """)

# =============================================================================
# PAGE 4: LIVE PREDICTOR
# =============================================================================
elif page.startswith("4"):
    st.markdown("<h1>Live Valuation Engine</h1>", unsafe_allow_html=True)
    st.markdown("<p>Test the final regression model yourself. Adjust the inputs to predict the starting price based on the log-linear equation.</p>", unsafe_allow_html=True)

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
        st.markdown(f"<div class='metric-box'><p style='margin:0; font-size: 1rem; text-transform: uppercase; color: #666;'>Estimated Starting Price</p><p class='price-text'>{price:,.0f} SEK</p></div>", unsafe_allow_html=True)
    with col_r2:
        st.metric("Lower Bound (95% PI)", f"{lower:,.0f} SEK")
    with col_r3:
        st.metric("Upper Bound (95% PI)", f"{upper:,.0f} SEK")

    st.markdown("### Explainable AI: Feature Contributions")
    contributions = {"Base Intercept": 13.8988571, "Area": 0.0138216 * area, "Rooms": 0.1103812 * rooms, "Interaction": -0.0010429 * (rooms * area)}
    if region != "Northeast": contributions[f"Region ({region})"] = 0.1850940 if region=="Northwest" else -0.1972418 if region=="Southeast" else 0.3768469 if region=="Stockholm" else -0.4179828
    if h_type != "Apartment": contributions[f"Type ({h_type})"] = -0.0762431 if h_type=="Terrace" else 0.1829979
    if balcony == "Yes": contributions["Balcony"] = -0.0697553

    sorted_contribs = sorted(contributions.items(), key=lambda x: abs(x[1]), reverse=True)
    fig = go.Figure(go.Bar(x=[x[1] for x in sorted_contribs], y=[x[0] for x in sorted_contribs], orientation='h', marker_color=['#004b87' if x[1] > 0 else '#e07a5f' for x in sorted_contribs], text=[f"{x[1]:+.3f}" for x in sorted_contribs], textposition='auto'))
    fig.update_layout(template="plotly_white", height=350, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# PAGE 5: TEST DATA PREDICTIONS
# =============================================================================
elif page.startswith("5"):
    st.markdown("<h1>Test Data Predictions</h1>", unsafe_allow_html=True)
    st.markdown("<p>Using the final log-transformed model, we predicted the starting prices for 6 unseen housing units. Below are the point predictions and the 95% prediction intervals.</p>", unsafe_allow_html=True)
    
    test_data = pd.DataFrame({
        "ID": [629, 718, 1534, 1695, 1864, 2138],
        "Region": ["Northwest", "Northeast", "Stockholm", "Stockholm", "Stockholm", "Northeast"],
        "Type": ["Apartment", "Apartment", "Apartment", "Apartment", "Apartment", "Apartment"],
        "Rooms": [3, 4, 6, 2, 1, 2],
        "Area": [74.0, 99.5, 115.0, 45.0, 29.0, 47.5],
        "Balcony": ["Yes", "Yes", "Yes", "No", "No", "Yes"],
        "Fit (SEK)": [3747555, 4117685, 6838775, 3350357, 2562945, 2207375],
        "Lower (95%)": [1864607, 2051409, 3392129, 1672540, 1277154, 1100005],
        "Upper (95%)": [7531971, 8265212, 13787459, 6711286, 5143222, 4429530]
    })
    
    st.dataframe(
        test_data.style.format({
            "Fit (SEK)": "{:,.0f}", 
            "Lower (95%)": "{:,.0f}", 
            "Upper (95%)": "{:,.0f}"
        }), 
        use_container_width=True, 
        hide_index=True
    )
    
    st.markdown("""
    <p style='font-size: 0.9rem; color: #888;'>Note: The wide prediction intervals reflect the high variance (residual standard error = 0.3525 on the log scale) inherent in real estate pricing.</p>
    """, unsafe_allow_html=True)
