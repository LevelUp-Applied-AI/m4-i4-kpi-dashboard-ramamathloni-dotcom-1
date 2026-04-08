"""Tests for the KPI dashboard analysis.

Write at least 3 tests:
1. test_extraction_returns_dataframes — extract_data returns a dict of DataFrames
2. test_kpi_computation_returns_expected_keys — compute_kpis returns a dict with your 5 KPI names
3. test_statistical_test_returns_pvalue — run_statistical_tests returns results with p-values
"""
import pytest
import pandas as pd
from analysis import connect_db, extract_data, compute_kpis, run_statistical_tests


def test_extraction_returns_dataframes():
    """Connect to the database, extract data, and verify the result is a dict of DataFrames."""
    # TODO: Call connect_db and extract_data, then assert the result is a dict
    #       with DataFrame values for each expected table
    engine = connect_db()
    results = extract_data(engine)
    
    # التأكد أن النتيجة ليست فارغة وأنها تحتوي على الجداول المطلوبة
    assert isinstance(results, tuple) or isinstance(results, list)
    for df in results:
        assert isinstance(df, pd.DataFrame)


def test_kpi_computation_returns_expected_keys():
    """Compute KPIs and verify the result contains all expected KPI names."""
    # TODO: Extract data, call compute_kpis, then assert the returned dict
    #       contains the keys matching your 5 KPI names
    engine = connect_db()
    df_customers, df_products, df_orders, df_items = extract_data(engine)
    
    data_dict = {
        'customers': df_customers,
        'products': df_products,
        'orders': df_orders,
        'order_items': df_items
    }
    
    kpi_results = compute_kpis(data_dict)
    
    expected_kpis = [
        "monthly_revenue", 
        "revenue_by_city", 
        "aov_by_category", 
        "weekly_orders", 
        "retention_rate"
    ]
    
    for kpi in expected_kpis:
        assert kpi in kpi_results


def test_statistical_test_returns_pvalue():
    """Run statistical tests and verify results include p-values."""
    # TODO: Extract data, call run_statistical_tests, then assert at least
    #       one result contains a numeric p-value between 0 and 1
    engine = connect_db()
    df_customers, df_products, df_orders, df_items = extract_data(engine)
    
    data_dict = {
        'customers': df_customers,
        'products': df_products,
        'orders': df_orders,
        'order_items': df_items
    }
    
    stat_results = run_statistical_tests(data_dict)
    
    # التأكد من وجود نتيجة اختبار ANOVA وقيمة p-value صحيحة
    assert "anova_product_categories" in stat_results
    p_val = stat_results["anova_product_categories"]["p_value"]
    assert 0 <= p_val <= 1