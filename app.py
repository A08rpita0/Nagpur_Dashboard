import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np
import time

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Nagpur Property Intelligence",
    page_icon="🏙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# CUSTOM CSS — Dark futuristic theme
# ---------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --bg-deep:    #050A14;
    --bg-card:    #0B1422;
    --bg-panel:   #0F1C30;
    --accent-1:   #00FFD1;
    --accent-2:   #FF5F40;
    --accent-3:   #FFD60A;
    --txt-main:   #E8F0F7;
    --txt-muted:  #6B8299;
    --border:     rgba(0,255,209,0.15);
    --glow:       0 0 24px rgba(0,255,209,0.25);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg-deep) !important;
    color: var(--txt-main) !important;
}

.hero-header {
    background: linear-gradient(135deg, #050A14 0%, #0B1F3A 60%, #050A14 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 40px 48px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
    box-shadow: var(--glow);
}
.hero-header::before {
    content: '';
    position: absolute; inset: 0;
    background:
        repeating-linear-gradient(90deg, transparent, transparent 60px, rgba(0,255,209,0.03) 60px, rgba(0,255,209,0.03) 61px),
        repeating-linear-gradient(0deg,  transparent, transparent 60px, rgba(0,255,209,0.03) 60px, rgba(0,255,209,0.03) 61px);
    pointer-events: none;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 56px; letter-spacing: 4px;
    color: var(--txt-main); margin: 0; line-height: 1;
}
.hero-title span { color: var(--accent-1); }
.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px; color: var(--accent-1);
    letter-spacing: 3px; margin-top: 10px; text-transform: uppercase;
}
.hero-badge {
    display: inline-block;
    background: rgba(0,255,209,0.08); border: 1px solid var(--accent-1);
    color: var(--accent-1); font-family: 'JetBrains Mono', monospace;
    font-size: 11px; padding: 4px 12px; border-radius: 20px;
    margin-top: 16px; letter-spacing: 2px;
}

/* METRIC CARDS */
.metric-row { display: flex; gap: 16px; margin-bottom: 32px; flex-wrap: wrap; }
.metric-card {
    flex: 1; min-width: 180px;
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 12px; padding: 24px 28px;
    position: relative; overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}
