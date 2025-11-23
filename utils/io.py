import streamlit as st
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
