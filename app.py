import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import re

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Vancouver Cherry Blossoms 🌸",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Nunito:wght@300;400;500;600&display=swap');

    /* ── App background ── */
    .stApp {
        background: linear-gradient(160deg, #fef6f8 0%, #fdf2f5 50%, #fceff4 100%) !important;
        font-family: 'Nunito', sans-serif;
    }
    .main .block-container {
        padding-top: 1.5rem;
    }

    /* ── Global type ── */
    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }
    h1, h2, h3, h4 {
        font-family: 'Cormorant Garamond', serif !important;
        color: #6b3050 !important;
        font-weight: 400 !important;
        letter-spacing: 0.03em;
    }

    /* ── Header ── */
    .main-header {
        background: linear-gradient(135deg, #fce9ef 0%, #f8d8e6 35%, #f3cade 65%, #edd0dc 100%);
        padding: 2.2rem 2.5rem;
        border-radius: 24px;
        margin-bottom: 1.8rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow:
            0 8px 40px rgba(180, 90, 130, 0.12),
            inset 0 1px 0 rgba(255, 255, 255, 0.75),
            inset 0 -1px 0 rgba(200, 120, 150, 0.1);
        border: 1px solid rgba(235, 190, 210, 0.5);
    }
    .main-header::before {
        content: "🌸";
        position: absolute;
        font-size: 9rem;
        opacity: 0.055;
        top: -15px;
        left: -20px;
        transform: rotate(-20deg);
        pointer-events: none;
    }
    .main-header::after {
        content: "🌸";
        position: absolute;
        font-size: 9rem;
        opacity: 0.055;
        bottom: -20px;
        right: -10px;
        transform: rotate(15deg);
        pointer-events: none;
    }
    .main-header h1 {
        color: #5e2a44 !important;
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 2.9rem !important;
        font-weight: 600 !important;
        margin: 0 !important;
        letter-spacing: 0.04em;
        text-shadow: 0 2px 4px rgba(180, 80, 120, 0.15);
        line-height: 1.1;
    }
    .main-header p {
        color: #9b6678 !important;
        margin: 0.6rem 0 0 0 !important;
        font-size: 0.9rem !important;
        font-family: 'Nunito', sans-serif;
        font-weight: 300;
        letter-spacing: 0.06em;
    }

    /* ── KPI metric cards ── */
    div[data-testid="metric-container"] {
        background: linear-gradient(
            150deg,
            rgba(255, 247, 250, 0.97) 0%,
            rgba(251, 233, 242, 0.88) 100%
        ) !important;
        border: 1px solid rgba(225, 175, 200, 0.38) !important;
        border-radius: 18px !important;
        padding: 1.2rem 1rem !important;
        box-shadow:
            0 4px 18px rgba(185, 90, 130, 0.07),
            inset 0 1px 0 rgba(255, 255, 255, 0.9);
        transition: transform 0.22s ease, box-shadow 0.22s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 28px rgba(185, 90, 130, 0.14);
    }
    div[data-testid="metric-container"] label {
        color: #a07080 !important;
        font-weight: 500 !important;
        font-family: 'Nunito', sans-serif;
        font-size: 0.78rem !important;
        letter-spacing: 0.07em;
        text-transform: uppercase;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #5e2a44 !important;
        font-size: 1.85rem !important;
        font-family: 'Cormorant Garamond', serif !important;
        font-weight: 600 !important;
        line-height: 1.15;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricDelta"] {
        color: #c07090 !important;
        font-size: 0.82rem !important;
        font-family: 'Nunito', sans-serif;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #fdf0f4 0%, #fae8ef 55%, #f7e0ea 100%) !important;
        border-right: 1px solid rgba(225, 175, 200, 0.3) !important;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.2rem;
    }
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h2 {
        font-family: 'Cormorant Garamond', serif !important;
        color: #6b3050 !important;
        font-size: 1.15rem !important;
        font-weight: 400 !important;
        letter-spacing: 0.04em;
    }
    /* Sidebar inputs */
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] .stSelectbox div,
    section[data-testid="stSidebar"] .stMultiSelect div {
        background: rgba(255, 248, 251, 0.85) !important;
        border-color: rgba(215, 165, 190, 0.5) !important;
        border-radius: 10px !important;
    }

    /* ── Bloom badge ── */
    .bloom-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: linear-gradient(135deg, #d4607a, #bf4a6a);
        color: white;
        padding: 7px 20px;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 600;
        font-family: 'Nunito', sans-serif;
        letter-spacing: 0.05em;
        margin: 6px 0;
        box-shadow: 0 4px 16px rgba(190, 74, 106, 0.38);
        animation: bloom-glow 2.8s ease-in-out infinite;
    }
    @keyframes bloom-glow {
        0%   { box-shadow: 0 4px 16px rgba(190,74,106,0.35), 0 0 0 0 rgba(212,96,122,0.4); }
        50%  { box-shadow: 0 6px 22px rgba(190,74,106,0.5), 0 0 0 10px rgba(212,96,122,0.0); }
        100% { box-shadow: 0 4px 16px rgba(190,74,106,0.35), 0 0 0 0 rgba(212,96,122,0.4); }
    }

    /* ── Section headers ── */
    .section-header {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.6rem;
        font-weight: 400;
        color: #6b3050;
        letter-spacing: 0.04em;
        margin: 0.5rem 0 1rem 0;
        padding-bottom: 0.35rem;
        border-bottom: 1px solid rgba(215, 165, 190, 0.45);
        display: flex;
        align-items: center;
        gap: 0.4em;
    }

    /* ── Divider ── */
    hr {
        border: none !important;
        border-top: 1px solid rgba(215, 165, 190, 0.4) !important;
        margin: 1.5rem 0 !important;
    }

    /* ── Dataframe ── */
    div[data-testid="stDataFrame"] {
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 20px rgba(185, 90, 130, 0.08) !important;
        border: 1px solid rgba(215, 165, 190, 0.3) !important;
    }

    /* ── Expanders ── */
    details {
        border: 1px solid rgba(215, 165, 190, 0.4) !important;
        border-radius: 14px !important;
        background: rgba(255, 248, 251, 0.85) !important;
    }
    details summary {
        font-family: 'Nunito', sans-serif;
        color: #7a3553 !important;
        font-weight: 500;
    }

    /* ── Download button ── */
    div[data-testid="stDownloadButton"] button {
        background: linear-gradient(135deg, #e8849f, #d4607a) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-family: 'Nunito', sans-serif;
        font-weight: 600;
        letter-spacing: 0.04em;
        box-shadow: 0 4px 14px rgba(212, 96, 122, 0.3);
        transition: all 0.2s ease;
    }
    div[data-testid="stDownloadButton"] button:hover {
        background: linear-gradient(135deg, #df6f8e, #c5506a) !important;
        box-shadow: 0 6px 20px rgba(212, 96, 122, 0.45);
        transform: translateY(-1px);
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #fdf0f4; }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(#e8a4b8, #d4607a);
        border-radius: 3px;
    }

    /* ── Slider accent ── */
    div[data-baseweb="slider"] div[data-testid="stThumbValue"] {
        background: #d4607a !important;
        color: white !important;
    }

    /* ── Radio + multiselect tags ── */
    span[data-baseweb="tag"] {
        background: rgba(235, 160, 185, 0.3) !important;
        border: 1px solid rgba(212, 96, 122, 0.35) !important;
        border-radius: 20px !important;
        color: #6b3050 !important;
    }
</style>
""", unsafe_allow_html=True)

# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <h1>🌸 Vancouver Cherry Blossom Tracker</h1>
  <p>Explore & visualise every cherry blossom tree across the city &nbsp;·&nbsp; Data: City of Vancouver Open Data</p>
</div>
""", unsafe_allow_html=True)

# ─── Load & Prepare Data ────────────────────────────────────────────────────
@st.cache_data(show_spinner="Loading tree data…")
def load_data():
    df = pd.read_csv("public-trees.csv", sep=";", encoding="utf-8-sig")
    df.columns = df.columns.str.strip()

    # Apply some basic cleaning for all trees

    def parse_coords(val):
        try:
            parts = str(val).split(",")
            return float(parts[0].strip()), float(parts[1].strip())
        except:
            return None, None

    df[["lat", "lon"]] = df["geo_point_2d"].apply(
        lambda x: pd.Series(parse_coords(x))
    )
    df = df.dropna(subset=["lat", "lon"])

    df["Date planted"] = pd.to_datetime(df["Date planted"], errors="coerce")
    this_year = datetime.now().year
    df["age_years"] = df["Date planted"].apply(
        lambda d: this_year - d.year if pd.notnull(d) else None
    )
    df["year_planted"] = df["Date planted"].dt.year

    df["neighbourhood"] = df["Address"].str.extract(r'(?:AV|ST|DR|RD|BLVD|WAY|PL|LANE|CRES|CT|CLOSE|MEWS|WALK|ROAD)\s+(.+)$')
    df["neighbourhood"] = df["neighbourhood"].fillna("Unknown")

    df["Cultivar name"] = df["Cultivar name"].replace("NONE", "")
    df["full_name"] = (
        df["Common name"].str.title() + " " +
        df["Species name"].str.lower() + " " +
        df["Cultivar name"].str.title()
    ).str.strip()

    df["weight"] = 1
    return df

df = load_data()

# ─── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔍 Search & Filter")

    address_search = st.text_input("🏠 Search by Address", placeholder="e.g. W 15TH AV")

    all_genuses = sorted(df["Genus name"].dropna().unique())
    selected_genus = st.multiselect(
        "🌲 Tree Genus",
        options=all_genuses,
        default=["PRUNUS"] if "PRUNUS" in all_genuses else all_genuses[:1],
    )

    df_filtered_genus = df[df["Genus name"].isin(selected_genus)]
    all_varieties = sorted(df_filtered_genus["Common name"].dropna().unique())
    selected_varieties = st.multiselect(
        "🌸 Variety (Common Name)",
        options=all_varieties,
        default=all_varieties,
    )

    height_range = st.slider(
        "📏 Height (m)",
        float(df["height_(m)"].min()), float(df["height_(m)"].max()),
        (float(df["height_(m)"].min()), float(df["height_(m)"].max())), step=0.5,
    )
    diam_range = st.slider(
        "🌲 Trunk Diameter (cm)",
        float(df["diameter_(cm)"].min()), float(df["diameter_(cm)"].max()),
        (float(df["diameter_(cm)"].min()), float(df["diameter_(cm)"].max())), step=1.0,
    )

    year_min = int(df["year_planted"].dropna().min())
    year_max = int(df["year_planted"].dropna().max())
    year_range = st.slider(
        "📅 Year Planted",
        year_min, year_max, (year_min, year_max), step=1,
    )

    st.markdown("---")
    st.markdown("### 🗺️ Map Options")
    map_style = st.selectbox(
        "Map Style",
        options=["light", "dark", "road", "satellite"],
        index=0,
    )

    st.markdown("---")
    st.markdown("### 📥 Export")

# ─── Apply Filters ───────────────────────────────────────────────────────────
filtered = df[
    (df["Genus name"].isin(selected_genus)) &
    (df["Common name"].isin(selected_varieties)) &
    (df["height_(m)"].between(*height_range)) &
    (df["diameter_(cm)"].between(*diam_range))
].copy()

has_year = filtered["year_planted"].notna()
filtered = pd.concat([
    filtered[~has_year],
    filtered[has_year & filtered["year_planted"].between(*year_range)]
])

if address_search:
    filtered = filtered[filtered["Address"].str.contains(address_search.upper(), na=False)]

# ─── Export in Sidebar ───────────────────────────────────────────────────────
with st.sidebar:
    csv_export = filtered[[
        "Asset ID", "Address", "Common name", "Species name", "Cultivar name",
        "height_(m)", "diameter_(cm)", "Date planted", "lat", "lon"
    ]].to_csv(index=False)
    st.download_button(
        label="⬇️ Download Filtered Data (.csv)",
        data=csv_export,
        file_name="vancouver_cherry_blossoms_filtered.csv",
        mime="text/csv",
        use_container_width=True,
    )

# ─── KPI Row ─────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("🌲 Trees Shown", f"{len(filtered):,}", f"of {len(df):,} total")
k2.metric("🌳 Varieties", filtered["Common name"].nunique())
k3.metric("📏 Avg Height", f"{filtered['height_(m)'].mean():.1f} m")
k4.metric("🌲 Avg Diameter", f"{filtered['diameter_(cm)'].mean():.1f} cm")

st.markdown("")

# ─── Map ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🗺️ Interactive Map (Heatmap)</div>', unsafe_allow_html=True)

# Heatmap layer only
layer = pdk.Layer(
    "HeatmapLayer",
    data=filtered,
    get_position="[lon, lat]",
    get_weight="weight",
    radiusPixels=40,
    colorRange=[
        [255, 245, 250],   # near-white blush
        [252, 220, 235],   # very light sakura
        [245, 175, 205],   # soft petal pink
        [225, 130, 170],   # medium rose
        [195,  85, 130],   # deeper rose
        [150,  40,  85],   # dark cherry
    ],
    threshold=0.05,
    aggregation="SUM",
)

view_state = pdk.ViewState(
    latitude=49.2500,
    longitude=-123.1200,
    zoom=11.5,
    pitch=0,
    bearing=0,
)

st.pydeck_chart(
    pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style=map_style,
    ),
    use_container_width=True,
    height=500,
)

