# Top Performers
# Imports ----
import dash
from dash import dcc
from dash import html
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash_table.Format import Format, Scheme, Trim

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gdp
import json

from my_pandas_extensions.plotting_plotly import *
#from my_pandas_extensions.database import collect_data

from app import app

# Data ----
#wells_final_df, production_final_df = collect_data()
wells_final_df = pd.read_pickle("datasets/wells_final_Q42021_df.pkl")
#production_final_df = pd.read_pickle("datasets/production_final_Q42021_df.pkl")

shapes = gdp.read_file('assets/produccin-hidrocarburos-concesiones-de-explotacin-shp.shp')
json_dict = json.loads(shapes.to_json())

areas_dict = {
    'AGUADA_BAGUALES': "BAG",
    'AGUADA_CANEPA':'AGUADA_CANEPA',
    'AGUADA_DEL_CHANAR': "AGUH",
    'AGUADA_DEL_CHIVATO-AGUADA_BO': "AGZ",
    'AGUADA_DE_CASTRO': "AGCA",
    'AGUADA_DE_LA_ARENA':"AGA",
    'AGUADA_FEDERAL':"AFED",
    'AGUADA_PICHANA_ESTE': "APE",
    'AGUADA_PICHANA_OESTE':"APO",
    'AGUA_DEL_CAJON':"CAO",
    'AGUILA_MORA':'AGUILA_MORA',
    'AL_NORTE_DE_LA_DORSAL':"NDD",
    'BAJADA_DEL_PALO_OESTE':"BAPO",
    'BAJADA_DE_ANELO':"BANE",
    'BAJO_DEL_CHOIQUE-LA_INVERNADA':"BCLI",
    'BAJO_DEL_TORO':'BAJO_DEL_TORO',
    'BANDURRIA_CENTRO':"BNDC",
    'BANDURRIA_NORTE':"BNDN",
    'BANDURRIA_SUR':"BNDS",
    'CENTENARIO':"CEN",
    'CERRO_ARENA':'CERRO_ARENA',
    'CERRO_AVISPA':'CERRO_AVISPA',
    'CERRO_LAS_MINAS':'CERRO_LAS_MINAS',
    'CERRO_PARTIDO':'CERRO_PARTIDO',
    'CHIHUIDO_DE_LA_SIERRA_NEGRA':"CSN",
    'CINCO_SALTOS':'CINCO_SALTOS',
    'COIRON_AMARGO_SUR_ESTE':"CANC",
    'COIRON_AMARGO_SUR_OESTE':'COIRON_AMARGO_SUR_OESTE',
    'CORRALERA':'CORRALERA',
    'COVUNCO_NORTE_SUR':'COVUNCO_NORTE_SUR',
    'CRUZ_DE_LORENA':"CDLO",
    'EL_MANGRULLO':"GRU",
    'EL_MANZANO_OESTE_(RESTO)':"EMOR",
    'EL_OREJANO':"ELOR",
    'EL_TRAPIAL-CURAMCHED':"HUA",
    'FORTIN_DE_PIEDRA':"FOR",
    'LAS_MANADAS':"LSMA",
    'LAS_TACANAS':'LAS_TACANAS',
    'LA_AMARGA_CHICA':"LAC",
    'LA_CALERA':"LCA",
    'LA_ESCALONADA':"LAES",
    'LA_RIBERA_BLOQUE_I':"LRIB",
    'LA_RIBERA_BLOQUE_II':"LRII",
    'LINDERO_ATRAVESADO':"LAT",
    'LOMA_AMARILLA_NORTE':'LOMA_AMARILLA_NORTE',
    'LOMA_AMARILLA_SUR':"LOAS",
    'LOMA_ANCHA':'LOMA_ANCHA',
    'LOMA_CAMPANA':"LCAM",
    'LOMA_DEL_MOLLE':'LOMA_DEL_MOLLE',
    'LOMA_JARILLOSA_ESTE-PUESTO_SIL':"LJE",
    'LOMA_LA_LATA-SIERRA_BARROSA':"LDL",
    'LOMA_RANQUELES':'LOMA_RANQUELES',
    'LOS_TOLDOS_II_ESTE':"LTE2",
    'LOS_TOLDOS_II_OESTE':'LOS_TOLDOS_II_OESTE',
    'LOS_TOLDOS_I_NORTE':"LTN1",
    'LOS_TOLDOS_I_SUR':"LTS1",
    'MATA_MORA':'MATA_MORA',
    'MESETA_BUENA_ESPERANZA':"MBE",
    'NEUQUEN_DEL_MEDIO':"NME",
    'PAMPA_DE_LAS_YEGUAS_I':"PDYI",
    'PAMPA_DE_LAS_YEGUAS_II':'PAMPA_DE_LAS_YEGUAS_II',
    'PARVA_NEGRA_ESTE':'PARVA_NEGRA_ESTE',
    'PAYUN_OESTE':'PAYUN_OESTE',
    'PUESTO_ROJAS':"PURO",
    'RINCON_DEL_MANGRULLO':"RDM",
    'RINCON_DE_ARANDA':"RDA",
    'RINCON_LA_CENIZA':"RLCZ",
    'SAN_ROQUE':"SRO",
    'SIERRAS_BLANCAS':"SBLA",
    'SIERRA_CHATA':"SICH"
}

