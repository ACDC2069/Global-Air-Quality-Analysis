import streamlit as st
# --- ADDED machine_learning to imports / 添加 machine_learning 导入 ---
from sections import intro, overview, deep_dives, conclusions, machine_learning
from utils import io, prep
import base64

# -----------------------------------------------------------------------------
# Page Configuration / 页面配置
# Academic and professional layout settings.
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Global Air Quality Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Custom Styling / 自定义样式
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    /* Sidebar Background / 侧边栏背景 - Premium Dark Blue */
    section[data-testid="stSidebar"] {
        background-color: #001529;
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
    
    /* Main Content Background / 主内容背景 - Light Gray */
    .stApp {
        background-color: #F5F5F5;
    }
    
    /* Metric Styling / 指标样式 - Clean Blue */
    div[data-testid="stMetricValue"] {
        font-family: 'Arial', sans-serif;
        color: #003366; /* Dark Blue */
    }
    </style>
    """, unsafe_allow_html=True)

# --- Helper for Logos / Logo 辅助函数 ---
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

def main():
    """
    Main Application Logic.
    """
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
      
        # 2. Project Info
        st.markdown("### Global Air Quality Analysis")
        st.caption("Air quality analysis including major cities around the world")
        
        st.markdown("---")
        
        # 3. Contact Info
        st.markdown("**Professor & Student**")
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

        # 4. Filters
        st.subheader("Configuration")
        
        df_raw = io.load_data()
        if df_raw is None:
            st.error("Data not found.")
            return

        df_clean = prep.clean_data(df_raw)
        if df_clean is None:
            st.stop()

        all_countries = sorted(df_clean['Country'].unique())
        
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

        df_filtered = df_clean[df_clean['Country'].isin(selected_countries)]
        
        st.markdown("---")
        
        # 5. Navigation
        st.subheader("Navigation")
        # --- Added "AI Prediction Simulator" to menu / 添加新页面到菜单 ---
        page = st.radio(
            "Go to:",
            ["Project Context", 
             "Overview & Trends", 
             "Deep Dives", 
             "AI Prediction Simulator",  # <--- NEW PAGE / 新页面
             "Conclusions"],
            label_visibility="collapsed"
        )

    # -------------------------------------------------------------------------
    # Main Page Routing / 页面路由
    # -------------------------------------------------------------------------
    if page == "Project Context":
        intro.render(df_raw)
    elif page == "Overview & Trends":
        overview.render(df_filtered)
    elif page == "Deep Dives":
        deep_dives.render(df_filtered)
    elif page == "AI Prediction Simulator": # <--- Render NEW PAGE / 渲染新页面
        # We use the full dataset (df_clean) for training to get better accuracy and generalization.
        # 我们使用完整数据集 (df_clean) 进行训练，以获得更好的准确性和泛化能力。
        machine_learning.render(df_clean) 
    elif page == "Conclusions":
        conclusions.render()

if __name__ == "__main__":
    main()