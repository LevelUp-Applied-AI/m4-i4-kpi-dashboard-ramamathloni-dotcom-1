import dash
from dash import html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine

dash.register_page(__name__, name="Time-Series Analysis")

engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5432/amman_market")

layout = html.Div([
    html.H2("Revenue Trends"),
    dcc.DatePickerRange(id='date-picker', start_date='2024-01-01', end_date='2025-12-31'),
    dcc.Graph(id='trend-graph')
])

@callback(Output('trend-graph', 'figure'), [Input('date-picker', 'start_date'), Input('date-picker', 'end_date')])
def update_graph(start, end):
    df = pd.read_sql(f"SELECT order_date, total_amount FROM orders WHERE order_date BETWEEN '{start}' AND '{end}'", engine)
    fig = px.line(df, x='order_date', y='total_amount', title="Revenue Over Time")
    return fig
