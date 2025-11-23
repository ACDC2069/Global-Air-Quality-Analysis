import streamlit as st
from utils import viz

def render(df):
    st.title("Global Overview & Trends")
    st.markdown("### Key Performance Indicators")
    
    # KPIs
    avg_pm25 = df['PM2.5'].mean()
    max_pm25 = df['PM2.5'].max()
    # Count distinct cities / 统计不同城市数量
    city_count = df['City'].nunique()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Average PM2.5 Level", f"{avg_pm25:.2f} µg/m³")
    col2.metric("Max PM2.5 Recorded", f"{max_pm25:.2f} µg/m³")
    col3.metric("Cities Analyzed", city_count)
    
    st.markdown("---")
    
    # Map
    st.subheader("Geographic Distribution")
    st.caption("Average PM2.5 intensity by country")
    fig_map = viz.plot_map(df)
    st.plotly_chart(fig_map, use_container_width=True)
    
    # Time Series
    st.subheader("Temporal Evolution")
    if 'Date' in df.columns:
        fig_line = viz.plot_line_chart(
            df, x='Date', y='PM2.5', 
            title="Daily PM2.5 Trends",
            color='Country' if df['Country'].nunique() < 10 else None
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.warning("Temporal data not available.")