wells_df = wells_final_df.copy()
wells_df['area_code'] = wells_df['area'].map(areas_dict)

wells_df = wells_df \
    .query(f"well_type == 'Horizontal'")
    
#wells_df = wells_df \
#    .query(f"well_type == 'Horizontal'") \
#    .query(f"produced_fluid == 'Oil'")
    
wells_df_col_select = ['well_name', 
                      'longitude', 'latitude',
                      #'completion_date', 
                      'fluid_type','area', 'area_code','operator','campaign',
                      'well_type', 'produced_fluid', 
                      #'horizontal_length', 'number_of_stages','stage_spacing',
                      #'fluid_volume_m3','proppant_volume_lbm',
                      'max_qo_bpd', 'cum180_oil_bbl',
                      'max_qg_mscfd', 'cum180_gas_mscf',
                      'eur_total_mboeq']

wells_df = wells_df[wells_df_col_select]

wells_df = wells_df.sort_values('cum180_oil_bbl', ascending=False)
    
# Creating an ID column name gives us more interactive capabilities
wells_df['id'] = wells_df['well_name']
wells_df.set_index('id', inplace=True, drop=True)
#print(wells_final_df.columns)

# Building App Layout ----
layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                       html.Div(id='container_tab6_dt_graph'),  
                    ], width={'size':3, 'offset':0}, style={"height": "100%"}
                ),
                dbc.Col(
                    [
                        dash_table.DataTable(
                            id='dt_tab6_interactive',
                            data=wells_df.to_dict('records'),  # the contents of the table
                            columns=[
                                {'name': 'Well Name', 'id': 'well_name', 'type': 'text', "deletable": False, "selectable": False, "hideable": False},
                                {'name': 'Longitude', 'id': 'longitude', 'type': 'numeric', "deletable": False, "selectable": False, "hideable": False, 'format':Format(precision=4, scheme=Scheme.fixed)},
                                {'name': 'Latitude', 'id': 'latitude', 'type': 'numeric', "deletable": False, "selectable": False, "hideable": False, 'format':Format(precision=4, scheme=Scheme.fixed)},
                                {'name': 'Area', 'id': 'area', 'type': 'text', "deletable": False, "selectable": False, "hideable": False},
                                {'name': 'Area Code', 'id': 'area_code', 'type': 'text', "deletable": False, "selectable": False, "hideable": True},
                                {'name': 'Operator', 'id': 'operator', 'type': 'text', "deletable": False, "selectable": False, "hideable": False},
                                {'name': 'Campaign', 'id': 'campaign', 'type': 'text', "deletable": False, "selectable": False, "hideable": False},
                                {'name': 'Well Type', 'id': 'well_type', 'type': 'text', "deletable": False, "selectable": False, "hideable": False},
                                {'name': 'Prod Fluid', 'id': 'produced_fluid', 'type': 'text', "deletable": False, "selectable": False, "hideable": False},
                                {'name': 'Fluid Type', 'id': 'fluid_type', 'type': 'text', "deletable": False, "selectable": False, "hideable": False},
                                {'name': 'Max Qo, bpd', 'id': 'max_qo_bpd', 'type': 'numeric', "deletable": False, "selectable": True, "hideable": False, 'format':Format(precision=0, scheme=Scheme.fixed).group(True)},
                                {'name': '6-Mo Cum Oil, bbl', 'id': 'cum180_oil_bbl', 'type': 'numeric', "deletable": False, "selectable": True, "hideable": False, 'format':Format(precision=0, scheme=Scheme.fixed).group(True)},
                                {'name': 'Max Qg, mscfd', 'id': 'max_qg_mscfd', 'type': 'numeric', "deletable": False, "selectable": True, "hideable": False, 'format':Format(precision=0, scheme=Scheme.fixed).group(True)},
                                {'name': '6-Mo Cum Gas, Mscf', 'id': 'cum180_gas_mscf', 'type': 'numeric', "deletable": False, "selectable": True, "hideable": False, 'format':Format(precision=0, scheme=Scheme.fixed).group(True)},
                                {'name': 'EUR, Mboeq', 'id': 'eur_total_mboeq', 'type': 'numeric', "deletable": False, "selectable": True, "hideable": False, 'format':Format(precision=0, scheme=Scheme.fixed).group(True)},
                            ],
                            
                            #columns=[
                            #    {"name": i, "id": i, "deletable": False, "selectable": True, "hideable": False, 'type':'numeric', 'format':Format(precision=0, scheme=Scheme.fixed)}
                            #    if i == 'max_qo_bpd' or i == 'cum180_oil_bbl' or i == "max_qg_mscfd" or i == "cum180_gas_mscf" or i == "eur_total_mboeq"
                            #    else {"name": i, "id": i, "deletable": True, "selectable": False, "hideable": True}
                            #    for i in wells_df.columns
                            #],
                            
                            #fixed_rows={'headers': True},
                            editable=False,              # allow editing of data inside all cells
                            filter_action="native",     # allow filtering of data by user ('native') or not ('none')
                            sort_action="native",       # enables data to be sorted per-column by user or not ('none')
                            sort_mode="single",         # sort across 'multi' or 'single' columns
                            column_selectable="single",  # allow users to select 'multi' or 'single' columns
                            row_selectable="multi",     # allow users to select 'multi' or 'single' rows
                            row_deletable=False,        # choose if user can delete a row (True) or not (False)
                            selected_columns=['cum180_oil_bbl'],        # ids of columns that user selects
                            selected_rows=[],           # indices of rows that user selects
                            hidden_columns=['longitude','latitude','well_type','produced_fluid','area_code'],        # ids of columns that user selects
                            page_action="native",       # all data is passed to the table up-front or not ('none')
                            page_current=0,             # page number that user is on
                            page_size=10,                # number of rows visible per page
                            #style_table={'overflowX': 'auto'},
                            style_cell={
                                'overflow': 'hidden',
                                'textOverflow': 'ellipsis',
                                'font_size': '15px',
                                'maxWidth': 0
                                #'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                            },
                            style_cell_conditional=[    # align text columns to left. By default they are aligned to right
                                {'if': {'column_id': 'area'},'width': '15%'},
                                {'if': {'column_id': 'max_qo_bpd'},'width': '8%'},
                                {'if': {'column_id': 'cum180_oil_bbl'},'width': '10%'},
                                {'if': {'column_id': 'max_qg_mscfd'},'width': '8%'},
                                {'if': {'column_id': 'cum180_gas_mscf'},'width': '10%'},
                                {'if': {'column_id': 'eur_total_mboeq'},'width': '8%'},
                                {'if': {'column_id': 'well_name'},'textAlign': 'left'},
                                {'if': {'column_id': 'area'},'textAlign': 'left'},
                                {'if': {'column_id': 'operator'},'textAlign': 'left'},
                                {'if': {'column_id': 'fluid_type'},'textAlign': 'left'},
                                {'if': {'column_id': 'campaign'},'textAlign': 'left'},
                            ],
                            style_data_conditional=(
                                [
                                    {
                                        'if': {
                                            'filter_query': '{{{}}} = ""'.format(col),
                                            'column_id': col
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    } for col in wells_df.columns
                                ]
                            ),
                            style_header={
                                #'backgroundColor': 'blue',
                                'fontWeight': 'bold'
                            },
                            style_header_conditional=[    # align text columns to left. By default they are aligned to right
                                {
                                    'if': {'column_id': c},
                                    'textAlign': 'left'
                                } for c in ['well_name', 'longitude', 'latitude', 'area', 'area_code', 'operator', 
                                            'fluid_type', 'campaign', 'well_type', 'produced_fluid']
                            ],
                            style_as_list_view=True,
                            #style_data={                # overflow cells' content into multiple lines
                            #    'whiteSpace': 'normal',
                            #    'height': 'auto'
                            #}
                            #tooltip_data=[
                            #    {
                            #        column: {'value': str(value), 'type': 'markdown'}
                            #        for column, value in row.items()
                            #    } for row in wells_df.to_dict('records')
                            #],
                            #tooltip_duration=None
                        ),
                    ], style={"height": "100%"}, width={'size': 9, "offset": 0}
                ),
            ], className="h-50", align="center", justify='start'
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                       dcc.Graph(
                            id = 'graph_tab6_dt_map', config={'displayModeBar': False, 'scrollZoom': True}, className='mh-10'
                        ),
                    ], width={'size':6, 'offset':0}, style={"height": "100%"}
                ),
                dbc.Col(
                    [
                        dcc.Graph(
                            id = 'graph_tab6_boxplot', className='mh-10'
                        ), 
                    ], width={'size':4, 'offset':0}, style={"height": "100%"}
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                   [
                                        html.P(
                                                "Choose produced fluid:",
                                                className="card-text",
                                            ),
                                        dcc.RadioItems(
                                            id = 'ri_tab6_prod_fluid',
                                            options=[
                                                {'label': 'Oil', 'value': 'Oil'},
                                                {'label': 'Gas', 'value': 'Gas'}],
                                            value='Oil',
                                            labelClassName="mt-0 ml-5",
                                            style = {'font-size': '13px'}
                                        ),
                                    ], className="p-1"
                                )
                            ], className="mt-2 mb-2 pb-2"
                        ),
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.P(
                                                "Choose filter variable:",
                                                className="card-text",
                                            ),
                                        dcc.RadioItems(
                                            id = 'ri_tab6_filter_var',
                                            options=[
                                                {'label': 'Fluid Type', 'value': 'fluid_type'},
                                                {'label': 'Area', 'value': 'area'},
                                                {'label': 'Operator', 'value': 'operator'},
                                                {'label': 'Campaign', 'value': 'campaign'}],
                                            value='fluid_type',
                                            labelClassName="mt-0 ml-2",
                                            style = {'font-size': '13px'}
                                        ),
                                    ], className="p-1"
                                )
                            ], className="mt-2 mb-2 pb-2"
                        ),
                    ], style={"height": "100%"}, width={'size': 2, "offset": 0}
                ),
            ], className="h-40", align="center", justify='start'
        )
    ], style={"height": "100vh"}, fluid=True
)

