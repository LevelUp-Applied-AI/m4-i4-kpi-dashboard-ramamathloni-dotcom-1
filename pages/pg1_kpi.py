import dash
from dash import html, dcc
import plotly.graph_objects as go

dash.register_page(__name__, path='/', name="Dashboard Overview")

layout = html.Div([
    html.H2("Key Performance Indicators"),
    dcc.Graph(
        figure=go.Figure(go.Indicator(
            mode="gauge+number",
            value=94, # القيمة اللي طلعت معك بالصور
            title={'text': "Customer Retention %"},
            gauge={'bar': {'color': "darkblue"}}
        ))
    )
])