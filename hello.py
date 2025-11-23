import os

# Define directory structure / 定义目录结构
directories = [
    "sections",
    "utils",
    "data",
    "assets"
]

# Function to create dummy logos so the app doesn't crash immediately
# 创建占位 Logo 的函数，防止应用因缺少图片崩溃
def create_dummy_logos():
    # Simple 1x1 pixel placeholders
    dummy_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDAT\x08\xd7c\xf8\xcf\xc0\x00\x00\x03\x01\x01\x00\x18\xdd\x8d\xb0\x00\x00\x00\x00IEND\xaeB`\x82'
    
    # Create placeholder for EFREI logo
    with open("assets/logo_efrei.png", "wb") as f:
        f.write(dummy_data)
        
    # Create placeholder for WUT logo
    with open("assets/logo_wut.png", "wb") as f:
        f.write(dummy_data)

# Define file contents / 定义文件内容
files = {
    "requirements.txt": """streamlit
pandas
plotly
numpy
""",

    "app.py": r'''import streamlit as st
from sections import intro, overview, deep_dives, conclusions
from utils import io, prep

# -----------------------------------------------------------------------------
# Page Configuration / 页面配置
# Academic and professional layout settings.
# 学术和专业布局设置。
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Global Air Quality Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Custom Styling / 自定义样式
# Black sidebar, professional fonts, hidden default streamlit menu elements.
# 黑色侧边栏，专业字体，隐藏默认 Streamlit 菜单元素。
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    /* Force Sidebar to be Black / 强制侧边栏为黑色 */
    section[data-testid="stSidebar"] {
        background-color: #000000;
    }
    
    /* Sidebar Text Colors / 侧边栏文字颜色 */
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] p {
        color: #FFFFFF !important;
    }

    /* Input widget labels in sidebar / 侧边栏输入控件标签 */
    .stMultiSelect label, .stDateInput label, .stRadio label {
        color: #FFFFFF !important;
    }
    
    /* Main Content Background / 主内容背景 - White for academic look */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* Metric Styling / 指标样式 - Clean Blue */
    div[data-testid="stMetricValue"] {
        font-family: 'Arial', sans-serif;
        color: #003366; /* Dark Blue */
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    """
    Main Application Logic.
    主应用程序逻辑。
    """
    
    # -------------------------------------------------------------------------
    # Sidebar Configuration / 侧边栏配置
    # -------------------------------------------------------------------------
    with st.sidebar:
        # 1. Logos / Logo 展示
        # Displaying two logos side-by-side or stacked
        col1, col2 = st.columns(2)
        with col1:
            try:
                st.image("assets/logo_efrei.png", use_container_width=True)
            except:
                st.write("EFREI")
        with col2:
            try:
                st.image("assets/logo_wut.png", use_container_width=True)
            except:
                st.write("WUT")
        
        st.markdown("---")
        
        # 2. Project Info / 项目信息
        st.markdown("### Global Air Quality Analysis")
        st.caption("Air quality analysis including major cities around the world")
        
        st.markdown("---")
        
        # 3. Contact Info / 联系信息
        st.markdown("**Supervisors & Team**")
        st.markdown("""
        <div style='font-size: 12px; color: #cccccc;'>
        <b>Mano Joseph Mathew</b><br>
        mano.mathew@efrei.fr
        <br><br>
        <b>Wangbeinuo</b><br>
        beinuo.wang@efrei.net
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")

        # 4. Filters / 筛选器
        st.subheader("Configuration")
        
        # Load Data / 加载数据
        df_raw = io.load_data()
        if df_raw is None:
            st.error("Data not found.")
            return

        df_clean = prep.clean_data(df_raw)
        if df_clean is None:
            st.stop()

        # Country Filter with "Select All" logic / 带有“全选”逻辑的国家筛选器
        all_countries = sorted(df_clean['Country'].unique())
        
        # Add a toggle or specific option for "All"
        # Using a multiselect where empty means "All" is often cleanest, 
        # but explicit "All" option is requested.
        container = st.container()
        select_all = st.checkbox("Select All Countries", value=False)
        
        if select_all:
            selected_countries = all_countries
            st.info(f"Analyzing all {len(all_countries)} countries.")
        else:
            selected_countries = st.multiselect(
                "Select Countries",
                all_countries,
                default=all_countries[:3] if len(all_countries) > 3 else all_countries
            )

        # Apply Filters / 应用筛选
        df_filtered = df_clean[df_clean['Country'].isin(selected_countries)]
        
        st.markdown("---")
        
        # 5. Navigation / 导航
        st.subheader("Navigation")
        page = st.radio(
            "Go to:",
            ["Project Context", 
             "Overview & Trends", 
             "Deep Dives", 
             "Conclusions"],
            label_visibility="collapsed"
        )

    # -------------------------------------------------------------------------
    # Main Page Routing / 主页面路由
    # -------------------------------------------------------------------------
    if page == "Project Context":
        intro.render(df_raw)
    elif page == "Overview & Trends":
        overview.render(df_filtered)
    elif page == "Deep Dives":
        deep_dives.render(df_filtered)
    elif page == "Conclusions":
        conclusions.render()

if __name__ == "__main__":
    main()
''',

    "utils/io.py": r'''import streamlit as st
import pandas as pd
import os

@st.cache_data(show_spinner=False)
def load_data():
    """
    Loads the dataset.
    Requires 'global_air_quality_dataset.csv' in 'data/' folder.
    
    加载数据集。
    需要 'data/' 文件夹中包含 'global_air_quality_dataset.csv'。
    """
    file_path = 'data/global_air_quality_dataset.csv'
    
    if not os.path.exists(file_path):
        # Error handling if file is missing / 文件缺失时的错误处理
        st.error(f"Dataset missing: {file_path}")
        return None
        
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        return None
''',

    "utils/prep.py": r'''import pandas as pd
import numpy as np

def clean_data(df):
    """
    Data cleaning pipeline.
    1. Standardize column names.
    2. Handle missing values.
    3. Create AQI Categories.
    
    数据清洗流程。
    1. 标准化列名。
    2. 处理缺失值。
    3. 创建 AQI 类别。
    """
    # Strip whitespace / 去除空格
    df.columns = df.columns.str.strip()
    
    # Rename for consistency / 重命名以保持一致性
    rename_map = {
        'O3': 'Ozone', 
        'Temp': 'Temperature', 
        'Hum': 'Humidity'
    }
    df = df.rename(columns=rename_map)
    
    # Ensure Date format / 确保日期格式
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        
    # Numeric conversion / 数值转换
    numeric_cols = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'Ozone', 'Temperature', 'Humidity', 'Wind Speed']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    # Categorize PM2.5 (US EPA Standards) / PM2.5 分类（美国 EPA 标准）
    def categorize(pm):
        if pd.isna(pm): return "Unknown"
        if pm <= 12: return "Good"
        elif pm <= 35.4: return "Moderate"
        elif pm <= 55.4: return "Unhealthy (Sensitive)"
        elif pm <= 150.4: return "Unhealthy"
        elif pm <= 250.4: return "Very Unhealthy"
        else: return "Hazardous"

    if 'PM2.5' in df.columns:
        df['AQI Category'] = df['PM2.5'].apply(categorize)
        # Drop rows without PM2.5 data as it's our key metric / 删除没有 PM2.5 数据的行，因为这是关键指标
        df = df.dropna(subset=['PM2.5'])
        
    return df

def get_data_quality_report(df):
    """
    Returns basic stats about the dataset quality.
    返回有关数据集质量的基本统计信息。
    """
    return {
        "rows": len(df),
        "missing": df.isnull().sum().sum(),
        "duplicates": df.duplicated().sum()
    }
''',

    "utils/viz.py": r'''import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# Visualization Standards / 可视化标准
# Using a clean, academic color palette suitable for white backgrounds.
# 使用适合白色背景的简洁学术调色板。
# -----------------------------------------------------------------------------
TEMPLATE = "plotly_white"
COLOR_SCALE = "Blues" 

def plot_line_chart(df, x, y, title, color=None):
    """
    Generate a standard line chart.
    生成标准折线图。
    """
    # Aggregate to avoid messy lines if multiple points exist per date
    # 聚合以避免每日期存在多个点时线条混乱
    if color:
        df_agg = df.groupby([x, color])[y].mean().reset_index()
    else:
        df_agg = df.groupby(x)[y].mean().reset_index()
        
    fig = px.line(
        df_agg, x=x, y=y, color=color,
        title=title,
        template=TEMPLATE
    )
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Concentration Level",
        legend_title="Region"
    )
    return fig

def plot_map(df):
    """
    Generate a choropleth map.
    生成等值区域地图。
    """
    # Aggregate by country for the map / 按国家聚合地图数据
    df_agg = df.groupby('Country')['PM2.5'].mean().reset_index()
    
    fig = px.choropleth(
        df_agg,
        locations='Country',
        locationmode='country names',
        color='PM2.5',
        title="Global PM2.5 Intensity Map",
        color_continuous_scale="Reds",
        template=TEMPLATE
    )
    fig.update_layout(geo=dict(showframe=False, showcoastlines=False))
    return fig

def plot_bar_chart(df, x, y, title):
    """
    Generate a horizontal bar chart.
    生成水平条形图。
    """
    fig = px.bar(
        df, x=x, y=y,
        orientation='h',
        title=title,
        template=TEMPLATE,
        color=x,
        color_continuous_scale="RdBu_r"
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig

def plot_scatter(df, x, y, size, color, title):
    """
    Generate a bubble chart for correlation analysis.
    生成用于相关性分析的气泡图。
    """
    # Sampling to improve performance / 采样以提高性能
    if len(df) > 2000:
        df_plot = df.sample(2000)
    else:
        df_plot = df
        
    fig = px.scatter(
        df_plot, x=x, y=y, size=size, color=color,
        title=title,
        template=TEMPLATE,
        opacity=0.6
    )
    return fig
''',

    "sections/intro.py": r'''import streamlit as st
from utils import prep

def render(df_raw):
    st.title("Project Context & Methodology")
    st.markdown("### Introduction")
    
    st.markdown("""
    This dashboard presents a comprehensive analysis of global air quality data. 
    The primary objective is to identify pollution patterns, understand meteorological influences, and highlight regional disparities.
    
    **Research Questions:**
    1.  Which regions exhibit the highest PM2.5 concentrations?
    2.  Is there a correlation between weather parameters (Wind, Temperature) and pollution?
    3.  How does air quality evolve over time in major urban centers?
    """)
    
    st.markdown("---")
    
    # Data Quality Section / 数据质量部分
    st.subheader("Data Quality Assessment")
    
    report = prep.get_data_quality_report(df_raw)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Observations", report['rows'])
    col2.metric("Missing Values", report['missing'])
    col3.metric("Duplicate Records", report['duplicates'])
    
    with st.expander("View Methodology & Limitations"):
        st.markdown("""
        **Methodology:**
        * Data was sourced from open air quality monitoring datasets.
        * **PM2.5** is used as the primary indicator for air health.
        * AQI categories follow the simplified US EPA standards.
        
        **Limitations:**
        * Spatial coverage is limited to available monitoring stations.
        * Temporal gaps may exist for certain regions.
        """)
''',

    "sections/overview.py": r'''import streamlit as st
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
''',

    "sections/deep_dives.py": r'''import streamlit as st
from utils import viz

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
        
        if 'Wind Speed' in df.columns and 'Temperature' in df.columns:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                fig_bubble = viz.plot_scatter(
                    df, x='Wind Speed', y='PM2.5',
                    size='PM10', color='Temperature',
                    title="Wind Speed vs PM2.5 (Color=Temperature)"
                )
                st.plotly_chart(fig_bubble, use_container_width=True)
                
            with col2:
                st.markdown("""
                **Insight:**
                
                The scatter plot typically reveals a **negative correlation** between wind speed and PM2.5 concentration. 
                High wind speeds facilitate dispersion, reducing local pollution levels.
                """)
        else:
            st.warning("Weather data (Wind/Temperature) missing.")
''',

    "sections/conclusions.py": r'''import streamlit as st

def render():
    st.title("Conclusions & Strategic Insights")
    
    st.markdown("""
    ### Summary of Findings
    Based on the analysis performed, the following conclusions are drawn:
    
    1.  **Regional Disparity:** Pollution is not uniformly distributed. Developing nations and specific industrial hubs show significantly higher baselines.
    2.  **Environmental Determinants:** Weather plays a crucial role. Stagnant air (low wind) is a major catalyst for hazardous air quality events.
    3.  **Urban Challenges:** Major metropolitan areas consistently face PM2.5 levels exceeding WHO safety guidelines.
    
    ---
    
    ### Recommendations
    
    **For Policy:**
    * Strengthen emission regulations in identified hotspots.
    * Implement dynamic traffic control based on weather forecasts (e.g., low wind days).
    
    **For Future Research:**
    * Incorporate satellite data to cover rural areas.
    * Analyze hour-by-hour data to identify peak emission times.
    """)
    
    st.success("Project analysis completed successfully.")
'''
}

def create_project():
    # Create directories / 创建目录
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}/")

    # Create dummy logos / 创建占位 Logo
    create_dummy_logos()
    print("Created placeholder logos in 'assets/'. Please replace them with your actual files.")

    # Create files / 创建文件
    for filepath, content in files.items():
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created file: {filepath}")

    print("\n" + "="*60)
    print("PROJECT UPDATE COMPLETE / 项目更新完成")
    print("="*60)
    print("Instructions / 下一步:")
    print("1. Replace 'assets/logo_wut.png' with your WUT logo.")
    print("2. Replace 'assets/logo_efrei.png' with your EFREI logo.")
    print("3. Ensure 'global_air_quality_dataset.csv' is in 'data/'.")
    print("4. Run: streamlit run app.py")

if __name__ == "__main__":
    create_project()