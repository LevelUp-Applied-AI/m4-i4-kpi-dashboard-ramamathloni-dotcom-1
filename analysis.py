"""Integration 4 — KPI Dashboard: Amman Digital Market Analytics

Extract data from PostgreSQL, compute KPIs, run statistical tests,
and create visualizations for the executive summary.

Usage:
    python analysis.py
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sqlalchemy import create_engine


def connect_db():
    """Create a SQLAlchemy engine connected to the amman_market database.

    Returns:
        engine: SQLAlchemy engine instance

    Notes:
        Use DATABASE_URL environment variable if set, otherwise default to:
        postgresql://postgres:postgres@localhost:5432/amman_market
    """
    # TODO: Create and return a SQLAlchemy engine using DATABASE_URL or a default
    engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5432/amman_market")
    return engine


def extract_data(engine):
    """Extract all required tables from the database into DataFrames.

    Args:
        engine: SQLAlchemy engine connected to amman_market

    Returns:
        dict: mapping of table names to DataFrames
              (e.g., {"customers": df, "products": df, "orders": df, "order_items": df})
    """
    # TODO: Query each table and return a dictionary of DataFrames
    df_customers = pd.read_sql("SELECT * FROM customers", engine)
    df_products = pd.read_sql("SELECT * FROM products", engine)
    df_orders = pd.read_sql("SELECT * FROM orders", engine)
    df_items = pd.read_sql("SELECT * FROM order_items", engine)

    ##data cleaning 
    df_orders = df_orders[df_orders['status'] != 'cancelled']
    df_items = df_items[df_items['quantity'] <= 100]

    return df_customers, df_products, df_orders, df_items


def compute_kpis(data_dict):
    """Compute the 5 KPIs defined in kpi_framework.md.

    Args:
        data_dict: dict of DataFrames from extract_data()

    Returns:
        dict: mapping of KPI names to their computed values (or DataFrames
              for time-series / cohort KPIs)

    Notes:
        At least 2 KPIs should be time-based and 1 should be cohort-based.
    """
    # TODO: Join tables as needed, then compute each KPI from your framework
    df_customers = data_dict['customers']
    df_products = data_dict['products']
    df_orders = data_dict['orders']
    df_orders['order_date'] = pd.to_datetime(df_orders['order_date'])

    df_items = data_dict['order_items']

    df_merged = df_items.merge(df_products, on='product_id')
    df_merged = df_merged.merge(df_orders, on='order_id')
    df_merged = df_merged.merge(df_customers, on='customer_id')
    
    #total price
    df_merged['total_price'] = df_merged['quantity'] * df_merged['unit_price']
    
    # KPI 1: Monthly Revenue (Time-based)
    df_merged['order_date'] = pd.to_datetime(df_merged['order_date'])

    # KPI 2: Revenue by City (Cohort/Segment-based)
    revenue_by_city = df_merged.groupby('city')['total_price'].sum()

    # KPI 3: Average Order Value (AOV) by Category
    aov_by_category = df_merged.groupby(['category', 'order_id'])['total_price'].sum().groupby('category').mean()

    # KPI 4: Weekly Order Volume (Time-based)
    weekly_orders = df_orders.resample('W', on='order_date')['order_id'].count()

    # KPI 5: Customer Retention (High-level metric)
    order_counts = df_orders.groupby('customer_id')['order_id'].count()
    retention_rate = (order_counts > 1).mean() * 100

    monthly_revenue = df_merged.resample('ME', on='order_date')['total_price'].sum()

    return {
        "monthly_revenue": monthly_revenue,
        "revenue_by_city": revenue_by_city,
        "aov_by_category": aov_by_category,
        "weekly_orders": weekly_orders,
        "retention_rate": retention_rate
    }


def run_statistical_tests(data_dict):
    """Run hypothesis tests to validate patterns in the data.

    Args:
        data_dict: dict of DataFrames from extract_data()

    Returns:
        dict: mapping of test names to results (test statistic, p-value,
              interpretation)

    Notes:
        Run at least one test. Consider:
        - Does average order value differ across product categories?
        - Is there a significant trend in monthly revenue?
        - Do customer cities differ in purchasing behavior?
    """
    # TODO: Select and run appropriate statistical tests
    df_orders = data_dict['orders']
    df_items = data_dict['order_items']
    df_products = data_dict['products']
    
    df_merged = df_items.merge(df_products, on='product_id')
    df_merged = df_merged.merge(df_orders, on='order_id')
    df_merged['total_price'] = df_merged['quantity'] * df_merged['unit_price']

    #ANOVA 
    categories = df_merged['category'].unique()
    group_data = [df_merged[df_merged['category'] == cat]['total_price'] for cat in categories]
    f_stat, p_val = stats.f_oneway(*group_data)

    # TODO: Interpret results (reject or fail to reject the null hypothesis)
    #Interpretation 
    alpha = 0.05
    if p_val < alpha:
        interpretation = "Reject H0: Significant difference exists across categories."
    else:
        interpretation = "Fail to reject H0: No significant difference found."

    return {
        "anova_product_categories": {
            "test_statistic": f_stat,
            "p_value": p_val,
            "interpretation": interpretation
        }
    }


def create_visualizations(kpi_results, stat_results):
    """Create publication-quality charts for all 5 KPIs.

    Args:
        kpi_results: dict from compute_kpis()
        stat_results: dict from run_statistical_tests()

    Returns:
        None

    Side effects:
        Saves at least 5 PNG files to the output/ directory.
        Each chart should have a descriptive title stating the finding,
        proper axis labels, and annotations where appropriate.
    """
    sns.set_theme(style="whitegrid")

    # 1. Monthly Revenue
    plt.figure(figsize=(10, 6))
    kpi_results['monthly_revenue'].plot(kind='line', marker='o', color='b')
    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Revenue ($)")
    plt.savefig("output/1_monthly_revenue.png")
    plt.close()

    # 2. Revenue by City
    plt.figure(figsize=(10, 6))
    kpi_results['revenue_by_city'].sort_values().plot(kind='barh', color='teal')
    plt.title("Revenue by City")
    plt.xlabel("Total Revenue ($)")
    plt.ylabel("City")
    plt.savefig("output/2_revenue_by_city.png")
    plt.close()

    # 3. AOV by Category
    plt.figure(figsize=(10, 6))
    kpi_results['aov_by_category'].plot(kind='bar', color='orange')
    plt.title("Average Order Value by Category")
    plt.xlabel("Category")
    plt.ylabel("Average Amount ($)")
    plt.savefig("output/3_aov_by_category.png")
    plt.close()

    # 4. Weekly Orders
    plt.figure(figsize=(10, 6))
    kpi_results['weekly_orders'].plot(kind='area', alpha=0.4, color='green')
    plt.title("Weekly Order Volume")
    plt.xlabel("Week")
    plt.ylabel("Number of Orders")
    plt.savefig("output/4_weekly_orders.png")
    plt.close()

    # 5. Retention Rate
    plt.figure(figsize=(6, 6))
    retention = kpi_results['retention_rate']
    plt.pie([retention, 100-retention], labels=['Repeat', 'One-time'], 
            autopct='%1.1f%%', colors=['skyblue', 'lightgrey'])
    plt.title(f"Customer Retention: {retention:.1f}%")
    plt.savefig("output/5_retention_rate.png")
    plt.close()


def main():
    os.makedirs("output", exist_ok=True)
    
    engine = connect_db()
    df_customers, df_products, df_orders, df_items = extract_data(engine)
    
    data_dict = {
        'customers': df_customers,
        'products': df_products,
        'orders': df_orders,
        'order_items': df_items
    }

    kpi_results = compute_kpis(data_dict)
    stat_results = run_statistical_tests(data_dict)
    create_visualizations(kpi_results, stat_results)

    print("Analysis Summary:")
    print(f"Retention Rate: {kpi_results['retention_rate']:.2f}%")
    print(f"ANOVA p-value: {stat_results['anova_product_categories']['p_value']:.4f}")


if __name__ == "__main__":
    main()