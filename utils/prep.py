import pandas as pd
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
