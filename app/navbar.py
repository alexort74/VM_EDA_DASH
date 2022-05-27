import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from dash_bootstrap_components._components.Container import Container

WD_LOGO = "/assets//descarga.png"

def Navbar():
  navbar = dbc.Navbar(
      dbc.Container(
        [
          html.A([
              # Use row and col to control vertical alignment of logo / brand
              dbc.Row(
                  [
                    dbc.Col(
                      [
                        html.Img(src=WD_LOGO, width="200px", height="30px")
                      ], style={"height": "100%"}, width={'size': 2, "offset": 0}
                    ),
                    dbc.Col(
                      [
                        dbc.NavbarBrand("Vaca Muerta EDA")
                      ], style={"height": "100%"}, width={'size': 2, "offset": 0}
                    ),
                    dbc.Col(
                      [
                        dbc.Nav(
                          [
                            dbc.NavLink("Wells", active="exact", href="/apps/app_tab1.py", id="page-1-link"),
                            dbc.NavLink("Production", active="exact", href="/apps/app_tab2.py", id="page-2-link"),
                            dbc.NavLink("Areas/Operators", active="exact", href="/apps/app_tab4.py", id="page-4-link"),
                            dbc.NavLink("Type Curves", active="exact", href="/apps/app_tab5.py", id="page-5-link"),
                            dbc.NavLink("Top Performers", active="exact", href="/apps/app_tab6.py", id="page-6-link"),
                            dbc.NavLink("Prod. Indicators", active="exact", href="/apps/app_tab3.py", id="page-3-link"),
                            dbc.NavLink("Completion", active="exact", href="/apps/app_tab7.py", id="page-7-link"),
                          ], horizontal='between', pills=True #className="me-auto", 
                        )
                        #dbc.Nav(
                        #  [
                        #    dbc.NavItem(dbc.NavLink("Wells", active="exact", href="/apps/app_tab1.py"), id="page-1-link"),
                        #    dbc.NavItem(dbc.NavLink("Production", active="exact", href="/apps/app_tab2.py"), id="page-2-link"),
                        #    dbc.NavItem(dbc.NavLink("Areas/Operators", active="exact", href="/apps/app_tab4.py"), id="page-4-link"),
                        #    dbc.NavItem(dbc.NavLink("Type Curves", active="exact", href="/apps/app_tab5.py"), id="page-5-link"),
                        #    dbc.NavItem(dbc.NavLink("Top Performers", active="exact", href="/apps/app_tab6.py"), id="page-6-link"),
                        #    dbc.NavItem(dbc.NavLink("Prod. Indicators", active="exact", href="/apps/app_tab3.py"), id="page-3-link"),
                        #    dbc.NavItem(dbc.NavLink("Completion", active="exact", href="/apps/app_tab7.py"), id="page-7-link"),
                        #  ], fill = True, horizontal='between', pills=True #className="me-auto", 
                        #)
                      ], style={"height": "100%", 'font-size': '14px'}, width={'size': 7, "offset": 0} 
                    ),
                    dbc.Col(
                        [
                          html.P("By: Alexis Ortega", className = 'text-white pt-3 ml-3')
                        ], style={"height": "100%", 'font-size': '10px'}, width={'size': 1, "offset": 0} 
                    )    
                  ], justify='around', align="center", className="g-0"
              ),
            ], style={"width": "100%"}, href="https://wintershalldea.com/en",
          ),
        ],fluid=True
      ),
      color="rgb(0, 39, 86)",
      dark=True,
      sticky="top",
      #expand="lg",
      style={'height': '4rem'},
  )
  return navbar