# Callbacks-------------------------------------------------------------------------------------
# Callback to generate boxplot ----
@app.callback(
    Output('graph_tab6_boxplot', 'figure'),
    [Input('dt_tab6_interactive', "derived_virtual_data"),
     Input('dt_tab6_interactive', 'derived_virtual_selected_rows'),
     Input('dt_tab6_interactive', 'selected_columns'),
     Input('ri_tab6_prod_fluid', 'value'),
     Input('ri_tab6_filter_var', 'value')])

def graph_production_rate(rows, derived_virtual_selected_rows,selected_columns, ri_fluid, ri_filter_var):
    
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []
    
    if selected_columns == []:
        if ri_fluid == 'Oil':
            column = "cum180_oil_bbl"
        if ri_fluid == 'Gas':
            column = "cum180_gas_mscf"
    else:
        column = selected_columns[0]
    
    dff = wells_df if rows is None else pd.DataFrame(rows)
    
    fig = dff \
        .boxplot_no_agg(column,ri_filter_var,
        sort_category = True, flip_coord = True,
        produced_fluid = ri_fluid,
        title = f'Boxplot of {column} by {ri_filter_var}')
    
    fig.update_layout(height=500, font=dict(size=10))
    fig.update_layout(margin=dict(t=40, r=20, l=20, b=20))
    return fig

