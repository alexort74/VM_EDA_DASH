# Index
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import app_tab1, app_tab2, app_tab3, app_tab4, app_tab5, app_tab6, app_tab7

from navbar import Navbar
nav = Navbar()

app.layout = dbc.Container(
    [ 
        nav,
        dcc.Location(
                id='url', refresh=False
        ),
        html.Div(
                id='page-content', children=[]
        )
    ], fluid=True
)

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    #if pathname == '/apps/app_tab1.py':
    #    return app_tab1.layout
    if pathname == '/apps/app_tab2.py':
        return app_tab2.layout
    if pathname == '/apps/app_tab3.py':
        return app_tab3.layout
    if pathname == '/apps/app_tab4.py':
        return app_tab4.layout
    if pathname == '/apps/app_tab5.py':
        return app_tab5.layout
    if pathname == '/apps/app_tab6.py':
        return app_tab6.layout
    if pathname == '/apps/app_tab7.py':
        return app_tab7.layout
    else:
        return app_tab1.layout

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)