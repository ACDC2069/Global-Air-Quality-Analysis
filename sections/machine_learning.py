import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
import plotly.express as px

def render(df):
    st.title("AI Prediction Simulator")
    st.markdown("""
    ### Machine Learning Model: Random Forest Regressor
    
    This module uses a machine learning model to understand the complex relationships between weather conditions, 
    gaseous pollutants, and PM2.5 levels. You can use the sidebar simulators to perform **"What-if" analysis**.
    
    此模块使用机器学习模型来理解天气条件、气态污染物和 PM2.5 水平之间的复杂关系。
    您可以使用侧边栏模拟器进行假设分析。
    """)
    
    # -------------------------------------------------------------------------
    # 1. Data Preparation / 数据准备
    # -------------------------------------------------------------------------
    # Select features for the model / 选择模型特征
    # We use weather and other pollutants to predict PM2.5
    feature_cols = ['Temperature', 'Humidity', 'Wind Speed', 'NO2', 'SO2', 'CO', 'Ozone']
    target_col = 'PM2.5'
    
    # Drop missing values for ML / 删除缺失值
    df_ml = df[feature_cols + [target_col]].dropna()
    
    X = df_ml[feature_cols]
    y = df_ml[target_col]
    
    # Split data / 分割数据
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # -------------------------------------------------------------------------
    # 2. Model Training / 模型训练
    # -------------------------------------------------------------------------
    with st.spinner('Training AI Model... (This may take a moment)'):
        # Initialize and train Random Forest / 初始化并训练随机森林
        model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        # Calculate metrics / 计算指标
        score_r2 = r2_score(y_test, y_pred)
        score_mae = mean_absolute_error(y_test, y_pred)

    # -------------------------------------------------------------------------
    # 3. Model Performance Display / 模型性能展示
    # -------------------------------------------------------------------------
    st.subheader("Model Performance")
    col1, col2 = st.columns(2)
    col1.metric("Model Accuracy (R² Score)", f"{score_r2:.2%}", help="How well the model explains the variance.")
    col2.metric("Avg Error (MAE)", f"{score_mae:.2f} µg/m³", help="Average difference between predicted and actual values.")
    
    st.markdown("---")

    # -------------------------------------------------------------------------
    # 4. Interactive Simulator / 交互式模拟器
    # -------------------------------------------------------------------------
    st.subheader("Pollution Simulator")
    
    col_input, col_result = st.columns([1, 2])
    
    with col_input:
        st.markdown("**Adjust Conditions:**")
        
        # Create sliders for inputs based on data ranges / 基于数据范围创建滑块
        input_data = {}
        for col in feature_cols:
            min_val = float(df[col].min())
            max_val = float(df[col].max())
            avg_val = float(df[col].mean())
            
            input_data[col] = st.slider(
                f"{col}", 
                min_value=min_val, 
                max_value=max_val, 
                value=avg_val
            )
            
    with col_result:
        # Predict using user inputs / 使用用户输入进行预测
        input_df = pd.DataFrame([input_data])
        prediction = model.predict(input_df)[0]
        
        # Display Prediction / 显示预测结果
        st.markdown("### Predicted PM2.5 Level")
        
        # Dynamic Color Logic / 动态颜色逻辑
        if prediction <= 12: color = "green"
        elif prediction <= 35: color = "#FFC107" # Amber
        else: color = "red"
        
        st.markdown(f"""
        <div style="
            background-color: {color}; 
            padding: 20px; 
            border-radius: 10px; 
            text-align: center; 
            color: white;
            font-size: 40px; 
            font-weight: bold;
            margin-bottom: 20px;">
            {prediction:.2f} µg/m³
        </div>
        """, unsafe_allow_html=True)
        
        # Categorize / 分类说明
        if prediction <= 12: category = "Good"
        elif prediction <= 35: category = "Moderate"
        elif prediction <= 55: category = "Unhealthy (Sensitive)"
        else: category = "Unhealthy / Hazardous"
        
        st.info(f"Predicted Category: **{category}**")
        st.caption("Try moving the 'Wind Speed' slider to see how it clears the pollution!")

    st.markdown("---")

    # -------------------------------------------------------------------------
    # 5. Feature Importance / 特征重要性
    # -------------------------------------------------------------------------
    st.subheader("Feature Importance")
    st.markdown("Which factors contribute most to the PM2.5 prediction?")
    
    # Extract importance / 提取重要性
    importance = pd.DataFrame({
        'Feature': feature_cols,
        'Importance': model.feature_importances_
    }).sort_values(by='Importance', ascending=True)
    
    fig = px.bar(
        importance, 
        x='Importance', 
        y='Feature', 
        orientation='h',
        title="Impact of Factors on PM2.5",
        template="plotly_white",
        color='Importance',
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig, use_container_width=True)
    