st.divider()

# ─── Analytics ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📊 Analytics</div>', unsafe_allow_html=True)

# Shared Plotly layout defaults
_layout = dict(
    plot_bgcolor="rgba(253,245,248,0.7)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#5e2a44", family="Nunito, sans-serif"),
    margin=dict(l=10, r=20, t=44, b=10),
    title_font=dict(family="Cormorant Garamond, serif", size=17, color="#6b3050"),
)
_scale = ["#fce4ec", "#eda8c0", "#bf4a72"]   # soft pink gradient for color scales

col1, col2 = st.columns(2)

with col1:
    variety_counts = filtered["Common name"].value_counts().reset_index()
    variety_counts.columns = ["Variety", "Count"]
    fig_var = px.bar(
        variety_counts,
        x="Count", y="Variety",
        orientation="h",
        title="🌸 Trees by Variety",
        color="Count",
        color_continuous_scale=_scale,
        text="Count",
    )
    fig_var.update_traces(textposition="outside", marker_line_width=0)
    fig_var.update_layout(
        **_layout,
        showlegend=False, coloraxis_showscale=False,
        yaxis={"categoryorder": "total ascending"},
    )
    st.plotly_chart(fig_var, use_container_width=True)

with col2:
    fig_scatter = px.scatter(
        filtered.dropna(subset=["height_(m)", "diameter_(cm)"]),
        x="diameter_(cm)", y="height_(m)",
        color="Common name",
        hover_data=["Address"],
        title="📐 Height vs. Trunk Diameter",
        opacity=0.6,
        color_discrete_sequence=[
            "#e8849f","#d4607a","#f0a8bf","#c04870","#f5c8d8",
            "#b83860","#ebb5cc","#a82850","#f8dae6","#983050",
        ],
        size_max=8,
    )
    fig_scatter.update_layout(
        **_layout,
        legend=dict(orientation="v", x=1, y=1, font=dict(size=10)),
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

col5, col6 = st.columns(2)

with col5:
    top_streets = (
        filtered["Address"]
        .str.extract(r'\d+\s+(.+)')
        [0]
        .value_counts()
        .head(15)
        .reset_index()
    )
    top_streets.columns = ["Street", "Count"]
    fig_streets = px.bar(
        top_streets,
        x="Count", y="Street",
        orientation="h",
        title="🏙️ Top 15 Streets by Tree Count",
        color="Count",
        color_continuous_scale=_scale,
        text="Count",
    )
    fig_streets.update_traces(textposition="outside", marker_line_width=0)
    fig_streets.update_layout(
        **_layout,
        showlegend=False, coloraxis_showscale=False,
        yaxis={"categoryorder": "total ascending"},
        margin=dict(l=10, r=30, t=44, b=10),
    )
    st.plotly_chart(fig_streets, use_container_width=True)

with col6:
    height_bins = pd.cut(filtered["height_(m)"], bins=10)
    height_dist = filtered.groupby(height_bins, observed=True)["height_(m)"].count().reset_index()
    height_dist.columns = ["Height Range", "Count"]
    height_dist["Height Range"] = height_dist["Height Range"].astype(str)
    fig_hist = px.bar(
        height_dist,
        x="Height Range", y="Count",
        title="📏 Height Distribution",
        color="Count",
        color_continuous_scale=_scale,
    )
    fig_hist.update_traces(marker_line_width=0)
    fig_hist.update_layout(
        **_layout,
        showlegend=False, coloraxis_showscale=False,
        xaxis_tickangle=-30,
        margin=dict(l=10, r=10, t=44, b=60),
    )
    st.plotly_chart(fig_hist, use_container_width=True)

st.divider()

# ─── Raw Data ─────────────────────────────────────────────────────────────────
with st.expander("📋 View Full Filtered Dataset", expanded=False):
    display_cols = [
        "Asset ID", "Address", "Common name", "Species name", "Cultivar name",
        "height_(m)", "diameter_(cm)", "age_years", "Date planted",
    ]
    st.dataframe(filtered[display_cols].reset_index(drop=True), use_container_width=True, height=400)
    st.caption(f"Showing {len(filtered):,} trees after filters applied.")

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 1.5rem 0 0.5rem 0;
            font-family:"Nunito",sans-serif; color:#b07090; font-size:0.8rem;
            letter-spacing:0.04em;'>
    🌸 Vancouver Cherry Blossom Tracker &nbsp;·&nbsp;
    Data: <a href='https://opendata.vancouver.ca' target='_blank'
             style='color:#d4607a; text-decoration:none;'>City of Vancouver Open Data</a>
    &nbsp;·&nbsp; Built with Streamlit + PyDeck + Plotly
</div>
""", unsafe_allow_html=True)