.metric-card:hover { transform: translateY(-3px); box-shadow: var(--glow); }
.metric-card::after {
    content: ''; position: absolute; top: 0; left: 0; right: 0;
    height: 3px; border-radius: 12px 12px 0 0;
}
.metric-card.cyan::after   { background: var(--accent-1); }
.metric-card.coral::after  { background: var(--accent-2); }
.metric-card.gold::after   { background: var(--accent-3); }
.metric-card.blue::after   { background: #4FA3FF; }
.metric-card.purple::after { background: #C77DFF; }
.metric-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; letter-spacing: 2px;
    color: var(--txt-muted); text-transform: uppercase; margin-bottom: 8px;
}
.metric-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 36px; letter-spacing: 2px; line-height: 1;
}
.metric-value.cyan   { color: var(--accent-1); }
.metric-value.coral  { color: var(--accent-2); }
.metric-value.gold   { color: var(--accent-3); }
.metric-value.blue   { color: #4FA3FF; }
.metric-value.purple { color: #C77DFF; }
.metric-delta { font-size: 12px; color: var(--txt-muted); margin-top: 4px; }

/* SECTION HEADERS */
.section-header { display: flex; align-items: center; gap: 14px; margin: 40px 0 20px; }
.section-line   { flex: 1; height: 1px; background: linear-gradient(90deg, var(--accent-1), transparent); }
.section-title  { font-family: 'Bebas Neue', sans-serif; font-size: 22px; letter-spacing: 4px; color: var(--txt-main); white-space: nowrap; }
.section-icon   { font-size: 18px; }

/* INFO BOX */
.info-box {
    background: rgba(0,255,209,0.05); border: 1px solid rgba(0,255,209,0.2);
    border-left: 3px solid var(--accent-1); border-radius: 8px;
    padding: 14px 18px; margin-bottom: 20px;
    font-size: 13px; color: var(--txt-muted);
    font-family: 'JetBrains Mono', monospace; letter-spacing: 0.5px;
}

/* TABLES */
.stDataFrame { background: var(--bg-card) !important; }
.stDataFrame table { font-family: 'DM Sans', sans-serif !important; font-size: 13px !important; }

/* SIDEBAR */
section[data-testid="stSidebar"] { background: var(--bg-panel) !important; border-right: 1px solid var(--border); }
section[data-testid="stSidebar"] * { color: var(--txt-main) !important; }
.sidebar-logo {
    font-family: 'Bebas Neue', sans-serif; font-size: 24px; letter-spacing: 3px;
    color: var(--accent-1); padding: 8px 0 20px;
    border-bottom: 1px solid var(--border); margin-bottom: 20px;
}
.sidebar-section {
    font-family: 'JetBrains Mono', monospace; font-size: 10px;
    letter-spacing: 2px; color: var(--txt-muted);
    text-transform: uppercase; margin: 20px 0 8px;
}

/* MISC */
.divider { height: 1px; background: linear-gradient(90deg, transparent, var(--border), transparent); margin: 32px 0; }
.plotly-container { background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 8px; margin-bottom: 24px; }
.stSelectbox > div > div,
.stMultiSelect > div > div { background: var(--bg-panel) !important; border-color: var(--border) !important; color: var(--txt-main) !important; }

/* FOOTER */
.dashboard-footer {
    text-align: center; font-family: 'JetBrains Mono', monospace;
    font-size: 11px; color: var(--txt-muted); letter-spacing: 2px;
    padding: 32px 0 16px; border-top: 1px solid var(--border); margin-top: 48px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# PLOTLY THEME
# ---------------------------------------------------

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(11,20,34,0)",
    plot_bgcolor="rgba(11,20,34,0)",
    font=dict(family="DM Sans, sans-serif", color="#E8F0F7", size=12),
    xaxis=dict(showgrid=False, showline=True, linecolor="rgba(0,255,209,0.2)", tickfont=dict(size=11)),
    yaxis=dict(gridcolor="rgba(0,255,209,0.07)", showline=False, tickfont=dict(size=11)),
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(bgcolor="rgba(11,20,34,0.8)", bordercolor="rgba(0,255,209,0.2)", borderwidth=1),
    colorway=["#00FFD1", "#FF5F40", "#FFD60A", "#4FA3FF", "#C77DFF", "#F72585"],
)
ACCENT_SEQ = ["#050A14", "#003D33", "#007A60", "#00B48C", "#00FFD1"]

# ---------------------------------------------------
# SCHEDULED AUTO-REFRESH (every 60 minutes)
# ---------------------------------------------------

REFRESH_INTERVAL = 3600
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

elapsed = time.time() - st.session_state.last_refresh
if elapsed > REFRESH_INTERVAL:
    st.session_state.last_refresh = time.time()
    st.cache_data.clear()
    st.rerun()

# ---------------------------------------------------
# CACHING STRATEGY — TTL matches refresh interval
# ---------------------------------------------------

@st.cache_data(ttl=3600, show_spinner="Loading data…")
def load_data():
    return pd.read_csv("nagpur_cleaned_dataset.csv")

df = load_data()

if df.empty:
    st.error("Dataset is empty. Please check your data source.")
    st.stop()

# ---------------------------------------------------
# SAFETY CHECKS & COLUMN PREP
# ---------------------------------------------------

required_cols = ["locality", "growth_1y", "growth_3y"]
for col in required_cols:
    if col not in df.columns:
        st.error(f"Missing required column: **{col}**")
        st.stop()

# Keep growth_5y in backend for model only — not shown in UI
if "growth_5y" not in df.columns:
    df["growth_5y"] = 0.0

# Auto-generate price segment if missing
if "segment" not in df.columns:
    if "price_per_sqft" in df.columns:
        df["segment"] = pd.cut(df["price_per_sqft"], bins=3,
                                labels=["Affordable", "Mid-Range", "Premium"])
    else:
        df["segment"] = pd.qcut(df["growth_3y"].rank(method="first"), q=3,
                                  labels=["Affordable", "Mid-Range", "Premium"])

# ---------------------------------------------------
# FEATURE ENGINEERING
# ---------------------------------------------------

# Volatility — std across 1Y & 3Y only (no 5Y in UI)
df["volatility"] = df[["growth_1y", "growth_3y"]].std(axis=1)

# Investment score — weighted blend of 1Y + 3Y
df["investment_score"] = (
    0.6 * df["growth_1y"] +
    0.4 * df["growth_3y"]
)
df["rank"] = df["investment_score"].rank(ascending=False).astype(int)

# ---------------------------------------------------
# BASIC PRICE GROWTH PREDICTION MODEL
# Linear Regression using 1Y + 3Y features
# ---------------------------------------------------

features = ["growth_1y", "growth_3y"]
X = df[features].fillna(0)
y = df["growth_1y"]

model = LinearRegression()
model.fit(X, y)

df["predicted_growth_next_year"] = model.predict(X).round(2)
r2_score = model.score(X, y)

# ---------------------------------------------------
# INVESTMENT RECOMMENDATION LOGIC
# Multi-tier system using predicted growth + volatility
# ---------------------------------------------------

def recommend(row):
    pg  = row["predicted_growth_next_year"]
    vol = row["volatility"]
    if pg > 15 and vol < 10:
        return "🚀 Strong Buy"
    elif pg > 15 and vol >= 10:
        return "📈 High Growth / High Risk"
    elif pg > 5:
        return "📊 Moderate Buy"
    elif pg > 0:
        return "⏸ Hold"
    else:
        return "⚠ Avoid"

df["recommendation"] = df.apply(recommend, axis=1)

# Bubble size — must be strictly positive for scatter plot
score_min = df["investment_score"].min()
score_max = df["investment_score"].max()
df["bubble_size"] = ((df["investment_score"] - score_min) / (score_max - score_min + 1e-9) * 99 + 1)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:
    st.markdown('<div class="sidebar-logo">🏙 NAGPUR<br>INTEL</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Locality Filter</div>', unsafe_allow_html=True)
    selected_localities = st.multiselect(
        "Localities", options=sorted(df["locality"].unique()),
        label_visibility="collapsed", placeholder="All localities"
    )

    st.markdown('<div class="sidebar-section">Growth Window</div>', unsafe_allow_html=True)
    duration_labels = {"1 Year": "growth_1y", "3 Years": "growth_3y"}
    duration_choice = st.radio("Growth Duration", list(duration_labels.keys()), label_visibility="collapsed")
    selected_duration = duration_labels[duration_choice]

    st.markdown('<div class="sidebar-section">Signal Filter</div>', unsafe_allow_html=True)
    all_recs = sorted(df["recommendation"].unique())
    selected_recs = st.multiselect("Signal", options=all_recs, default=all_recs, label_visibility="collapsed")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    mins_since = int(elapsed / 60)
    st.markdown(
        f"<span style='font-family:JetBrains Mono,monospace;font-size:11px;color:#6B8299;line-height:2;'>"
        f"RECORDS: {len(df)}<br>LAST REFRESH: {mins_since}m ago<br>"
        f"MODEL R²: {r2_score:.3f}<br>CACHE TTL: 60 MIN</span>",
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Force Refresh"):
        st.cache_data.clear()
        st.session_state.last_refresh = time.time()
        st.rerun()

# Apply filters
df_filtered = df.copy()
if selected_localities:
    df_filtered = df_filtered[df_filtered["locality"].isin(selected_localities)]
if selected_recs:
    df_filtered = df_filtered[df_filtered["recommendation"].isin(selected_recs)]

# ---------------------------------------------------
# HERO HEADER
# ---------------------------------------------------

st.markdown("""
<div class="hero-header">
    <div class="hero-title">NAGPUR <span>PROPERTY</span> INTELLIGENCE</div>
    <div class="hero-sub">Real Estate Analytics Platform · Nagpur, Maharashtra</div>
    <div class="hero-badge">● LIVE DASHBOARD · AUTO-REFRESH ENABLED</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# KPI METRICS ROW
# ---------------------------------------------------

top_locality  = df_filtered.loc[df_filtered["investment_score"].idxmax(), "locality"] if not df_filtered.empty else "—"
avg_1y        = df_filtered["growth_1y"].mean()
avg_3y        = df_filtered["growth_3y"].mean()
strong_buys   = (df_filtered["recommendation"] == "🚀 Strong Buy").sum()
high_risk_cnt = (df_filtered["volatility"] > df_filtered["volatility"].quantile(0.75)).sum()
total_loc     = len(df_filtered)

st.markdown(f"""
<div class="metric-row">
    <div class="metric-card cyan">
        <div class="metric-label">Avg 1Y Growth</div>
        <div class="metric-value cyan">{avg_1y:.1f}%</div>
        <div class="metric-delta">Year-on-year average</div>
    </div>
    <div class="metric-card blue">
        <div class="metric-label">Avg 3Y Growth</div>
        <div class="metric-value blue">{avg_3y:.1f}%</div>
        <div class="metric-delta">3-year average CAGR</div>
    </div>
    <div class="metric-card gold">
        <div class="metric-label">Strong Buy Zones</div>
        <div class="metric-value gold">{strong_buys}</div>
        <div class="metric-delta">Low risk · high predicted growth</div>
    </div>
    <div class="metric-card coral">
        <div class="metric-label">High-Risk Areas</div>
        <div class="metric-value coral">{high_risk_cnt}</div>
        <div class="metric-delta">Top quartile volatility</div>
    </div>
    <div class="metric-card purple">
        <div class="metric-label">Model R²</div>
        <div class="metric-value purple">{r2_score:.2f}</div>
        <div class="metric-delta">Linear regression fit score</div>
    </div>
    <div class="metric-card cyan">
        <div class="metric-label">Top Locality</div>
        <div class="metric-value cyan" style="font-size:20px;letter-spacing:1px;">{top_locality}</div>
        <div class="metric-delta">Highest investment score</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ===================================================
# SECTION 1: LOCALITY-WISE PRICE GROWTH COMPARISON
# ===================================================

st.markdown("""
<div class="section-header">
    <span class="section-icon">📊</span>
    <span class="section-title">LOCALITY-WISE PRICE GROWTH COMPARISON</span>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    f'<div class="info-box">Showing <b>{selected_duration.replace("growth_","").upper()}</b> '
    f'growth for <b>{len(df_filtered)}</b> localities — sorted by growth rate. '
    f'Use the sidebar to filter by locality or signal.</div>',
    unsafe_allow_html=True
)

_loc_df = df_filtered.sort_values(selected_duration, ascending=True).copy()
_vals = _loc_df[selected_duration].values
_vmin, _vmax = _vals.min(), _vals.max()
_span = _vmax - _vmin if _vmax != _vmin else 1

def _val_to_color(v):
    t = (v - _vmin) / _span
    if t < 0.5:
        r = int(255 + (255 - 255) * (t / 0.5))
        g = int(95  + (214 - 95)  * (t / 0.5))
        b = int(64  + (10  - 64)  * (t / 0.5))
    else:
        t2 = (t - 0.5) / 0.5
        r = int(255 + (0   - 255) * t2)
        g = int(214 + (255 - 214) * t2)
        b = int(10  + (209 - 10)  * t2)
    return f"rgb({r},{g},{b})"

_colors = [_val_to_color(v) for v in _vals]
_texts  = [f"{v:.1f}%" for v in _vals]

fig_locality = go.Figure(go.Bar(
    x=_vals,
    y=_loc_df["locality"],
    orientation="h",
    marker=dict(color=_colors, line_width=0),
    text=_texts,
    textposition="outside",
    textfont=dict(size=11, color="#E8F0F7"),
    cliponaxis=False,
    hovertemplate="<b>%{y}</b><br>Growth: %{x:.1f}%<extra></extra>",
))
fig_locality.update_layout(**{
    **PLOTLY_LAYOUT,
    "height": max(320, len(df_filtered) * 34),
    "margin": dict(l=20, r=80, t=40, b=20),
    "xaxis": dict(showgrid=False, showline=False, showticklabels=False, title=""),
    "yaxis": dict(showgrid=False, showline=False, tickfont=dict(size=11)),
    "showlegend": False,
})

st.markdown('<div class="plotly-container">', unsafe_allow_html=True)
st.plotly_chart(fig_locality, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ===================================================
# SECTION 2: TOP 5 FASTEST GROWING + LOWEST PERFORMING
# ===================================================

st.markdown("""
<div class="section-header">
    <span class="section-icon">🏆</span>
    <span class="section-title">TOP 5 FASTEST GROWING vs LOWEST PERFORMING</span>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        "<span style='font-family:JetBrains Mono,monospace;font-size:11px;"
        "color:#00FFD1;letter-spacing:2px;'>▲ TOP 5 FASTEST GROWING</span>",
        unsafe_allow_html=True
    )
    top5 = df_filtered.sort_values(selected_duration, ascending=False).head(5)
    fig_top = go.Figure(go.Bar(
        x=top5[selected_duration], y=top5["locality"], orientation="h",
        marker=dict(color=top5[selected_duration],
                    colorscale=[[0, "#007A60"], [1, "#00FFD1"]], line_width=0),
        text=top5[selected_duration].apply(lambda v: f"{v:.1f}%"),
        textposition="outside", textfont=dict(color="#00FFD1", size=11)
    ))
    fig_top.update_layout(**{**PLOTLY_LAYOUT, "height": 280, "margin": dict(l=10, r=70, t=20, b=10)})
    st.plotly_chart(fig_top, use_container_width=True)
    st.dataframe(
        top5[["locality", "growth_1y", "growth_3y", "recommendation"]]
        .rename(columns={"locality": "Locality", "growth_1y": "1Y%",
                         "growth_3y": "3Y%", "recommendation": "Signal"}),
        use_container_width=True, hide_index=True
    )

with col2:
    st.markdown(
        "<span style='font-family:JetBrains Mono,monospace;font-size:11px;"
        "color:#FF5F40;letter-spacing:2px;'>▼ LOWEST PERFORMING LOCALITIES</span>",
        unsafe_allow_html=True
    )
    bottom5 = df_filtered.sort_values(selected_duration, ascending=True).head(5)
    fig_bot = go.Figure(go.Bar(
        x=bottom5[selected_duration], y=bottom5["locality"], orientation="h",
        marker=dict(color=bottom5[selected_duration],
                    colorscale=[[0, "#FF5F40"], [1, "#FFD60A"]], line_width=0),
        text=bottom5[selected_duration].apply(lambda v: f"{v:.1f}%"),
        textposition="outside", textfont=dict(color="#FF5F40", size=11)
    ))
    fig_bot.update_layout(**{**PLOTLY_LAYOUT, "height": 280, "margin": dict(l=10, r=70, t=20, b=10)})
    st.plotly_chart(fig_bot, use_container_width=True)
    st.dataframe(
        bottom5[["locality", "growth_1y", "growth_3y", "recommendation"]]
        .rename(columns={"locality": "Locality", "growth_1y": "1Y%",
                         "growth_3y": "3Y%", "recommendation": "Signal"}),
        use_container_width=True, hide_index=True
    )

# ===================================================
# SECTION 3: 1Y vs 3Y GROWTH COMPARISON
# ===================================================

st.markdown("""
<div class="section-header">
    <span class="section-icon">📈</span>
    <span class="section-title">1Y vs 3Y GROWTH COMPARISON</span>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="info-box">Grouped bars comparing short-term (1Y) vs medium-term (3Y) price appreciation '
    'per locality — sorted by 1Y growth. Localities where 3Y &gt; 1Y indicate accelerating long-term momentum.</div>',
    unsafe_allow_html=True
)

df_sorted_1y = df_filtered.sort_values("growth_1y", ascending=False)

fig_multi = go.Figure()
fig_multi.add_trace(go.Bar(x=df_sorted_1y["locality"], y=df_sorted_1y["growth_1y"],
                           name="1 Year", marker_color="#00FFD1", marker_line_width=0))
fig_multi.add_trace(go.Bar(x=df_sorted_1y["locality"], y=df_sorted_1y["growth_3y"],
                           name="3 Years", marker_color="#4FA3FF", marker_line_width=0))
fig_multi.update_layout(**{**PLOTLY_LAYOUT, "barmode": "group", "height": 420})

st.markdown('<div class="plotly-container">', unsafe_allow_html=True)
st.plotly_chart(fig_multi, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Heatmap — 1Y vs 3Y at a glance
st.markdown(
    "<span style='font-family:JetBrains Mono,monospace;font-size:11px;"
    "color:#6B8299;letter-spacing:2px;'>GROWTH HEATMAP — 1Y vs 3Y</span>",
    unsafe_allow_html=True
)
heatmap_df = df_filtered.set_index("locality")[["growth_1y", "growth_3y"]].T
fig_heat = px.imshow(
    heatmap_df,
    color_continuous_scale=["#FF5F40", "#050A14", "#00FFD1"],
    aspect="auto",
    labels=dict(x="Locality", y="Period", color="Growth %"),
)
fig_heat.update_layout(**{
    **PLOTLY_LAYOUT,
    "height": 200,
    "margin": dict(l=60, r=20, t=20, b=80),
    "coloraxis_colorbar": dict(thickness=8, tickfont=dict(color="#E8F0F7", size=10))
})
fig_heat.update_xaxes(tickangle=45, tickfont=dict(size=10))

st.markdown('<div class="plotly-container">', unsafe_allow_html=True)
st.plotly_chart(fig_heat, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ===================================================
# SECTION 4: PRICE SEGMENT ANALYSIS
# ===================================================

st.markdown("""
<div class="section-header">
    <span class="section-icon">🏷</span>
    <span class="section-title">PRICE SEGMENT ANALYSIS</span>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="info-box">Localities grouped into <b>Affordable / Mid-Range / Premium</b> segments based on '
    'price per sqft (or growth-based proxy if unavailable). Compares average growth and predicted returns per segment.</div>',
    unsafe_allow_html=True
)

segment_agg = (
    df_filtered.groupby("segment", observed=True)[
        ["growth_1y", "growth_3y", "predicted_growth_next_year"]
    ].mean().round(2).reset_index()
)

col_seg1, col_seg2 = st.columns([3, 2])

with col_seg1:
    fig_seg = px.bar(
        segment_agg, x="segment",
        y=["growth_1y", "growth_3y", "predicted_growth_next_year"],
        barmode="group",
        color_discrete_sequence=["#00FFD1", "#4FA3FF", "#FF5F40"],
        labels={"value": "Avg Growth %", "segment": "Segment", "variable": "Period"},
    )
    fig_seg.update_layout(**{**PLOTLY_LAYOUT, "height": 340})
    fig_seg.update_traces(marker_line_width=0)
    fig_seg.for_each_trace(lambda t: t.update(name=t.name
        .replace("growth_1y", "1Y Growth")
        .replace("growth_3y", "3Y Growth")
        .replace("predicted_growth_next_year", "Predicted Next Year")
    ))
    st.markdown('<div class="plotly-container">', unsafe_allow_html=True)
    st.plotly_chart(fig_seg, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_seg2:
    seg_count = df_filtered["segment"].value_counts().reset_index()
    seg_count.columns = ["segment", "count"]
    fig_donut = px.pie(seg_count, names="segment", values="count", hole=0.6,
                       color_discrete_sequence=["#00FFD1", "#4FA3FF", "#FFD60A"])
    fig_donut.update_layout(**{
        **PLOTLY_LAYOUT, "height": 260, "showlegend": True,
        "margin": dict(l=10, r=10, t=10, b=10)
    })
    fig_donut.update_traces(textfont=dict(color="#E8F0F7"))
    st.markdown('<div class="plotly-container">', unsafe_allow_html=True)
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    seg_count_full = df_filtered.groupby("segment", observed=True).size().reset_index(name="Localities")
    display_seg = segment_agg.merge(seg_count_full, on="segment")
    display_seg.columns = ["Segment", "1Y Avg%", "3Y Avg%", "Predicted%", "Localities"]
    st.dataframe(display_seg, use_container_width=True, hide_index=True)

# ===================================================
# SECTION 5: PRICE GROWTH PREDICTION MODEL
# ===================================================

st.markdown("""
<div class="section-header">
    <span class="section-icon">🔮</span>
    <span class="section-title">PRICE GROWTH PREDICTION MODEL</span>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    f'<div class="info-box">'
    f'Linear Regression trained on 1Y + 3Y growth features → predicts next-year % appreciation. '
    f'R² = <b>{r2_score:.3f}</b> &nbsp;|&nbsp; '
    f'Coefficients → 1Y: <b>{model.coef_[0]:.3f}</b> · 3Y: <b>{model.coef_[1]:.3f}</b> · '
    f'Intercept: <b>{model.intercept_:.3f}</b>'
    f'</div>',
    unsafe_allow_html=True
)

col_pred1, col_pred2 = st.columns([3, 2])

with col_pred1:
    fig_pred = px.bar(
        df_filtered.sort_values("predicted_growth_next_year", ascending=False),
        x="locality", y="predicted_growth_next_year",
        color="predicted_growth_next_year",
        color_continuous_scale=["#FF5F40", "#FFD60A", "#00FFD1"],
        labels={"predicted_growth_next_year": "Predicted Growth %", "locality": "Locality"},
        hover_data={"recommendation": True, "investment_score": ":.2f"}
    )
    fig_pred.update_layout(**{
        **PLOTLY_LAYOUT, "height": 380,
        "coloraxis_colorbar": dict(title="Predicted %", thickness=8,
                                   tickfont=dict(color="#E8F0F7", size=10))
    })
    fig_pred.update_traces(marker_line_width=0)
    st.markdown('<div class="plotly-container">', unsafe_allow_html=True)
    st.plotly_chart(fig_pred, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_pred2:
    st.markdown(
        "<span style='font-family:JetBrains Mono,monospace;font-size:11px;"
        "color:#6B8299;letter-spacing:2px;'>ACTUAL 1Y vs PREDICTED</span>",
        unsafe_allow_html=True
    )
    fig_av = px.scatter(
        df_filtered, x="growth_1y", y="predicted_growth_next_year",
        color="segment", hover_name="locality",
        color_discrete_sequence=["#00FFD1", "#4FA3FF", "#FFD60A"],
        labels={"growth_1y": "Actual 1Y Growth %",
                "predicted_growth_next_year": "Predicted Next Year %"},
    )
    # Manual trendline using numpy (no statsmodels needed)
    try:
        _x = df_filtered["growth_1y"].fillna(0).values
        _y = df_filtered["predicted_growth_next_year"].fillna(0).values
        if len(_x) >= 2 and np.std(_x) > 0:
            _m, _b = np.polyfit(_x, _y, 1)
            _x_line = np.linspace(_x.min(), _x.max(), 100)
            fig_av.add_trace(go.Scatter(
                x=_x_line, y=_m * _x_line + _b,
                mode="lines", name="Trend",
                line=dict(color="rgba(255,214,10,0.7)", width=2, dash="dot"),
                showlegend=True
            ))
    except (np.linalg.LinAlgError, ValueError):
        pass  # skip trendline if data has no variance or too few points
    fig_av.update_layout(**{**PLOTLY_LAYOUT, "height": 360})
    st.markdown('<div class="plotly-container">', unsafe_allow_html=True)
    st.plotly_chart(fig_av, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ===================================================
# SECTION 6: INVESTMENT RECOMMENDATION LOGIC
# ===================================================

st.markdown("""
<div class="section-header">
    <span class="section-icon">💡</span>
    <span class="section-title">INVESTMENT RECOMMENDATION LOGIC</span>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="info-box">'
    'Multi-tier signal engine using predicted growth + volatility: &nbsp;'
    '<b>🚀 Strong Buy</b> = predicted &gt;15% + vol &lt;10 &nbsp;|&nbsp; '
    '<b>📈 High Growth/Risk</b> = predicted &gt;15% + vol ≥10 &nbsp;|&nbsp; '
    '<b>📊 Moderate Buy</b> = predicted 5–15% &nbsp;|&nbsp; '
    '<b>⏸ Hold</b> = predicted 0–5% &nbsp;|&nbsp; '
    '<b>⚠ Avoid</b> = negative prediction'
    '</div>',
    unsafe_allow_html=True
)

col_r1, col_r2 = st.columns([2, 3])

with col_r1:
    rec_dist = df_filtered["recommendation"].value_counts().reset_index()
    rec_dist.columns = ["Signal", "Count"]
    fig_rec_pie = px.pie(rec_dist, names="Signal", values="Count", hole=0.55,
                         color_discrete_sequence=["#00FFD1", "#4FA3FF", "#FFD60A", "#FF5F40", "#C77DFF"])
    fig_rec_pie.update_layout(**{
        **PLOTLY_LAYOUT, "height": 320,
        "margin": dict(l=10, r=10, t=10, b=10), "showlegend": True
    })
    fig_rec_pie.update_traces(textfont=dict(color="#E8F0F7"))
    st.markdown('<div class="plotly-container">', unsafe_allow_html=True)
    st.plotly_chart(fig_rec_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_r2:
    # Risk vs Reward scatter
    fig_scatter = px.scatter(
        df_filtered, x="volatility", y="predicted_growth_next_year",
        size="bubble_size", color="investment_score",
        hover_name="locality",
        hover_data={"recommendation": True, "bubble_size": False},
        color_continuous_scale=["#FF5F40", "#FFD60A", "#00FFD1"],
        labels={"volatility": "Volatility (Risk)",
                "predicted_growth_next_year": "Predicted Growth %",
                "investment_score": "Score"},
        size_max=40,
    )
    fig_scatter.update_layout(**{
        **PLOTLY_LAYOUT, "height": 360,
        "coloraxis_colorbar": dict(title="Score", thickness=8,
                                   tickfont=dict(color="#E8F0F7", size=10))
    })
    fig_scatter.update_traces(marker=dict(line=dict(color="rgba(0,255,209,0.3)", width=1)))

    if not df_filtered.empty:
        mid_vol    = df_filtered["volatility"].median()
        mid_growth = df_filtered["predicted_growth_next_year"].median()
        for shape_args in [
            dict(type="line", x0=mid_vol, x1=mid_vol,
                 y0=df_filtered["predicted_growth_next_year"].min(),
                 y1=df_filtered["predicted_growth_next_year"].max(),
                 line=dict(color="rgba(255,255,255,0.12)", dash="dot", width=1)),
            dict(type="line",
                 x0=df_filtered["volatility"].min(), x1=df_filtered["volatility"].max(),
                 y0=mid_growth, y1=mid_growth,
                 line=dict(color="rgba(255,255,255,0.12)", dash="dot", width=1)),
        ]:
            fig_scatter.add_shape(**shape_args)

    st.markdown('<div class="plotly-container">', unsafe_allow_html=True)
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ===================================================
# SECTION 7: INVESTMENT LEADERBOARD
# ===================================================

st.markdown("""
<div class="section-header">
    <span class="section-icon">🏅</span>
    <span class="section-title">INVESTMENT LEADERBOARD</span>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

leaderboard = df_filtered.sort_values("investment_score", ascending=False).reset_index(drop=True)
leaderboard.index = leaderboard.index + 1

display_lb = leaderboard[[
    "locality", "segment", "growth_1y", "growth_3y",
    "investment_score", "predicted_growth_next_year", "volatility", "recommendation"
]].copy()
display_lb.columns = ["Locality", "Segment", "1Y%", "3Y%", "Score", "Predicted%", "Volatility", "Signal"]
display_lb["Score"]      = display_lb["Score"].round(2)
display_lb["Predicted%"] = display_lb["Predicted%"].round(2)
display_lb["Volatility"] = display_lb["Volatility"].round(2)

st.dataframe(
    display_lb,
    use_container_width=True,
    column_config={
        "Score": st.column_config.ProgressColumn(
            "Investment Score",
            min_value=float(display_lb["Score"].min()),
            max_value=float(display_lb["Score"].max()),
            format="%.2f"
        ),
        "Predicted%": st.column_config.NumberColumn("Predicted %", format="%.2f%%"),
        "1Y%":        st.column_config.NumberColumn("1Y %",        format="%.1f%%"),
        "3Y%":        st.column_config.NumberColumn("3Y %",        format="%.1f%%"),
        "Volatility": st.column_config.NumberColumn("Volatility",  format="%.2f"),
    },
    height=420
)

# ===================================================
# SECTION 8: HIGH-VOLATILITY RISK ZONES
# ===================================================

st.markdown("""
<div class="section-header">
    <span class="section-icon">⚠</span>
    <span class="section-title">HIGH-VOLATILITY RISK ZONES</span>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

high_risk = df_filtered.sort_values("volatility", ascending=False).head(5)

col_risk1, col_risk2 = st.columns([2, 3])

with col_risk1:
    st.dataframe(
        high_risk[["locality", "volatility", "growth_1y", "growth_3y", "recommendation"]]
        .rename(columns={"locality": "Locality", "volatility": "Volatility",
                         "growth_1y": "1Y%", "growth_3y": "3Y%", "recommendation": "Signal"})
        .reset_index(drop=True),
        use_container_width=True, hide_index=True
    )

with col_risk2:
    fig_risk = go.Figure()
    fig_risk.add_trace(go.Scatterpolar(
        r=high_risk["volatility"], theta=high_risk["locality"],
        fill="toself", fillcolor="rgba(255,95,64,0.15)",
        line=dict(color="#FF5F40", width=2), name="Volatility"
    ))
    fig_risk.add_trace(go.Scatterpolar(
        r=high_risk["growth_1y"].clip(lower=0), theta=high_risk["locality"],
        fill="toself", fillcolor="rgba(0,255,209,0.08)",
        line=dict(color="#00FFD1", width=2), name="1Y Growth"
    ))
    fig_risk.update_layout(**{
        **PLOTLY_LAYOUT,
        "polar": dict(
            bgcolor="rgba(11,20,34,0)",
            radialaxis=dict(visible=True, gridcolor="rgba(0,255,209,0.1)",
                            linecolor="rgba(0,255,209,0.2)", tickfont=dict(color="#6B8299")),
            angularaxis=dict(gridcolor="rgba(0,255,209,0.1)", linecolor="rgba(0,255,209,0.2)",
                             tickfont=dict(color="#E8F0F7"))
        ),
        "height": 380
    })
    st.markdown('<div class="plotly-container">', unsafe_allow_html=True)
    st.plotly_chart(fig_risk, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown(f"""
<div class="dashboard-footer">
    NAGPUR PROPERTY INTELLIGENCE &nbsp;·&nbsp;
    LINEAR REGRESSION MODEL (R²={r2_score:.3f}) &nbsp;·&nbsp;
    AUTO-REFRESH EVERY 60 MIN &nbsp;·&nbsp;
    CACHE TTL: 3600s &nbsp;·&nbsp;
    {total_loc} LOCALITIES TRACKED
</div>
""", unsafe_allow_html=True)
