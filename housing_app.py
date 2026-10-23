"""
Stockholm Real Estate Analytics: portfolio edition
Run:  streamlit run app.py
Tip:  create .streamlit/config.toml with
      [theme]
      base = "light"
      so the design renders the same on every recruiter's machine.
"""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# -----------------------------------------------------------------------------
# CONFIG: edit these
# -----------------------------------------------------------------------------
AUTHOR = "Prashant Kumar Singh"
TAGLINE = "MSc Data Science, Stockholm University"
GITHUB = "https://github.com/"        # replace with your profile / repo
LINKEDIN = "https://www.linkedin.com/"  # replace with your profile

IMG_HERO = "https://images.unsplash.com/photo-1509356843151-3e7d96241e11?auto=format&fit=crop&w=1800&q=80"
IMG_A = "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=900&q=80"
IMG_B = "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=900&q=80"
IMG_C = "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=900&q=80"

# Palette: Baltic ink, Falu red (the Swedish farmhouse red), harbour teal, facade ochre
INK, FALU, TEAL, OCHRE = "#10202F", "#A5392B", "#1F6E78", "#D6A04A"
MIST, LINE, MUTED = "#F2F5F8", "#DCE3EA", "#5B6B7B"

st.set_page_config(page_title="Stockholm Real Estate Analytics", page_icon="🏙️", layout="wide")

