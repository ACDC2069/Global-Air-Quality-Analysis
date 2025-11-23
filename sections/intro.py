import streamlit as st
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
