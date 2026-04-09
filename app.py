import dash
from dash import html, dcc

# تفعيل خاصية الصفحات المتعددة
app = dash.Dash(__name__, use_pages=True)

# تصميم القائمة العلوية والتنقل
app.layout = html.Div([
    html.Div([
        html.H1("Amman Digital Market - Tier 3 Analytics", 
                style={'color': 'white', 'textAlign': 'center', 'fontFamily': 'Arial'}),
        
        # إنشاء روابط التنقل تلقائياً بناءً على ملفات مجلد pages
        html.Div([
            dcc.Link(f"{page['name']}", href=page["relative_path"], 
                     style={'margin': '0 20px', 'color': '#f1c40f', 'fontSize': '18px', 'textDecoration': 'none', 'fontWeight': 'bold'})
            for page in dash.page_registry.values()
        ], style={'textAlign': 'center', 'paddingBottom': '10px'})
    ], style={'backgroundColor': '#2c3e50', 'padding': '20px', 'marginBottom': '20px'}),

    # المكان اللي رح ينعرض فيه محتوى كل صفحة
    html.Div(dash.page_container, style={'padding': '20px'})
], style={'backgroundColor': '#f4f7f6', 'minHeight': '100vh'})

if __name__ == '__main__':
    # التعديل المهم: استخدام app.run بدلاً من app.run_server للنسخ الحديثة
    app.run(debug=True)