import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from sqlalchemy import create_engine
import os

def run_full_kpi_monitor():
    # 1. إعداد المسارات والاتصال
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, 'config.json')
    output_dir = os.path.join(base_dir, 'output')
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(config_path, 'r') as f:
        targets = json.load(f)

    # الاتصال بـ PostgreSQL
    engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5432/amman_market")

    # 2. سحب البيانات وحل مشكلة التاريخ
    df_orders = pd.read_sql("SELECT * FROM orders WHERE status != 'cancelled'", engine)
    df_items = pd.read_sql("SELECT * FROM order_items", engine)
    df_products = pd.read_sql("SELECT * FROM products", engine)
    
    # --- الحل الجذري للخطأ: تحويل العمود لتاريخ حقيقي ---
    df_orders['order_date'] = pd.to_datetime(df_orders['order_date'])
    
    # دمج البيانات للحسابات الأخرى
    df_merged = df_items.merge(df_products, on='product_id').merge(df_orders, on='order_id')
    df_merged['total_price'] = df_merged['quantity'] * df_merged['unit_price']
    df_merged['order_date'] = pd.to_datetime(df_merged['order_date'])

    # 3. الحسابات الفعلية للـ KPIs
    actual_revenue = df_merged['total_price'].sum()
    
    order_counts = df_orders.groupby('customer_id')['order_id'].count()
    actual_retention = (order_counts > 1).mean() * 100
    
    actual_aov = df_merged.groupby('order_id')['total_price'].sum().mean()
    
    # حساب Weekly Volume بدون TypeError
    weekly_counts = df_orders.resample('W', on='order_date')['order_id'].count()
    actual_weekly_vol = weekly_counts.mean() if not weekly_counts.empty else 0

    # 4. بناء العدادات (Gauges)
    fig = make_subplots(
        rows=2, cols=2, 
        specs=[[{'type': 'indicator'}, {'type': 'indicator'}],
               [{'type': 'indicator'}, {'type': 'indicator'}]],
        subplot_titles=("Total Revenue", "Retention Rate", "Avg Order Value", "Weekly Orders")
    )

    # العدادات مع الأهداف من الـ JSON
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta", value=actual_revenue,
        delta={'reference': targets.get('monthly_revenue_target', 25000)},
        gauge={'axis': {'range': [None, 40000]}, 'bar': {'color': "teal"}},
    ), row=1, col=1)

    fig.add_trace(go.Indicator(
        mode="gauge+number+delta", value=actual_retention,
        delta={'reference': targets.get('retention_rate_target', 90)},
        gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "royalblue"}},
    ), row=1, col=2)

    fig.add_trace(go.Indicator(
        mode="gauge+number+delta", value=actual_aov,
        delta={'reference': targets.get('avg_order_value_target', 50)},
        gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "orange"}},
    ), row=2, col=1)

    fig.add_trace(go.Indicator(
        mode="gauge+number+delta", value=actual_weekly_vol,
        delta={'reference': targets.get('weekly_orders_target', 10)},
        gauge={'axis': {'range': [None, 30]}, 'bar': {'color': "green"}},
    ), row=2, col=2)

    fig.update_layout(height=800, title_text="Amman Market KPI Monitoring Tool")

    # 5. الحفظ النهائي
    output_path = os.path.join(output_dir, 'monitor_gauges.html')
    fig.write_html(output_path)
    
    print("-" * 30)
    print(f"✅ Success! Monitor generated at: {output_path}")
    print("-" * 30)

if __name__ == "__main__":
    run_full_kpi_monitor()