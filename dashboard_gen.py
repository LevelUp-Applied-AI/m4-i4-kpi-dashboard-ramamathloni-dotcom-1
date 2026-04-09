import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
import os

def generate_interactive_dashboard():
    # 1. Database Connection (using your settings)
    engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5432/amman_market")
    
    # 2. Extract Data
    df_customers = pd.read_sql("SELECT * FROM customers", engine)
    df_products = pd.read_sql("SELECT * FROM products", engine)
    df_orders = pd.read_sql("SELECT * FROM orders", engine)
    df_items = pd.read_sql("SELECT * FROM order_items", engine)

    # 3. Data Cleaning (Matching your analysis.py)
    df_orders = df_orders[df_orders['status'] != 'cancelled']
    df_items = df_items[df_items['quantity'] <= 100]
    df_orders['order_date'] = pd.to_datetime(df_orders['order_date'])

    # 4. Merging for KPI computation
    df_merged = df_items.merge(df_products, on='product_id')
    df_merged = df_merged.merge(df_orders, on='order_id')
    df_merged = df_merged.merge(df_customers, on='customer_id')
    df_merged['total_price'] = df_merged['quantity'] * df_merged['unit_price']

    # --- Compute your 5 KPIs and Create Plotly Figures ---

    # KPI 1: Monthly Revenue Trend
    monthly_rev = df_merged.resample('ME', on='order_date')['total_price'].sum().reset_index()
    fig1 = px.line(monthly_rev, x='order_date', y='total_price', markers=True,
                  title="Monthly Revenue Trend", labels={'total_price': 'Total Revenue ($)'})

    # KPI 2: Revenue by City
    rev_city = df_merged.groupby('city')['total_price'].sum().sort_values().reset_index()
    fig2 = px.bar(rev_city, x='total_price', y='city', orientation='h',
                  title="Revenue by City", color_discrete_sequence=['teal'])

    # KPI 3: AOV by Category
    aov_cat = df_merged.groupby(['category', 'order_id'])['total_price'].sum().groupby('category').mean().reset_index()
    fig3 = px.bar(aov_cat, x='category', y='total_price', 
                  title="Average Order Value by Category", color_discrete_sequence=['orange'])

    # KPI 4: Weekly Order Volume
    weekly_orders = df_orders.resample('W', on='order_date')['order_id'].count().reset_index()
    fig4 = px.area(weekly_orders, x='order_date', y='order_id', 
                   title="Weekly Order Volume", color_discrete_sequence=['green'])

    # KPI 5: Customer Retention
    order_counts = df_orders.groupby('customer_id')['order_id'].count()
    retention_val = (order_counts > 1).mean() * 100
    fig5 = px.pie(names=['Repeat', 'One-time'], values=[retention_val, 100-retention_val],
                  title=f"Customer Retention: {retention_val:.1f}%",
                  color_discrete_sequence=['skyblue', 'lightgrey'])

    # 5. Save to HTML
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, 'dashboard.html')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("<html><head><title>Amman Digital Market Dashboard</title></head><body>")
        f.write("<h1 style='text-align: center;'>Amman Digital Market Analytics (Interactive)</h1>")
        for fig in [fig1, fig2, fig3, fig4, fig5]:
            f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write("</body></html>")

    print(f"✅ Dashboard successfully generated: {output_path}")

if __name__ == "__main__":
    generate_interactive_dashboard()