# Callback to color selected column ----
# Select column
@app.callback(
    Output('dt_tab6_interactive', 'style_data_conditional'),
    Input('dt_tab6_interactive', 'selected_columns')
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

# Callback to generate bar graph ----
# Create bar chart
@app.callback(
    Output('container_tab6_dt_graph', 'children'),
    [Input('dt_tab6_interactive', "derived_virtual_data"),
     Input('dt_tab6_interactive', 'derived_virtual_selected_rows'),
     Input('dt_tab6_interactive', 'selected_columns'),
     Input('ri_tab6_prod_fluid', 'value')]
)
    
def update_bar_graph(rows, derived_virtual_selected_rows, selected_columns,ri_fluid):
    
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []
        
    if selected_columns == []:
        if ri_fluid == 'Oil':
            column = "cum180_oil_bbl"
        if ri_fluid == 'Gas':
            column = "cum180_gas_mscf"
    else:
        column = selected_columns[0]
        
    dff = wells_df if rows is None else pd.DataFrame(rows)
    dff = dff.head(10)
    
    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff))]
    return [
            dcc.Graph(
                id='bar_column',
                figure={
                    "data": [
                        {
                            "y": dff["well_name"],
                            "x": dff[column],
                            "type": "bar",
                            "orientation":'h',
                            "marker": {"color": colors},
                        }
                    ],
                    "layout": {
                        "xaxis": {"automargin": True,
                                  "title": {"text": column},
                                  
                        },
                        "yaxis": {
                            "automargin": True,
                            "categoryorder": "total ascending"
                        },
                        "height": 470,
                        "margin": {"t": 20, "l": 20, "r": 20},
                        "font": {'size':10}
                    },
                },
            )
        ]

