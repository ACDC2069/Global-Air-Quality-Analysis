import streamlit as st
from utils import viz
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render(df):
    st.title("Deep Dives & Analysis")
    
    tab1, tab2 = st.tabs(["Regional Rankings", "Correlations"])
    
    # Tab 1: Ranking
    with tab1:
        st.subheader("Top Polluted Cities")
        
        # Aggregate by City / 按城市聚合
        city_stats = df.groupby('City')['PM2.5'].mean().sort_values(ascending=False).head(10).reset_index()
        
        fig_bar = viz.plot_bar_chart(
            city_stats, x='PM2.5', y='City',
            title="Top 10 Cities by Average PM2.5"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
    # Tab 2: Correlations
    with tab2:
        st.subheader("Meteorological Impacts")
        
        # Check if necessary columns exist
        if 'Wind Speed' in df.columns and 'Temperature' in df.columns:
            
            col1, col2 = st.columns(2)
            
            # --- Helper Function to Create Trend Plot ---
            # 辅助函数：创建带有趋势线的清晰图表
            def create_trend_plot(data, x_col, y_col, title, x_label):
                # 1. Create Binned Averages (The "Trend Line") / 创建分箱均值（趋势线）
                # Round x-values to create bins (e.g., round temp to nearest integer)
                # 将X轴数值取整以创建分组
                data['x_bin'] = data[x_col].round()
                trend_data = data.groupby('x_bin')[y_col].mean().reset_index()
                trend_data = trend_data.sort_values('x_bin')
                
                fig = go.Figure()
                
                # Layer 1: Raw Scatter (Faint Background) / 第一层：原始散点（淡背景）
                # Sampling to reduce visual noise / 采样减少噪点
                plot_sample = data.sample(min(1000, len(data)))
                fig.add_trace(go.Scatter(
                    x=plot_sample[x_col], 
                    y=plot_sample[y_col],
                    mode='markers',
                    name='Raw Data',
                    marker=dict(
                        color='#cccccc', # Light gray / 浅灰
                        size=5,
                        opacity=0.3 # Very transparent / 高透明度
                    ),
                    hoverinfo='skip' # Skip hover on noise / 跳过背景点的悬停信息
                ))
                
                # Layer 2: Trend Line (Bold & Clear) / 第二层：趋势线（粗且清晰）
                fig.add_trace(go.Scatter(
                    x=trend_data['x_bin'], 
                    y=trend_data[y_col],
                    mode='lines+markers',
                    name='Average Trend',
                    line=dict(color='#FF4B4B', width=3), # Streamlit Red / 醒目红
                    marker=dict(color='#FF4B4B', size=6)
                ))
                
                fig.update_layout(
                    title=title,
                    xaxis_title=x_label,
                    yaxis_title="Avg PM2.5 Concentration",
                    template="plotly_white",
                    hovermode="x unified",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                return fig

            with col1:
                # Plot 1: Temperature vs PM2.5
                st.markdown("#### Temperature Impact")
                fig_temp = create_trend_plot(
                    df.copy(), 
                    'Temperature', 
                    'PM2.5', 
                    "Temperature vs PM2.5 Trend",
                    "Temperature (°C)"
                )
                st.plotly_chart(fig_temp, use_container_width=True)
                st.caption("The **Red Line** shows the average PM2.5 level at each temperature.")
                
            with col2:
                # Plot 2: Wind Speed vs PM2.5
                st.markdown("#### Wind Speed Impact")
                fig_wind = create_trend_plot(
                    df.copy(), 
                    'Wind Speed', 
                    'PM2.5', 
                    "Wind Speed vs PM2.5 Trend",
                    "Wind Speed (km/h)"
                )
                st.plotly_chart(fig_wind, use_container_width=True)
                st.caption("The **Red Line** shows the average PM2.5 level at each wind speed.")

            st.markdown("---")
            st.markdown("""
            **How to read these charts:**
            * **Grey Dots (Background)**: These are the individual daily records. They show the variability (the "messiness") of real-world data.
            * **Red Line (Foreground)**: This is the **average trend**. Follow this line to see the pattern.
            
            **Key Insights:**
            1.  **Wind Speed**: Notice how the Red Line generally **slopes downwards** as wind speed increases. This confirms that wind helps clear the air.
            2.  **Temperature**: The pattern might be U-shaped or irregular, indicating that both extreme cold (heating) and extreme heat can affect air quality differently.
            """)
        else:
            st.warning("Weather data (Wind/Temperature) missing from the dataset.")