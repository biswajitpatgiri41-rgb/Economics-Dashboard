# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Page Config ---
st.set_page_config(
    page_title="Economics Indicator Dashboard",
    layout="wide",
    page_icon="💹"
)

# --- Header ---
st.title("💹 Economics Indicator Dashboard")
st.markdown("""
Analyze key economic indicators like GDP, Inflation, Unemployment, and Interest Rate
across countries with interactive charts.
""")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("Economics_Dashboard/dataSet.csv")
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("Filters")
country = st.sidebar.multiselect("Select Country", options=df['Country'].unique(), default=['USA', 'India'])
indicators = st.sidebar.multiselect(
    "Select Indicators to Visualize", 
    options=['GDP', 'Inflation', 'Unemployment', 'Interest_Rate'],
    default=['GDP', 'Inflation']
)
year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=int(df['Year'].min()),
    max_value=int(df['Year'].max()),
    value=(int(df['Year'].min()), int(df['Year'].max()))
)

# --- Filter Data ---
data_filtered = df[
    (df['Country'].isin(country)) & 
    (df['Year'] >= year_range[0]) & 
    (df['Year'] <= year_range[1])
]

# --- Key Performance Indicators ---
st.subheader("📊 Key Performance Indicators")
kpi_cols = st.columns(len(indicators))
for i, ind in enumerate(indicators):
    latest_value = data_filtered[data_filtered['Year'] == data_filtered['Year'].max()][ind].mean()
    kpi_cols[i].metric(label=ind, value=f"{latest_value:.2f}")

# --- Line Charts ---
st.subheader("📈 Trends Over Time")
for ind in indicators:
    fig = px.line(
        data_filtered, 
        x='Year', 
        y=ind, 
        color='Country',
        markers=True,
        title=f"{ind} Trends",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Multi-indicator Comparison Radar Chart ---
if len(indicators) > 1 and len(country) > 0:
    st.subheader("🕸 Multi-indicator Comparison (Radar Chart)")
    radar_data = data_filtered.groupby('Country')[indicators].mean().reset_index()
    fig = go.Figure()
    for i, row in radar_data.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=row[indicators].values,
            theta=indicators,
            fill='toself',
            name=row['Country']
        ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True,
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Footer ---
st.markdown("""
---
Created by **Your Name** | Advanced Economics Dashboard with Streamlit & Plotly
""")