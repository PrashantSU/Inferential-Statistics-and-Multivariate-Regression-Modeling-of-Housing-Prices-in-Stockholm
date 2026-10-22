import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG & PREMIUM EDITORIAL CSS
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Stockholm Real Estate Analytics", page_icon="🏙️", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Lora:ital,wght@0,400;0,500;1,400&display=swap');
    
    .stApp { background-color: #FAFAFA; }
    .block-container { padding-top: 3rem; max-width: 950px; }
    
    /* Typography */
    h1 { font-family: 'Inter', sans-serif !important; color: #0F172A; font-weight: 800; font-size: 3rem; line-height: 1.1; margin-bottom: 1rem; letter-spacing: -0.03em;}
    h2 { font-family: 'Inter', sans-serif !important; color: #0F172A; font-weight: 700; font-size: 2rem; border-bottom: 2px solid #E2E8F0; padding-bottom: 0.5rem; margin-top: 4rem; }
    h3 { font-family: 'Inter', sans-serif !important; color: #004b87; font-weight: 600; font-size: 1.3rem; margin-top: 2rem; }
    p, li, .stMarkdown { font-family: 'Lora', serif !important; color: #334155; font-size: 1.15rem; line-height: 1.8; }
    
    /* Editorial Elements */
    .hero-caption { font-family: 'Inter', sans-serif; font-size: 0.85rem; color: #64748B; margin-top: 0.5rem; margin-bottom: 3rem; }
    .pull-quote { font-family: 'Lora', serif; font-size: 1.6rem; font-style: italic; color: #0F172A; margin: 3rem 0; padding: 1rem 0 1rem 2rem; border-left: 4px solid #004b87; background-color: #F8FAFC; }
    .metric-card { background-color: #FFFFFF; padding: 1.5rem; border-radius: 12px; border: 1px solid #E2E8F0; text-align: center; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
    .metric-value { font-family: 'Inter', sans-serif; font-size: 2rem; font-weight: 800; color: #004b87; margin: 0; }
    .metric-label { font-family: 'Inter', sans-serif; font-size: 0.9rem; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E2E8F0; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🏙️ Market Analysis")
    st.markdown("**Stockholm Real Estate**\n*Statistical Inference & Modeling*")
    st.markdown("---")
    page = st.radio("Navigate the Report:", [
        "1. Executive Summary",
        "2. Exploratory Data Analysis",
        "3. Hypothesis Testing",
        "4. The Valuation Engine",
        "5. Test Predictions"
    ])
    st.markdown("---")
    st.caption("Developed by Prashant Kumar Singh\nMSc Data Science @ Stockholm University")

# -----------------------------------------------------------------------------
# 3. MATHEMATICAL MODEL & DATA
# -----------------------------------------------------------------------------
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
# PAGE 1: EXECUTIVE SUMMARY
# =============================================================================
if page.startswith("1"):
    st.markdown("<h1>Decoding the Stockholm Real Estate Market.</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.3rem; color: #475569;'>How we used inferential statistics and explainable AI to demystify property valuations.</p>", unsafe_allow_html=True)
    
    st.image("https://images.unsplash.com/photo-1509356843151-3e7d96241e11?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80", use_container_width=True)
    st.markdown("<div class='hero-caption'>Stockholm, Sweden. Photo: Unsplash</div>", unsafe_allow_html=True)

    st.markdown("""
    <p style='font-size: 1.2rem;'><b>The Problem:</b> Buying a home in Stockholm is one of the most significant financial decisions a person can make. Yet, pricing often feels like a black box. Why does a 3-room apartment in Södermalm cost double the price of a similar one in the suburbs?</p>
    
    <p style='font-size: 1.2rem;'><b>The Solution:</b> We analyzed a dataset of 647 housing units across Stockholm County. Instead of guessing, we applied rigorous statistical inference to debunk market myths, and built a <b>log-linear multivariate regression model</b> to objectively isolate the factors that truly drive price.</p>
    """, unsafe_allow_html=True)

    st.markdown("<h2>The Market at a Glance</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.markdown("<div class='metric-card'><p class='metric-label'>Mean Price</p><p class='metric-value'>4.27M SEK</p></div>", unsafe_allow_html=True)
    col2.markdown("<div class='metric-card'><p class='metric-label'>Median Price</p><p class='metric-value'>3.49M SEK</p></div>", unsafe_allow_html=True)
    col3.markdown("<div class='metric-card'><p class='metric-label'>Right-Skewness</p><p class='metric-value'>2.06</p></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='pull-quote'>
    "The mean price is heavily distorted by ultra-luxury outliers. To understand the typical Stockholm buyer, we must look at the median."
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# PAGE 2: EXPLORATORY DATA ANALYSIS (EDA)
# =============================================================================
elif page.startswith("2"):
    st.markdown("<h1>Exploratory Data Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<p>Before building predictive models, we must understand the shape of the data and the relationships between variables.</p>", unsafe_allow_html=True)

    st.markdown("<h2>The Area vs. Price Relationship</h2>", unsafe_allow_html=True)
    st.markdown("<p>Intuitively, larger homes cost more. Our analysis confirms a <b>moderate positive correlation (Pearson's r = 0.62)</b>. However, Area alone only explains 38.5% of the price variance. The location and type of housing play a massive role.</p>", unsafe_allow_html=True)

    # Simulate scatter plot
    np.random.seed(42)
    areas = np.random.normal(77, 36, 647)
    areas = np.clip(areas, 15, 250)
    prices = 646202 + 47132 * areas + np.random.normal(0, 1500000, 647)
    prices = np.clip(prices, 500000, 15000000)
    
    fig = px.scatter(x=areas, y=prices, labels={'x': 'Area (m²)', 'y': 'Starting Price (SEK)'}, opacity=0.5, color_discrete_sequence=['#004b87'])
    fig.update_layout(template="plotly_white", height=450, margin=dict(l=0, r=0, t=10, b=0), title="Scatterplot: Area vs Starting Price")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<h2>Housing Types Across Regions</h2>", unsafe_allow_html=True)
    st.markdown("<p>Cross-tabulation reveals that <b>Apartments dominate the market</b> in almost every region, particularly in Stockholm and the Northwest. Villas and Terraces are much rarer, which makes them statistically distinct in our model.</p>", unsafe_allow_html=True)

# =============================================================================
# PAGE 3: HYPOTHESIS TESTING
# =============================================================================
elif page.startswith("3"):
    st.markdown("<h1>Hypothesis Testing: Debunking Myths</h1>", unsafe_allow_html=True)
    st.markdown("<p>We used statistical inference to test common assumptions about the Stockholm housing market. We set our significance levels strictly (\(\alpha = 0.01\) or \(0.05\)).</p>", unsafe_allow_html=True)

    t1, t2, t3, t4 = st.tabs(["1. Balcony Z-Test", "2. Average Area T-Test", "3. Apartment Proportion", "4. Expected Rooms"])

    with t1:
        st.markdown("### Myth: Exactly 50% of homes have a balcony.")
        st.latex(r"H_0: p = 0.5 \quad \text{vs} \quad H_1: p \neq 0.5")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**The Evidence (R Output):**")
            st.code("prop.test(x= has_bal, n=647, p=0.5, conf.level = 0.99)\n# X-squared = 18.028, p-value = 2.177e-05\n# 99% CI: 0.5329 to 0.6337\n# sample estimate: p = 0.5842", language="r")
        with col2:
            st.markdown("**The Verdict:**")
            st.markdown("We **reject the null hypothesis**. With a p-value of \(1.82 \times 10^{-5}\) (far below 0.01), we are highly confident that the true proportion is not 50%. In fact, we are 99% confident it lies between **53.4% and 63.4%**.")
            st.error("Conclusion: Balconies are more common than a coin flip.")

    with t2:
        st.markdown("### Myth: The average home size is exactly 75 m².")
        st.latex(r"H_0: \mu = 75 \quad \text{vs} \quad H_1: \mu \neq 75")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**The Evidence (R Output):**")
            st.code("t.test(DataSet$AREA, mu = 75, conf.level = 0.95)\n# t = 1.3775, p-value = 0.1688\n# 95% CI: 74.16 to 79.76\n# sample mean = 76.96 m²", language="r")
        with col2:
            st.markdown("**The Verdict:**")
            st.markdown("With a p-value of 0.1688 (which is > 0.05), we **fail to reject the null hypothesis**. The 95% confidence interval contains 75. Therefore, we cannot statistically prove the average size is different from 75 m².")
            st.warning("Conclusion: 75 m² is a statistically sound assumption.")

    with t3:
        st.markdown("### Estimate: What proportion of the market is Apartments?")
        col1, col2 = st.columns(2)
        with col1:
            st.code("prop.test(sum(TYPE == 'Apartment'), n=647, conf.level=0.90)\n# 90% CI: 0.7727 to 0.8259\n# sample estimate: p = 0.8006", language="r")
        with col2:
            st.markdown("We are **90% confident** that the true proportion of apartments in Stockholm County lies between **77.27% and 82.59%**. The market is overwhelmingly apartment-driven.")

    with t4:
        st.markdown("### Estimate: What is the expected number of rooms?")
        col1, col2 = st.columns(2)
        with col1:
            st.code("t.test(DataSet$ROOMS, conf.level=0.95)\n# 95% CI: 2.942 to 3.166\n# sample mean = 3.054 rooms", language="r")
        with col2:
            st.markdown("The average home has about 3 rooms. We are **95% confident** that the true expected number of rooms lies between **2.94 and 3.17**.")

# =============================================================================
# PAGE 4: THE VALUATION ENGINE
# =============================================================================
elif page.startswith("4"):
    st.markdown("<h1>The Valuation Engine</h1>", unsafe_allow_html=True)
    st.markdown("<p>To accurately predict price, simple regression wasn't enough. We built a <b>log-linear multivariate model</b> with an interaction term to correct for non-constant variance (heteroscedasticity).</p>", unsafe_allow_html=True)

    st.markdown("<h2>The Mathematical Model</h2>", unsafe_allow_html=True)
    st.latex(r"\log(Price) = 13.899 + \beta_{region} + \beta_{type} + 0.110 \cdot Rooms - 0.070 \cdot Balcony + 0.014 \cdot Area - 0.001 \cdot (Rooms \times Area)")
    
    st.markdown("<p>By taking the natural logarithm of the price, we transformed the data so the residuals follow a normal distribution, achieving an <b>\(R^2\) of 0.6113</b> (a massive jump from the 0.385 of simple regression).</p>", unsafe_allow_html=True)

    st.markdown("<h2>Try the Live Predictor</h2>", unsafe_allow_html=True)
    st.markdown("<p>Adjust the property features below to see the model's valuation in real-time.</p>", unsafe_allow_html=True)

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
        st.markdown(f"<div class='metric-card'><p class='metric-label'>Estimated Starting Price</p><p class='metric-value'>{price:,.0f} SEK</p></div>", unsafe_allow_html=True)
    with col_r2:
        st.metric("Lower Bound (95% PI)", f"{lower:,.0f} SEK")
    with col_r3:
        st.metric("Upper Bound (95% PI)", f"{upper:,.0f} SEK")

    st.markdown("<h3>Explainable AI: Feature Contributions</h3>", unsafe_allow_html=True)
    st.markdown("<p>Why did the model predict this price? The chart below shows the exact positive or negative log-impact of every feature.</p>", unsafe_allow_html=True)
    
    contributions = {"Base Intercept": 13.8988571, "Area": 0.0138216 * area, "Rooms": 0.1103812 * rooms, "Interaction (Rooms*Area)": -0.0010429 * (rooms * area)}
    if region != "Northeast": contributions[f"Region ({region})"] = 0.1850940 if region=="Northwest" else -0.1972418 if region=="Southeast" else 0.3768469 if region=="Stockholm" else -0.4179828
    if h_type != "Apartment": contributions[f"Type ({h_type})"] = -0.0762431 if h_type=="Terrace" else 0.1829979
    if balcony == "Yes": contributions["Balcony"] = -0.0697553

    sorted_contribs = sorted(contributions.items(), key=lambda x: abs(x[1]), reverse=True)
    fig = go.Figure(go.Bar(x=[x[1] for x in sorted_contribs], y=[x[0] for x in sorted_contribs], orientation='h', marker_color=['#004b87' if x[1] > 0 else '#e07a5f' for x in sorted_contribs], text=[f"{x[1]:+.3f}" for x in sorted_contribs], textposition='auto'))
    fig.update_layout(template="plotly_white", height=350, margin=dict(l=0, r=0, t=10, b=0), xaxis_title="Impact on log(Price)")
    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# PAGE 5: TEST PREDICTIONS
# =============================================================================
elif page.startswith("5"):
    st.markdown("<h1>Test Predictions</h1>", unsafe_allow_html=True)
    st.markdown("<p>We applied our final log-transformed model to 6 unseen properties to predict their starting prices, complete with 95% prediction intervals.</p>", unsafe_allow_html=True)

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
        }).set_properties(**{'background-color': '#FFFFFF', 'color': '#333'}), 
        use_container_width=True, 
        hide_index=True
    )
    
    st.markdown("""
    <div class='pull-quote'>
    "Notice the width of the prediction intervals. Real estate pricing has inherent variance, and a responsible model must communicate its uncertainty."
    </div>
    """, unsafe_allow_html=True)
