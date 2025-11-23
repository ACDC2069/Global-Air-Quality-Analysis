import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# Visualization Standards / 可视化标准
# -----------------------------------------------------------------------------
TEMPLATE = "plotly_white"
COLOR_SCALE = "Reds" # Changed to Reds for pollution warning feel / 改为红色系以体现警示感

def plot_line_chart(df, x, y, title, color=None):
    """
    Generate a standard line chart with markers.
    生成带有标记的标准折线图。
    """
    if color:
        df_agg = df.groupby([x, color])[y].mean().reset_index()
    else:
        df_agg = df.groupby(x)[y].mean().reset_index()
        
    fig = px.line(
        df_agg, x=x, y=y, color=color,
        title=title,
        template=TEMPLATE,
        markers=True # Enable markers to make points clearer / 启用标记点
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="PM2.5 Concentration (µg/m³)",
        legend_title="Region",
        hovermode="x unified"
    )
    return fig

def plot_map(df):
    """
    Generate a high-contrast choropleth map.
    生成高对比度的等值区域地图。
    """
    # Aggregate by country / 按国家聚合
    df_agg = df.groupby('Country')['PM2.5'].mean().reset_index()
    
    fig = px.choropleth(
        df_agg,
        locations='Country',
        locationmode='country names',
        color='PM2.5',
        title="Global PM2.5 Intensity Map",
        color_continuous_scale=COLOR_SCALE,
        template=TEMPLATE,
        hover_name="Country",
        hover_data={"PM2.5": ":.2f"}
    )
    
    # --- KEY FIXES FOR VISIBILITY / 针对可见性的关键修复 ---
    fig.update_geos(
        # 1. Show land for missing countries / 显示无数据国家的陆地
        showland=True, 
        landcolor="#E5E5E5", # Light gray land / 浅灰陆地
        
        # 2. Show distinct borders / 显示清晰边界
        showcountries=True, 
        countrycolor="#333333", # Dark gray borders / 深灰边界
        countrywidth=1.0,       # Thicker borders / 加宽边界
        
        # 3. Show ocean context / 显示海洋背景
        showocean=True, 
        oceancolor="#F5F5F5", # Matches app background / 与应用背景融合
        
        # 4. Show coastlines / 显示海岸线
        showcoastlines=True,
        coastlinecolor="#333333",
        
        # 5. Better projection / 更好的投影
        projection_type="natural earth", 
        
        # 6. Auto-zoom if few countries selected / 如果选中国家较少则自动缩放
        # If fewer than 10 countries are shown, zoom in. Otherwise show world.
        fitbounds="locations" if len(df_agg) > 0 and len(df_agg) < 10 else False
    )
    
    # Adjust margin and height / 调整边距和高度
    fig.update_layout(
        margin={"r":0,"t":40,"l":0,"b":0},
        height=500,
        coloraxis_colorbar_title="PM2.5"
    )
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
        color_continuous_scale="RdBu_r",
        text_auto='.1f' # Show values on bars / 在条形上显示数值
    )
    fig.update_layout(
        yaxis={'categoryorder':'total ascending'}, # Sort bars / 排序
        xaxis_title="PM2.5 Concentration",
        yaxis_title=""
    )
    return fig

def plot_scatter(df, x, y, size, color, title):
    """
    Generate a bubble chart with better transparency.
    生成透明度更好的气泡图。
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
        opacity=0.6,
        size_max=40, # Limit max bubble size / 限制最大气泡尺寸
        hover_data=['City']
    )
    fig.update_layout(
        xaxis_title=x,
        yaxis_title=y
    )
    return fig