# -----------------------------------------------------------------------------
# STYLE
# -----------------------------------------------------------------------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,500;0,6..72,700;1,6..72,400&family=Manrope:wght@400;500;600;800&display=swap');
.stApp {{ background:{MIST}; }}
.block-container {{ max-width:1020px; padding-top:2rem; padding-bottom:5rem; }}
header[data-testid="stHeader"] {{ background:transparent; }}
h1,h2,h3 {{ font-family:'Newsreader',serif !important; color:{INK}; letter-spacing:-0.01em; }}
h1 {{ font-size:3.1rem !important; line-height:1.08 !important; font-weight:700 !important; }}
h2 {{ font-size:2rem !important; font-weight:700 !important; margin-top:3.2rem !important; }}
h3 {{ font-size:1.35rem !important; font-weight:500 !important; }}
p, li, label, .stMarkdown, .stCaption {{ font-family:'Manrope',sans-serif !important; color:#2C3C4D; font-size:1.02rem; line-height:1.75; }}
.prose {{ max-width:68ch; font-size:1.08rem; line-height:1.8; }}
.prose b {{ color:{INK}; }}

.hero {{ position:relative; border-radius:6px; overflow:hidden; min-height:430px; display:flex; align-items:flex-end;
  background: linear-gradient(135deg,{INK},{TEAL}); }}
.hero-img {{ position:absolute; inset:0; background-size:cover; background-position:center 60%; }}
.hero-shade {{ position:absolute; inset:0; background:linear-gradient(180deg,rgba(16,32,47,.15) 0%,rgba(16,32,47,.88) 100%); }}
.hero-body {{ position:relative; padding:2.6rem 2.8rem; }}
.hero h1 {{ color:#fff !important; margin:0 0 .8rem 0; max-width:16ch; }}
.hero p {{ color:#DDE6EE !important; font-size:1.18rem; max-width:52ch; margin:0; }}
.hero-credit {{ font-size:.78rem !important; color:#9FB2C3 !important; margin-top:1.2rem !important; }}

.stat {{ background:#fff; border:1px solid {LINE}; border-radius:4px; padding:1.2rem 1.3rem; border-top:3px solid {TEAL}; height:100%; }}
.stat .v {{ font-family:'Newsreader',serif; font-size:2.3rem; font-weight:700; color:{INK}; line-height:1.1; }}
.stat .l {{ font-size:.95rem; font-weight:600; color:{INK}; margin-top:.25rem; }}
.stat .n {{ font-size:.85rem; color:{MUTED}; line-height:1.5; margin-top:.2rem; }}
.stat.red {{ border-top-color:{FALU}; }} .stat.ochre {{ border-top-color:{OCHRE}; }}

.finding {{ background:#fff; border:1px solid {LINE}; border-left:5px solid {FALU}; border-radius:2px 14px 14px 2px; padding:1.2rem 1.5rem; margin:.8rem 0; }}
.finding b {{ font-family:'Newsreader',serif; font-size:1.2rem; color:{INK}; }}
.finding p {{ margin:.3rem 0 0 0; }}
.callout {{ background:#fff; border:1px solid {LINE}; border-radius:10px; padding:1rem 1.3rem; margin:1rem 0; }}
.callout.note {{ border-left:5px solid {OCHRE}; }}
.callout.ok {{ border-left:5px solid {TEAL}; }}
.callout.no {{ border-left:5px solid {FALU}; }}
.pull {{ font-family:'Newsreader',serif; font-style:italic; font-size:1.7rem; line-height:1.4; color:{INK}; margin:2.6rem 0; padding-left:1.6rem; border-left:4px solid {FALU}; max-width:34ch; }}

.photo {{ border-radius:4px; height:210px; background-size:cover; background-position:center; background-color:{LINE}; }}
.cap {{ font-size:.85rem !important; color:{MUTED} !important; margin-top:.5rem; line-height:1.5 !important; }}
.tag {{ display:inline-block; background:#fff; border:1px solid {LINE}; border-radius:999px; padding:.2rem .8rem; margin:.2rem .3rem .2rem 0; font-size:.88rem; color:{INK}; font-family:'Manrope',sans-serif; }}
.result {{ background:{INK}; border-radius:6px; padding:1.6rem 1.8rem; }}
.result .l {{ color:#9FB2C3; font-size:.95rem; }}
.result .v {{ font-family:'Newsreader',serif; color:#fff; font-size:3rem; font-weight:700; line-height:1.1; }}
.result .r {{ color:#DDE6EE; font-size:1rem; margin-top:.4rem; }}

[data-testid="stSidebar"] {{ background:#fff; border-right:1px solid {LINE}; }}
[data-testid="stSidebar"] .brand {{ font-family:'Newsreader',serif; font-size:1.5rem; font-weight:700; color:{INK}; line-height:1.2; }}
.stTabs [data-baseweb="tab"] {{ font-family:'Manrope',sans-serif; font-weight:600; }}
.stTabs [aria-selected="true"] {{ color:{FALU} !important; }}
.stTabs [data-baseweb="tab-highlight"] {{ background-color:{FALU} !important; }}
.js-plotly-plot {{ background:#fff; border:1px solid {LINE}; border-radius:6px; }}
.disc {{ font-size:.82rem !important; color:{MUTED} !important; font-style:italic; }}
@media (max-width:700px) {{ h1 {{ font-size:2.2rem !important; }} .hero-body {{ padding:1.6rem; }} }}
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# HELPERS
# -----------------------------------------------------------------------------
def html(s: str):
    """Render HTML safely (strips indentation/blank lines so markdown never treats it as code)."""
    st.markdown("".join(line.strip() for line in s.splitlines()), unsafe_allow_html=True)


def prose(s: str):
    html(f"<p class='prose'>{s}</p>")


def stat(label, value, note="", tone=""):
    return f"<div class='stat {tone}'><div class='v'>{value}</div><div class='l'>{label}</div><div class='n'>{note}</div></div>"


def finding(title, text):
    html(f"<div class='finding'><b>{title}</b><p>{text}</p></div>")


def callout(text, kind="note"):
    html(f"<div class='callout {kind}'>{text}</div>")


def photo(url, caption):
    return f"<div class='photo' style=\"background-image:url('{url}')\"></div><p class='cap'>{caption}</p>"


def style(fig, h=340, **kw):
    title = kw.pop("title", None)
    layout = dict(template="plotly_white", height=h, margin=dict(l=16, r=16, t=48, b=16),
                  font=dict(family="Manrope, sans-serif", color=INK, size=13),
                  paper_bgcolor="#fff", plot_bgcolor="#fff")
    layout.update(kw)
    if title is not None:
        layout["title"] = dict(text=title, font=dict(family="Newsreader, serif", size=18))
    fig.update_layout(**layout)
    return fig


def show(fig):
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def ci_plot(lo, est, hi, null, unit, title, h=150):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[lo, hi], y=[0, 0], mode="lines", line=dict(color=TEAL, width=10), hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=[est], y=[0], mode="markers", marker=dict(color=INK, size=14, line=dict(color="#fff", width=2)),
                             hovertemplate=f"estimate: {est}{unit}<extra></extra>"))
    if null is not None:
        fig.add_vline(x=null, line_dash="dash", line_color=FALU, annotation_text=f"H₀ = {null}{unit}", annotation_position="top")
    pad = (hi - lo) * 0.6
    fig.update_xaxes(range=[min(lo, null if null is not None else lo) - pad, max(hi, null if null is not None else hi) + pad], ticksuffix=unit)
    fig.update_yaxes(visible=False)
    style(fig, h, showlegend=False, title=title, margin=dict(l=16, r=16, t=56, b=24))
    return fig


# -----------------------------------------------------------------------------
# MODEL (fitted in R; coefficients copied from the final lm output)
# -----------------------------------------------------------------------------
B0, SIGMA = 13.8988571, 0.3525
REGION = {"Northeast": 0.0, "Northwest": 0.1850940, "Southeast": -0.1972418, "Stockholm": 0.3768469, "West": -0.4179828}
TYPE = {"Apartment": 0.0, "Terrace": -0.0762431, "Villa": 0.1829979}
BALC = {"No": 0.0, "Yes": -0.0697553}
B_ROOMS, B_AREA, B_INT = 0.1103812, 0.0138216, -0.0010429


def size_term(rooms, area):
    return B_ROOMS * rooms + B_AREA * area + B_INT * rooms * area


def predict_price(region, h_type, balcony, rooms, area):
    lp = B0 + REGION[region] + TYPE[h_type] + BALC[balcony] + size_term(rooms, area)
    return np.exp(lp), np.exp(lp - 1.96 * SIGMA), np.exp(lp + 1.96 * SIGMA)


# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
PAGES = ["Overview", "The data", "Hypothesis tests", "The model", "Valuation engine", "Held-out predictions", "Method & about"]
with st.sidebar:
    html("<div class='brand'>Stockholm<br>Real Estate Analytics</div>")
    st.caption("Statistical inference and regression modelling")
    page = st.radio("Navigate", PAGES, label_visibility="collapsed")
    st.markdown("---")
    html(f"<p style='font-size:.9rem;line-height:1.6'><b>{AUTHOR}</b><br>{TAGLINE}<br>"
         f"<a href='{GITHUB}' target='_blank'>GitHub</a> &nbsp;|&nbsp; <a href='{LINKEDIN}' target='_blank'>LinkedIn</a></p>")

# =============================================================================
# OVERVIEW
# =============================================================================
if page == "Overview":
    html(f"""
    <div class='hero'>
      <div class='hero-img' style="background-image:url('{IMG_HERO}')"></div>
      <div class='hero-shade'></div>
      <div class='hero-body'>
        <h1>What actually sets the price of a Stockholm home?</h1>
        <p>647 listings, four hypothesis tests and one log-linear regression, turned into a valuation tool you can use below.</p>
        <p class='hero-credit'>Gamla Stan, Stockholm. Photo: Unsplash</p>
      </div>
    </div>""")

    st.write("")
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(stat("Listings analysed", "647", "Stockholm County, 5 regions"), unsafe_allow_html=True)
    c2.markdown(stat("Variance explained", "61.1%", "Final model R², up from 38.5% with area alone", "red"), unsafe_allow_html=True)
    c3.markdown(stat("Median price", "3.49M", "SEK. The mean is 4.27M, pulled up by 32 outliers", "ochre"), unsafe_allow_html=True)
    c4.markdown(stat("Location premium", "+46%", "Stockholm city vs Northeast, all else equal"), unsafe_allow_html=True)

    st.markdown("## The question")
    prose("Buying a home in Stockholm is one of the largest financial decisions most people make, and the price often feels "
          "like a black box. Why does a flat in the city cost far more than a similar one in the suburbs? "
          "I wanted answers I could defend with numbers rather than intuition.")
    prose("<b>The approach.</b> I tested common beliefs about the market with formal hypothesis tests, then built a regression that "
          "isolates each factor's effect on price. When the first model broke its own assumptions, I diagnosed the problem, "
          "transformed the response, and re-validated, rather than reporting the first number that looked good.")

    st.markdown("## Three things the data says")
    finding("Location is the biggest lever", "Holding size and type constant, a Stockholm city listing sells for about 46% more than the Northeast reference region. "
            "A West-region listing sells for about 34% less.")
    finding("Size matters, but with diminishing returns", "The Rooms × Area interaction is negative: an extra square metre is worth less in a home that already has many rooms. "
            "At 3 rooms, each extra m² adds roughly 1.1% to price.")
    finding("The price distribution is heavily skewed", "Skewness is 2.06. That is why a log transform was needed to fix the funnel-shaped residuals "
            "of the first linear model.")

    html("<div class='pull'>A model that hides its uncertainty is not a model worth trusting.</div>")

    st.markdown("## The market in pictures")
    p1, p2, p3 = st.columns(3)
    p1.markdown(photo(IMG_A, "Apartments make up about 80% of listings."), unsafe_allow_html=True)
    p2.markdown(photo(IMG_B, "Villas carry a premium of about 20% over apartments."), unsafe_allow_html=True)
    p3.markdown(photo(IMG_C, "Rooms and area interact: size effects fade as homes grow."), unsafe_allow_html=True)

# =============================================================================
# THE DATA
# =============================================================================
elif page == "The data":
    st.markdown("# The data")
    prose("Before modelling, I looked at the shape of the data. Three questions drove the exploration: "
          "what kinds of homes are on the market, how big are they, and how does price relate to size?")
    callout("<b>Note on charts.</b> The charts on this page are illustrative reconstructions that match the summary statistics "
            "of the real dataset (counts, mean, median, correlation). They are not the raw records.", "note")

    st.markdown("### What is for sale, and where")
    prose("Apartments are about 80% of the market (518 of 647 listings). Stockholm city has the most listings, "
          "and villas are rarer but more evenly spread across regions.")
    regions = ["Stockholm", "Northwest", "Northeast", "Southeast", "West"]
    counts = {"Apartment": [190, 120, 95, 65, 48], "Terrace": [12, 12, 14, 10, 7], "Villa": [14, 18, 20, 12, 10]}
    fig = go.Figure()
    for (t, vals), col in zip(counts.items(), [TEAL, OCHRE, FALU]):
        fig.add_bar(name=t, x=regions, y=vals, marker_color=col)
    style(fig, 340, barmode="stack", title="Listings by region and housing type", legend=dict(orientation="h", y=1.12, x=0))
    show(fig)

    st.markdown("### Price is skewed, which shapes everything after")
    prose("The mean (4.27M SEK) sits well above the median (3.49M SEK) because of a long right tail of luxury listings. "
          "Taking logs makes the distribution close to symmetric, which is why the final model works on log(price).")
    rng = np.random.default_rng(7)
    price = np.exp(rng.normal(np.log(3.49e6), 0.634, 647))
    a, b = st.columns(2)
    f1 = go.Figure(go.Histogram(x=price / 1e6, nbinsx=40, marker_color=TEAL))
    f1.add_vline(x=3.49, line_color=FALU, line_dash="dash", annotation_text="median")
    f1.update_xaxes(title="Price (M SEK)")
    style(f1, 300, title="Raw price: right-skewed", showlegend=False)
    f2 = go.Figure(go.Histogram(x=np.log(price), nbinsx=40, marker_color=OCHRE))
    f2.update_xaxes(title="log(price)")
    style(f2, 300, title="Log price: close to symmetric", showlegend=False)
    with a: show(f1)
    with b: show(f2)

    st.markdown("### Size and price")
    prose("The Pearson correlation between area and starting price is <b>0.62</b>. Area alone explains 38.5% of the variance, "
          "so size is important but far from the whole story.")
    area = np.clip(rng.lognormal(np.log(70), 0.45, 300), 15, 250)
    lp = 14.0 + 0.0125 * area + rng.normal(0, 0.4, 300)
    slope, icpt = np.polyfit(area, lp, 1)
    xs = np.linspace(area.min(), area.max(), 50)
    f3 = go.Figure()
    f3.add_trace(go.Scatter(x=area, y=np.exp(lp) / 1e6, mode="markers", marker=dict(color=TEAL, opacity=.45, size=7), name="Listings"))
    f3.add_trace(go.Scatter(x=xs, y=np.exp(icpt + slope * xs) / 1e6, mode="lines", line=dict(color=FALU, width=3), name="Trend"))
    f3.update_xaxes(title="Area (m²)")
    f3.update_yaxes(title="Price (M SEK, log scale)", type="log")
    style(f3, 380, title="Area vs price (illustrative)", legend=dict(orientation="h", y=1.12, x=0))
    show(f3)

# =============================================================================
# HYPOTHESIS TESTS
# =============================================================================
elif page == "Hypothesis tests":
    st.markdown("# Hypothesis tests")
    prose("Four questions about the market, each answered with a formal test or confidence interval. "
          "The R output is shown next to a plain-language reading of it.")
    t1, t2, t3, t4 = st.tabs(["Balconies", "Average area", "Apartment share", "Number of rooms"])

    with t1:
        st.markdown("### Are balconies more common than not?")
        st.latex(r"H_0: p = 0.5 \quad \text{vs} \quad H_1: p \neq 0.5")
        c1, c2 = st.columns([1, 1])
        with c1:
            st.code("prop.test(x = has_bal, n = 647, p = 0.5, conf.level = 0.99)\n"
                    "# X-squared = 18.028, p-value = 2.177e-05\n"
                    "# 99% CI: 0.5329 to 0.6337\n"
                    "# sample estimate: p = 0.5842", language="r")
        with c2:
            callout("<b>Reject H₀.</b> With p ≈ 0.00002, far below 0.01, balconies are more common than a coin flip. "
                    "We are 99% confident that between 53.3% and 63.4% of homes have one.", "no")
        show(ci_plot(53.29, 58.42, 63.37, 50, "%", "99% CI for the share of homes with a balcony"))

    with t2:
        st.markdown("### Is the average home 75 m²?")
        st.latex(r"H_0: \mu = 75 \quad \text{vs} \quad H_1: \mu \neq 75")
        c1, c2 = st.columns([1, 1])
        with c1:
            st.code("t.test(DataSet$AREA, mu = 75, conf.level = 0.95)\n"
                    "# t = 1.3775, p-value = 0.1688\n"
                    "# 95% CI: 74.16 to 79.76\n"
                    "# sample mean = 76.96 m²", language="r")
        with c2:
            callout("<b>Fail to reject H₀.</b> p = 0.169 is above 0.05 and the interval contains 75 m². "
                    "The data are consistent with a 75 m² average. That is not proof it is exactly 75.", "ok")
        show(ci_plot(74.16, 76.96, 79.76, 75, " m²", "95% CI for mean area"))

    with t3:
        st.markdown("### What share of listings are apartments?")
        c1, c2 = st.columns([1, 1])
        with c1:
            st.code("prop.test(sum(TYPE == 'Apartment'), n = 647, conf.level = 0.90)\n"
                    "# 90% CI: 0.7727 to 0.8259\n"
                    "# sample estimate: p = 0.8006", language="r")
        with c2:
            callout("We are 90% confident that between <b>77.3% and 82.6%</b> of Stockholm County listings are apartments.", "ok")
        show(ci_plot(77.27, 80.06, 82.59, None, "%", "90% CI for the apartment share"))

    with t4:
        st.markdown("### How many rooms does a typical home have?")
        c1, c2 = st.columns([1, 1])
        with c1:
            st.code("t.test(DataSet$ROOMS, conf.level = 0.95)\n"
                    "# 95% CI: 2.942 to 3.166\n"
                    "# sample mean = 3.054 rooms", language="r")
        with c2:
            callout("The sample mean is 3.05 rooms. We are 95% confident that the true average lies between <b>2.94 and 3.17</b>.", "ok")
        show(ci_plot(2.942, 3.054, 3.166, None, "", "95% CI for mean number of rooms"))

# =============================================================================
# THE MODEL
# =============================================================================
elif page == "The model":
    st.markdown("# The model")
    st.markdown("## Three iterations")
    prose("Each model fixed a specific weakness in the one before it.")
    fig = go.Figure(go.Bar(x=["1. Area only", "2. Multiple regression", "3. Log price + interaction"], y=[0.385, 0.563, 0.6113],
                           marker_color=[LINE, OCHRE, TEAL], text=["0.385", "0.563", "0.611"], textposition="outside"))
    fig.update_yaxes(range=[0, 0.8], title="R²")
    style(fig, 320, title="Variance explained at each step", showlegend=False)
    show(fig)

    finding("Step 1: area only", "R² of 0.385. Size matters but cannot carry the model alone.")
    finding("Step 2: add region, type, balcony and rooms", "R² rises to 0.563, but the residuals fan out as fitted values grow (a funnel). "
            "That violates constant variance, so the standard errors and prediction intervals cannot be trusted.")
    finding("Step 3: log-transform price, add Rooms × Area", "R² reaches 0.611 and the diagnostics look healthy. "
            "Residual standard error is 0.3525 on the log scale.")

    st.markdown("### Why the log transform worked")
    callout("<b>Illustrative diagnostics.</b> These two plots reproduce the pattern seen in the real residual plots. They are simulated, not the actual residuals.", "note")
    rng = np.random.default_rng(3)
    fitted = np.linspace(2, 10, 160)
    a, b = st.columns(2)
    f1 = go.Figure(go.Scatter(x=fitted, y=rng.normal(0, fitted * 0.18, 160), mode="markers", marker=dict(color=FALU, opacity=.6)))
    f1.add_hline(y=0, line_dash="dash", line_color=INK)
    f1.update_xaxes(title="Fitted values"); f1.update_yaxes(title="Residuals")
    style(f1, 320, title="Before: funnel shape", showlegend=False)
    f2 = go.Figure(go.Scatter(x=fitted, y=rng.normal(0, 1.2, 160), mode="markers", marker=dict(color=TEAL, opacity=.6)))
    f2.add_hline(y=0, line_dash="dash", line_color=INK)
    f2.update_xaxes(title="Fitted values"); f2.update_yaxes(title="Residuals")
    style(f2, 320, title="After: even spread", showlegend=False)
    with a: show(f1)
    with b: show(f2)

    st.markdown("## What each factor is worth")
    prose("Because the response is log(price), a coefficient β translates to a percentage effect of (e<sup>β</sup> − 1). "
          "Effects below are relative to a Northeast apartment with no balcony.")
    labels, vals = [], []
    for k, v in REGION.items():
        if v: labels.append(f"Region: {k}"); vals.append((np.exp(v) - 1) * 100)
    for k, v in TYPE.items():
        if v: labels.append(f"Type: {k}"); vals.append((np.exp(v) - 1) * 100)
    labels.append("Balcony: yes"); vals.append((np.exp(BALC["Yes"]) - 1) * 100)
    order = np.argsort(vals)
    fig = go.Figure(go.Bar(x=[vals[i] for i in order], y=[labels[i] for i in order], orientation="h",
                           marker_color=[TEAL if vals[i] > 0 else FALU for i in order],
                           text=[f"{vals[i]:+.1f}%" for i in order], textposition="outside"))
    fig.update_xaxes(title="Effect on price (%)", range=[-45, 60], zeroline=True, zerolinecolor=INK)
    style(fig, 360, title="Effect on price vs the reference home", showlegend=False)
    show(fig)
    callout("<b>A result worth questioning.</b> The balcony coefficient is negative (about −6.7%). That is probably not causal. "
            "Balconies may be more common in cheaper or older buildings, so the sign likely reflects what else comes with them. "
            "This is the kind of result I would investigate with building-age data before drawing conclusions.", "note")

    st.markdown("### The final equation")
    st.latex(r"\log(\text{Price}) = 13.899 + \beta_{\text{region}} + \beta_{\text{type}} + 0.110\,\text{Rooms} - 0.070\,\text{Balcony} + 0.014\,\text{Area} - 0.001\,(\text{Rooms}\times\text{Area})")
    prose("At the 5% level, Region, Type (Villa), Rooms, Balcony, Area and the interaction term are significant.")

# =============================================================================
# VALUATION ENGINE
# =============================================================================
elif page == "Valuation engine":
    st.markdown("# Valuation engine")
    prose("Describe a home and the model returns an estimated starting price with a 95% prediction interval. "
          "The chart below shows how each feature moves the estimate.")

    c1, c2 = st.columns(2)
    with c1:
        region = st.selectbox("Region", list(REGION))
        h_type = st.selectbox("Housing type", list(TYPE))
        balcony = st.radio("Balcony", list(BALC), horizontal=True)
    with c2:
        area = st.slider("Area (m²)", 15, 250, 75)
        rooms = st.slider("Rooms", 1.0, 8.0, 3.0, 0.5)

    price, lo, hi = predict_price(region, h_type, balcony, rooms, area)
    median = 3.49e6
    diff = (price / median - 1) * 100
    html(f"""
    <div class='result'>
      <div class='l'>Estimated starting price</div>
      <div class='v'>{price:,.0f} SEK</div>
      <div class='r'>95% prediction interval: {lo:,.0f} to {hi:,.0f} SEK. That is {abs(diff):.0f}% {"above" if diff >= 0 else "below"} the market median.</div>
    </div>""")

    st.write("")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[lo / 1e6, hi / 1e6], y=[0, 0], mode="lines", line=dict(color=TEAL, width=14), hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=[price / 1e6], y=[0], mode="markers", marker=dict(color=INK, size=18, line=dict(color="#fff", width=3)), hoverinfo="skip"))
    fig.add_vline(x=median / 1e6, line_dash="dash", line_color=FALU, annotation_text="market median", annotation_position="top")
    fig.update_yaxes(visible=False)
    fig.update_xaxes(title="Price (M SEK)", rangemode="tozero")
    style(fig, 180, showlegend=False, title="Where this home sits", margin=dict(l=16, r=16, t=56, b=40))
    show(fig)

    st.markdown("### How the estimate is built")
    prose("Starting from the model's baseline, each group of features is applied in turn. "
          "Because effects multiply, the SEK amounts depend on the order shown.")
    steps = [("Size (area, rooms, interaction)", size_term(rooms, area)), ("Region", REGION[region]),
             ("Housing type", TYPE[h_type]), ("Balcony", BALC[balcony])]
    cum, prev, names, deltas = B0, np.exp(B0), ["Baseline"], [np.exp(B0)]
    for n, v in steps:
        cum += v
        new = np.exp(cum)
        names.append(n); deltas.append(new - prev); prev = new
    names.append("Estimate"); deltas.append(prev)
    fig = go.Figure(go.Waterfall(x=names, y=[d / 1e6 for d in deltas], measure=["absolute"] + ["relative"] * 4 + ["absolute"],
                                 increasing=dict(marker=dict(color=TEAL)), decreasing=dict(marker=dict(color=FALU)),
                                 totals=dict(marker=dict(color=INK)), connector=dict(line=dict(color=LINE)),
                                 text=[f"{d/1e6:+.2f}M" if 0 < i < 5 else f"{d/1e6:.2f}M" for i, d in enumerate(deltas)],
                                 textposition="outside"))
    fig.update_yaxes(title="M SEK")
    style(fig, 400, title="Feature contributions", showlegend=False)
    show(fig)
    st.markdown("<p class='disc'>Intervals are wide by design: the model's residual standard error of 0.3525 on the log scale means a typical "
                "95% interval runs from about half to about double the point estimate.</p>", unsafe_allow_html=True)

# =============================================================================
# HELD-OUT PREDICTIONS
# =============================================================================
elif page == "Held-out predictions":
    st.markdown("# Held-out predictions")
    prose("The final model was applied to six properties that were not used for fitting. "
          "The fitted price and 95% prediction interval for each are below.")
    df = pd.DataFrame({
        "ID": [629, 718, 1534, 1695, 1864, 2138],
        "Region": ["Northwest", "Northeast", "Stockholm", "Stockholm", "Stockholm", "Northeast"],
        "Rooms": [3, 4, 6, 2, 1, 2],
        "Area (m²)": [74.0, 99.5, 115.0, 45.0, 29.0, 47.5],
        "Balcony": ["Yes", "Yes", "Yes", "No", "No", "Yes"],
        "Fit": [3747555, 4117685, 6838775, 3350357, 2562945, 2207375],
        "Lower": [1864607, 2051409, 3392129, 1672540, 1277154, 1100005],
        "Upper": [7531971, 8265212, 13787459, 6711286, 5143222, 4429530],
    })
    fig = go.Figure()
    for i, r in df.iterrows():
        fig.add_trace(go.Scatter(x=[r.Lower / 1e6, r.Upper / 1e6], y=[f"#{r.ID} · {r.Region}"] * 2, mode="lines",
                                 line=dict(color=TEAL, width=9), hoverinfo="skip", showlegend=False))
        fig.add_trace(go.Scatter(x=[r.Fit / 1e6], y=[f"#{r.ID} · {r.Region}"], mode="markers", marker=dict(color=INK, size=13, line=dict(color="#fff", width=2)),
                                 hovertemplate="fit: %{x:.2f}M SEK<extra></extra>", showlegend=False))
    fig.update_xaxes(title="Price (M SEK, log scale)", type="log")
    fig.update_yaxes(autorange="reversed")
    style(fig, 380, title="Predicted price with 95% prediction interval")
    show(fig)

    st.dataframe(df.style.format({"Fit": "{:,.0f}", "Lower": "{:,.0f}", "Upper": "{:,.0f}"}), use_container_width=True, hide_index=True)
    html("<div class='pull'>Wide intervals are an honest answer: a single listing is genuinely hard to price.</div>")
    callout("<b>Limitation.</b> Prediction intervals here assume normal, constant-variance residuals on the log scale. "
            "With only six held-out points, I would not claim coverage rates. A proper check needs cross-validation on a larger test set.", "note")

# =============================================================================
# METHOD & ABOUT
# =============================================================================
else:
    st.markdown("# Method and about")
    st.markdown("## Method")
    prose("Analysis was done in R (<code>prop.test</code>, <code>t.test</code>, <code>lm</code>) on 647 Stockholm County listings. "
          "This app presents the results and reimplements the final model in Python for the interactive valuation tool.")
    html("".join(f"<span class='tag'>{t}</span>" for t in
                 ["Hypothesis testing", "Confidence intervals", "Multiple linear regression", "Log transformation", "Interaction terms",
                  "Residual diagnostics", "Prediction intervals", "R", "Python", "Streamlit", "Plotly"]))

    st.markdown("## What I would do next")
    finding("Validate out of sample", "Replace the six-point check with k-fold cross-validation and report RMSE and interval coverage.")
    finding("Add spatial information", "Region is coarse. Distance to the centre or to transit, or a hierarchical model with region as a random effect, should help.")
    finding("Try regularised and tree-based models", "Compare against ridge/lasso and gradient boosting, and explain the boosted model with SHAP.")

    st.markdown("## About")
    st.markdown("<p class='prose'>I am a data scientist finishing an MSc in Data Science at Stockholm University. "
                "This project shows how I approach a problem: test assumptions, fix the model when diagnostics fail, and report uncertainty honestly.</p>",
                unsafe_allow_html=True)
    html(f"<p><b>{AUTHOR}</b><br><a href='{GITHUB}' target='_blank'>GitHub</a> &nbsp;|&nbsp; <a href='{LINKEDIN}' target='_blank'>LinkedIn</a></p>")