# Callback to generate map ----

@app.callback(
    Output('graph_tab6_dt_map', 'figure'),
    [Input('dt_tab6_interactive', "derived_virtual_data"),
     Input('dt_tab6_interactive', 'derived_virtual_selected_rows'),
     Input('dt_tab6_interactive', 'selected_columns'),
     Input('ri_tab6_prod_fluid', 'value')]
)
def update_map(rows, derived_virtual_selected_rows, selected_columns, ri_fluid):
    
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []
        
    if selected_columns == []:
        if ri_fluid == 'Oil':
            column = "cum180_oil_bbl"
        if ri_fluid == 'Gas':
            column = "cum180_gas_mscf"
    else:
        column = selected_columns[0]
        
    dff = wells_df if rows is None else pd.DataFrame(rows)
    
    dff = dff.query(f"{column} == {column}")
    
    #print(derived_virtual_selected_rows)
    #print(dff.iloc[derived_virtual_selected_rows])
    
    col_dff = dff\
                .groupby(['area','area_code'])[column].mean().reset_index(name="col_mean")
        
    # highlight selected wells on map
    # if derived_virtual_selected_rows == []:
    #     marker_size = [6 for i in range(len(dff))]
    # else:
    #     marker_size = [30 if i in derived_virtual_selected_rows else 6
    #             for i in range(len(dff))]
    
    fig = go.Figure(go.Choroplethmapbox(geojson=json_dict, 
                                        locations=col_dff.area_code, 
                                        z=col_dff.col_mean,
                                        colorscale = 'icefire',
                                        # zmin = 0,
                                        # zmid = 10000,
                                        # zmax = 30000,
                                        featureidkey="properties.CODIGODESE",
                                        text=col_dff.area,
                                        hovertemplate=
                                                    "<b>%{text}</b><br><br>" +
                                                    "Indicator: %{z:,.0f}<br>" +
                                                    "<extra></extra>",
                                        marker_opacity=0.5, 
                                        marker_line_width=1))
    
    fig.add_scattermapbox(
                        lat = dff['latitude'],
                        lon = dff['longitude'],
                        below='',
                        mode = 'markers',
                        selectedpoints=derived_virtual_selected_rows,
                        marker = dict(
                                color = dff[column],
                                #size = marker_size,
                                size = 6,
                                opacity = 0.5,
                                symbol = 'circle',
                                colorscale= "icefire"
                                ),
                        unselected={'marker' : {'opacity':0.5}},
                        selected={'marker' : {'opacity':0.5, 
                                              'size':25,
                                            #   'line':{'width':2,
                                            #           'color':'DarkSlateGrey'
                                            #           }
                                              }
                                  },
                        text=dff[column],
                        customdata=dff['well_name'],
                        hovertemplate = "Well: %{customdata}</b><br><br>" +
                                        "Indicator: %{text}<br>" +
                                        "Longitude: %{lon}<br>" +
                                        "Latitude: %{lat}<br>" +
                                        "<extra></extra>",
                        )
    
    fig.update_layout(uirevision= 'foo', #preserves state of figure/map after callback activated
                      #clickmode= 'event+select',
                      hovermode='closest',
                      mapbox_style="carto-positron",
                      mapbox_zoom=8, 
                      mapbox_center = {"lat": -38.0986, "lon": -68.746998})
    
    fig.update_layout(height=500, margin={"r":0,"t":0,"l":60,"b":0})
    
    return fig
