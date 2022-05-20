# Area / Operators
import dash
from dash import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash_table.Format import Format, Scheme, Trim

import pandas as pd
import geopandas as gdp
import json

from pandas.core.arrays.categorical import factorize_from_iterables

from my_pandas_extensions.plotting_plotly import *
#from my_pandas_extensions.database import collect_data

from app import app

#wells_final_df, production_final_df = collect_data()
wells_final_df = pd.read_pickle("datasets/wells_final_Q42021_df.pkl")
production_final_df = pd.read_pickle("datasets/production_final_Q42021_df.pkl")

shapes = gdp.read_file('assets/produccin-hidrocarburos-concesiones-de-explotacin-shp.shp')
json_dict = json.loads(shapes.to_json())

#shapes = gdp.read_file('assets/NqnBasin_Unconventional_GeoWGS84.shp')
# with open('assets/areas2_dict.json', 'w') as f:
#     json.dump(json_dict, f)

# areas_dict3 = {
#     'AGUADA_BAGUALES': "BAG",
#     'AGUADA_CANEPA':143,
#     'AGUADA_DEL_CHANAR': 170,
#     'AGUADA_DEL_CHIVATO-AGUADA_BO': "AGZ",
#     'AGUADA_DE_CASTRO': 160,
#     'AGUADA_DE_LA_ARENA':229,
#     'AGUADA_FEDERAL':247,
#     'AGUADA_PICHANA_ESTE': 130,
#     'AGUADA_PICHANA_OESTE':84,
#     'AGUA_DEL_CAJON':228,
#     'AGUILA_MORA':47,
#     'AL_NORTE_DE_LA_DORSAL':"NDD",
#     'BAJADA_DEL_PALO_OESTE':31,
#     'BAJADA_DE_ANELO':147,
#     'BAJO_DEL_CHOIQUE-LA_INVERNADA':30,
#     'BAJO_DEL_TORO':28,
#     'BANDURRIA_CENTRO':199,
#     'BANDURRIA_NORTE':78,
#     'BANDURRIA_SUR':120,
#     'CENTENARIO':258,
#     'CERRO_ARENA':68,
#     'CERRO_AVISPA':'CERRO_AVISPA',
#     'CERRO_LAS_MINAS':239,
#     'CERRO_PARTIDO':'CERRO_PARTIDO',
#     'CHIHUIDO_DE_LA_SIERRA_NEGRA':250,
#     'CINCO_SALTOS':'CINCO_SALTOS',
#     'COIRON_AMARGO_SUR_ESTE':214,
#     'COIRON_AMARGO_SUR_OESTE':125,
#     'CORRALERA':97,
#     'COVUNCO_NORTE_SUR':169,
#     'CRUZ_DE_LORENA':243,
#     'EL_MANGRULLO':"GRU",
#     'EL_MANZANO_OESTE_(RESTO)':19,
#     'EL_OREJANO':18,
#     'EL_TRAPIAL-CURAMCHED':107,
#     'FORTIN_DE_PIEDRA':158,
#     'LAS_MANADAS':"LSMA",
#     'LAS_TACANAS':'LAS_TACANAS',
#     'LA_AMARGA_CHICA':"LAC",
#     'LA_CALERA':"LCA",
#     'LA_ESCALONADA':"LAES",
#     'LA_RIBERA_BLOQUE_I':"LRIB",
#     'LA_RIBERA_BLOQUE_II':"LRII",
#     'LINDERO_ATRAVESADO':"LAT",
#     'LOMA_AMARILLA_NORTE':'LOMA_AMARILLA_NORTE',
#     'LOMA_AMARILLA_SUR':"LOAS",
#     'LOMA_ANCHA':'LOMA_ANCHA',
#     'LOMA_CAMPANA':"LCAM",
#     'LOMA_DEL_MOLLE':'LOMA_DEL_MOLLE',
#     'LOMA_JARILLOSA_ESTE-PUESTO_SIL':"LJE",
#     'LOMA_LA_LATA-SIERRA_BARROSA':"LDL",
#     'LOMA_RANQUELES':'LOMA_RANQUELES',
#     'LOS_TOLDOS_II_ESTE':"LTE2",
#     'LOS_TOLDOS_II_OESTE':'LOS_TOLDOS_II_OESTE',
#     'LOS_TOLDOS_I_NORTE':"LTN1",
#     'LOS_TOLDOS_I_SUR':"LTS1",
#     'MATA_MORA':'MATA_MORA',
#     'MESETA_BUENA_ESPERANZA':"MBE",
#     'NEUQUEN_DEL_MEDIO':"NME",
#     'PAMPA_DE_LAS_YEGUAS_I':"PDYI",
#     'PAMPA_DE_LAS_YEGUAS_II':'PAMPA_DE_LAS_YEGUAS_II',
#     'PARVA_NEGRA_ESTE':'PARVA_NEGRA_ESTE',
#     'PAYUN_OESTE':'PAYUN_OESTE',
#     'PUESTO_ROJAS':"PURO",
#     'RINCON_DEL_MANGRULLO':212,
#     'RINCON_DE_ARANDA':"RDA",
#     'RINCON_LA_CENIZA':"RLCZ",
#     'SAN_ROQUE':"SRO",
#     'SIERRAS_BLANCAS':"SBLA",
#     'SIERRA_CHATA':"SICH"
# }

operators_dict = {
    'AMERICAS_PETROGAS':'AMERICAS PETROGAS ARGENTINA S.A.',
    'ARGENTA':'ARGENTA',
    'CAPEX':'CAPEX S.A.',
    'CHEVRON':'CHEVRON ARGENTINA S.R.L.',
    'EXXON_MOBIL':'EXXONMOBIL EXPLORATION ARGENTINA S.R.L.',
    'GEOPARK':'GEOPARK ARGENTINA LTD. (SUCURSAL ARGENTINA)',
    'MEDANITO':'MEDANITO S.A.',
    'OILSTONE':'OILSTONE ENERGIA S.A.',
    'PAE':'PAN AMERICAN ENERGY SL',
    'PAMPA':'PAMPA ENERGIA S.A.',
    'PHOENIX':'PHOENIX',
    'PLUSPETROL':'PLUSPETROL S.A.',
    'SHELL':'SHELL ARGENTINA S.A.',
    'SIN OPERADOR':'SIN OPERADOR',
    'TECPETROL':'TECPETROL S.A.',
    'TOTAL':'TOTAL AUSTRAL S.A.',
    'VISTA':'VISTA OIL & GAS ARGENTINA SAU',
    'WINTERSHALL':'WINTERSHALL DEA ARGENTINA S.A',
    'YPF':'YPF S.A.'
}

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

production_df = production_final_df.copy()
production_df['area_code'] = production_df['area'].map(areas_dict)
production_df['operator_code'] = production_df['operator'].map(operators_dict)

# layout ----
layout = dbc.Container(
    [
        dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H6("Completed Wells"),
                                    html.H3(id="prod_wells_3", children="", style={'fontWeight':'bold'})
                                ], className="p-1"
                            )
                        ], className="mt-2 mb-2 pb-2",
                    )
                ], style={"height": "100%"}, width={'size': 2, "offset": 0, 'order': 1}
            ),
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H6(id="prod_rate_3_title", children=""),
                                    html.H3(id="prod_rate_3", children="", style={'fontWeight':'bold'})
                                ], className="p-1"
                            )
                        ], className="mt-2 mb-2 pb-2",
                    )
                ], style={"height": "100%"}, width={'size': 2, "offset": 0, 'order': 2}
            ),
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H6(id="cum_prod_3_title", children=""),
                                    html.H3(id="cum_prod_3", children="", style={'fontWeight':'bold'})
                                ], className="p-1"
                            )
                        ], className="mt-2 mb-2 pb-2",
                    )
                ], style={"height": "100%"}, width={'size': 2, "offset": 0, 'order': 3}
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
                                            id = 'ri_tab4_prod_fluid',
                                            options=[
                                                {'label': 'Oil', 'value': 'Oil'},
                                                {'label': 'Gas', 'value': 'Gas'}],
                                            value='Oil',
                                            labelClassName="mt-0 ml-2",
                                            style = {'font-size': '13px'}
                                    ),
                                ], className="p-1"
                            )
                        ], className="mt-2 mb-2 pb-3"
                    ),
                ], style={"height": "100%"}, width={'size': 2, "offset": 0, 'order': 4}
            ),
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.P(
                                            "Choose the filter variable:",
                                            className="card-text",
                                        ),
                                    dcc.RadioItems(
                                            id = 'area_operator_radio',
                                            options=[
                                                {'label': 'Area', 'value': 'area'},
                                                {'label': 'Operator', 'value': 'operator'}],
                                            value='area',
                                            labelClassName="mt-0 ml-2",
                                            style = {'font-size': '13px'}
                                    ),
                                ], className="p-1"
                            )
                        ], className="mt-2 mb-2 pb-3",
                    )
                ], style={"height": "100%"}, width={'size': 2, "offset": 0, 'order': 5}
            ),
            dbc.Col(
                [
                    dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.P(
                                            "Choose the Area/Operator:",
                                            className="card-text",
                                        ),
                                        dcc.Dropdown(id='drop_area_op',
                                            #options=[],
                                            #value=None,
                                            clearable = False,
                                            multi=False,
                                            style = {'font-size': '13px'}
                                        ) 
                                    ], className="p-1"
                                )
                            ], className="mt-2 mb-2 pb-2"
                        ),
                ], style={"height": "100%"}, width={'size': 2, "offset": 0, 'order': 6}
            )
        ], className="h-10", justify='start'
    ),
    dbc.Row(
        [
            dbc.Col(
                [
                   dcc.Graph(
                        id = 'area_agg_prod_fig'
                    ),
                   dcc.Graph(
                        id = 'area_prod_fig'
                    ) 
                ], width={'size':4, 'offset':0}, style={"height": "100%"}
            ),
            dbc.Col(
                [
                   dcc.Graph(
                        id = 'area_agg_cum_fig'
                    ),
                   dcc.Graph(
                        id = 'area_cum_fig'
                    ) 
                ], width={'size':4, 'offset':0}, style={"height": "100%"}
            ),
            dbc.Col(
                [
                    dcc.Graph(
                        id = 'map_fig'
                    )
                ], width={'size':4, 'offset':0}, style={"height": "100%"}
            ),
            dcc.Store(id='prod_df_3')
        ], className="h-60", align="start", justify='around'
    )         
    ], style={"height": "100vh"}, fluid=True
)

#----------------------------------------------
# Callback to configure the dropdown
@app.callback( 
    [Output('drop_area_op', 'options'),
     Output('drop_area_op', 'value')],
    [Input('area_operator_radio','value')]
)

def drop_options(area_op_radio):
    
    if area_op_radio == 'area':
        area_op_options=[{'label': x, 'value': x} for x in sorted(production_df["area"].unique())]
        area_op_value = 'AGUADA_FEDERAL'
    else:
        area_op_options=[{'label': x, 'value': x} for x in sorted(production_df["operator"].unique())]
        area_op_value = 'WINTERSHALL'
    
    return area_op_options, area_op_value

#----------------------------------------------
# Callback to filter well_df dataframe
@app.callback( 
    Output('prod_df_3', 'data'),
    [Input('drop_area_op', 'value'),
     Input('area_operator_radio','value')]
)

def process_data(area_op_str,area_op_radio):
    
    if area_op_str == None:
        prod_df=production_df  \
            .query(f"well_name != 'BCeCg-111(h)'") \
            .query(f"well_name != 'BCeCf-101(h)'") \
            .query(f"well_name != 'BCeCf-105(h)'") \
            .query(f"well_name != 'BCeCg-112(h)'") \
            .query(f"well_name != 'BCeAe-113(h)'") \
            .query(f"well_name != 'BCeCf-108(h)'") \
            .query(f"well_name != 'BCeCf-106(h)'")
    
        prod_df = prod_df.rename(columns={'production_date':'date'})
    else:
        if area_op_radio == 'area': 
            prod_df=production_df  \
                    .query(f"well_name != 'BCeCg-111(h)'") \
                    .query(f"well_name != 'BCeCf-101(h)'") \
                    .query(f"well_name != 'BCeCf-105(h)'") \
                    .query(f"well_name != 'BCeCg-112(h)'") \
                    .query(f"well_name != 'BCeAe-113(h)'") \
                    .query(f"well_name != 'BCeCf-108(h)'") \
                    .query(f"well_name != 'BCeCf-106(h)'")

            prod_df=prod_df[prod_df['area']==area_op_str]
            prod_df = prod_df.rename(columns={'production_date':'date'})
    
        elif area_op_radio == 'operator':
            prod_df=production_df  \
                    .query(f"well_name != 'BCeCg-111(h)'") \
                    .query(f"well_name != 'BCeCf-101(h)'") \
                    .query(f"well_name != 'BCeCf-105(h)'") \
                    .query(f"well_name != 'BCeCg-112(h)'") \
                    .query(f"well_name != 'BCeAe-113(h)'") \
                    .query(f"well_name != 'BCeCf-108(h)'") \
                    .query(f"well_name != 'BCeCf-106(h)'")

            prod_df=prod_df[prod_df['operator']==area_op_str]
            prod_df = prod_df.rename(columns={'production_date':'date'})

    prod_df_json = prod_df.to_json()
    return prod_df_json

#----------------------------------------------
# Callback to update map
@app.callback(
            Output('map_fig', 'figure'),
             [Input('prod_df_3', 'data')]
             )

def map_figure_update(df_json):
        df = pd.read_json(df_json, convert_axes=True, convert_dates=True)

        df = df.rename(columns={
                'date':'production_date'
            })
            
        area_op_oil_cum_df = df.groupby(["operator","operator_code",'area','area_code'])["oil_month_bbl"].sum().reset_index(name="oil_cum")

        fig = px.choropleth_mapbox(area_op_oil_cum_df, 
                    geojson=json_dict, 
                    color='oil_cum',
                    locations='area_code', 
                    featureidkey="properties.CODIGODESE",
                    range_color=[0, 20000000],
                    labels={'operator':'Operator','area':'Area','oil_cum':'Cum. Oil, bbl'},
                    hover_data = {'operator':True, 'operator_code':False, 'area':True, 'area_code':False,'oil_cum':True},
                    center={'lat':-38.0986,'lon':-68.746998},
                    mapbox_style="carto-positron", 
                    zoom=8,
                    opacity = 0.5
                    )
        fig.update_geos(fitbounds="locations", visible=False)
            
        fig.update_layout(height=750)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        
        return fig

#----------------------------------------------
# Callback to generate agg prod plot ----
@app.callback(
    [Output('area_agg_prod_fig', 'figure'),
     Output('area_agg_cum_fig', 'figure')],
    [Input('prod_df_3', 'data'),
     Input('ri_tab4_prod_fluid', 'value'),
     Input('area_operator_radio','value')]
    )

def area_agg_image(df_json, ri_prod_fluid_value, area_op_radio):
    
    df = pd.read_json(df_json, convert_axes=True, convert_dates=True)
    df = df.rename(columns={
                'date':'production_date'
            })
    
    if ri_prod_fluid_value == "Oil":
    
        if area_op_radio == 'area':
            fig_prod = df.area_plot_agg('production_date', 'oil_month_bpd', 'area', 
                                        title="Oil Production Rate vs. Date", agg_func = np.sum)
            fig_cum = df.area_plot_agg('production_date', 'oil_month_bbl', 'area', cumsum = 'Y',
                                       title="Oil Production Volume vs. Date",agg_func = np.sum)

        elif area_op_radio == 'operator':
            fig_prod = df.area_plot_agg('production_date', 'oil_month_bpd', 'operator', 
                                        title="Oil Production Rate vs. Date", agg_func = np.sum)
            fig_cum = df.area_plot_agg('production_date', 'oil_month_bbl', 'operator', cumsum = 'Y',
                                       title="Oil Production Volume vs. Date",agg_func = np.sum)
            
    else:
        
        if area_op_radio == 'area':
            fig_prod = df.area_plot_agg('production_date', 'gas_month_mscf_d', 'area', 
                                        title="Gas Production Rate vs. Date", agg_func = np.sum)
            fig_cum = df.area_plot_agg('production_date', 'gas_month_mscf', 'area', cumsum = 'Y',
                                       title="Gas Production Volume vs. Date",agg_func = np.sum)

        elif area_op_radio == 'operator':
            fig_prod = df.area_plot_agg('production_date', 'gas_month_mscf_d', 'operator', 
                                        title="Gas Production Rate vs. Date", agg_func = np.sum)
            fig_cum = df.area_plot_agg('production_date', 'gas_month_mscf', 'operator', cumsum = 'Y',
                                       title="Gas Production Volume vs. Date",agg_func = np.sum)
    
    fig_prod.update_layout(height=400, width=500)
    fig_prod.update_layout(margin=dict(t=40, r=40, l=40, b=40),font=dict(size=10))
    
    fig_cum.update_layout(height=400, width=500)
    fig_cum.update_layout(margin=dict(t=40, r=40, l=40, b=40),font=dict(size=10))
    
    return fig_prod, fig_cum

#----------------------------------------------
# Callback to generate cum plot per well ----
@app.callback(
    [Output('area_prod_fig', 'figure'),
     Output('area_cum_fig', 'figure')],
    [Input('prod_df_3', 'data'),
     Input('ri_tab4_prod_fluid', 'value')])

def area_cum_image(df_json, ri_prod_fluid_value):
    
    df = pd.read_json(df_json, convert_axes=True, convert_dates=True)
    df = df.rename(columns={
                'date':'production_date'
            })
    
    if ri_prod_fluid_value == "Oil":
        fig_prod = df.line_well_prod_plot_no_agg('cum_eff_prod_day', 'oil_month_bpd', 'well_name',
        title="Oil Production Rate vs. Time", plot_type = 'rate', normalized = False)
    
        fig_cum = df.line_well_prod_plot_no_agg('cum_eff_prod_day', 'cum_oil_bbl', 'well_name',
        title="Oil Production Volume vs. Time", plot_type = 'volume', normalized = False)
        
    else:
        fig_prod = df.line_well_prod_plot_no_agg('cum_eff_prod_day', 'gas_month_mscf_d', 'well_name',
        title="Oil Production Rate vs. Time", plot_type = 'rate', normalized = False)
    
        fig_cum = df.line_well_prod_plot_no_agg('cum_eff_prod_day', 'cum_gas_mscf', 'well_name',
        title="Oil Production Volume vs. Time", plot_type = 'volume', normalized = False)
    
    fig_prod.update_layout(height=400, width=500)
    fig_prod.update_layout(margin=dict(t=40, r=40, l=40, b=40), font=dict(size=10))
    
    fig_cum.update_layout(height=400, width=500)
    fig_cum.update_layout(margin=dict(t=40, r=40, l=40, b=40), font=dict(size=10))
    
    return fig_prod, fig_cum

#----------------------------------------------
# Callback to update cards
@app.callback(
    Output('prod_wells_3','children'),
    Output('cum_prod_3', 'children'),
    Output('prod_rate_3', 'children'),
    Output('cum_prod_3_title', 'children'),
    Output('prod_rate_3_title', 'children'),
    [Input('prod_df_3', 'data'),
     Input('ri_tab4_prod_fluid', 'value')])

def wells_prod(df_json, ri_prod_fluid_value):

    df = pd.read_json(df_json, convert_axes=True, convert_dates=True)
    df = df.rename(columns={'date':'production_date'})
    
    if ri_prod_fluid_value == "Oil":
        table1_df = df[["well_name", 'production_date',  'oil_month_bbl', 
                            'oil_month_bpd', 'production_status']] \
            .groupby('well_name') \
            .agg({
                'oil_month_bbl' : ['sum'],
                }) \
            .reset_index()
            
        table1_df = table1_df.set_axis(
            ["_".join(col).rstrip("_") for col in table1_df.columns.tolist()],axis = 1)     
            
        table1_df = table1_df \
                .agg({'well_name' : ['count'],
                    'oil_month_bbl_sum' : ['sum'],
                    }) \
                .reset_index(drop=True) \
                .fillna(0) \
                .agg({'well_name' : ['sum'],
                    'oil_month_bbl_sum' : ['sum'],
                    }) \
                .reset_index(drop=True) \
                .rename({'well_name':'Completed Wells',
                        'oil_month_bbl_sum': 'Total Cum. Oil Prod., bbl',
                        }, axis=1)

        table1_df['Completed Wells']=(table1_df['Completed Wells']).map("{:,.0f}".format)
        table1_df['Total Cum. Oil Prod., MMbbl']=(table1_df['Total Cum. Oil Prod., bbl']/1000000).map("{:,.2f}".format)

        table2_df = df[["well_name", 'production_date',  'cum_oil_bbl', 
                            'oil_month_bpd', 'production_status']] \
            .assign(max_prod_date = lambda x: x.production_date.max()) \
            .query(f"production_date == max_prod_date") \
            .query(f"production_status == 'Producing'") \
            .agg({'oil_month_bpd' : ['sum']}) \
            .reset_index(drop=True) \
            .fillna(0) \
            .agg({'oil_month_bpd' : ['sum']}) \
            .reset_index(drop=True) \
            .rename({'oil_month_bpd': 'Total Oil Prod. Rate, bbl/d'}, axis=1)

        table2_df['Total Oil Prod. Rate, bbl/d']=table2_df['Total Oil Prod. Rate, bbl/d'].map("{:,.0f}".format)
    
        prod_wells = table1_df['Completed Wells']
        cum_prod = table1_df['Total Cum. Oil Prod., MMbbl']
        prod_rate = table2_df['Total Oil Prod. Rate, bbl/d']
        cum_prod_title = "Total Cum. Oil Prod., MMbbl"
        prod_rate_title = "Total Oil Prod. Rate, bbl/d"
        
    else:
        table1_df = df[["well_name", 'production_date',  'gas_month_mscf', 
                            'gas_month_mscf_d', 'production_status']] \
            .groupby('well_name') \
            .agg({
                'gas_month_mscf' : ['sum'],
                }) \
            .reset_index()
            
        table1_df = table1_df.set_axis(
            ["_".join(col).rstrip("_") for col in table1_df.columns.tolist()],axis = 1)     
            
        table1_df = table1_df \
                .agg({'well_name' : ['count'],
                    'gas_month_mscf_sum' : ['sum'],
                    }) \
                .reset_index(drop=True) \
                .fillna(0) \
                .agg({'well_name' : ['sum'],
                    'gas_month_mscf_sum' : ['sum'],
                    }) \
                .reset_index(drop=True) \
                .rename({'well_name':'Completed Wells',
                        'gas_month_mscf_sum': 'Total Cum. Gas Prod., Mscf',
                        }, axis=1)

        table1_df['Completed Wells']=(table1_df['Completed Wells']).map("{:,.0f}".format)
        table1_df['Total Cum. Gas Prod., Bcf']=(table1_df['Total Cum. Gas Prod., Mscf']/1000000).map("{:,.2f}".format)

        table2_df = df[["well_name", 'production_date',  'cum_gas_mscf', 
                            'gas_month_mscf_d', 'production_status']] \
            .assign(max_prod_date = lambda x: x.production_date.max()) \
            .query(f"production_date == max_prod_date") \
            .query(f"production_status == 'Producing'") \
            .agg({'gas_month_mscf_d' : ['sum']}) \
            .reset_index(drop=True) \
            .fillna(0) \
            .agg({'gas_month_mscf_d' : ['sum']}) \
            .reset_index(drop=True) \
            .rename({'gas_month_mscf_d': 'Total Gas Prod. Rate, Mscf/d'}, axis=1)

        table2_df['Total Gas Prod. Rate, Mscf/d']=table2_df['Total Gas Prod. Rate, Mscf/d'].map("{:,.0f}".format)
    
        prod_wells = table1_df['Completed Wells']
        cum_prod = table1_df['Total Cum. Gas Prod., Bcf']
        prod_rate = table2_df['Total Gas Prod. Rate, Mscf/d']
        cum_prod_title = "Total Cum. Gas Prod., Bcf"
        prod_rate_title = "Total Gas Prod. Rate, Mscf/d"

    return prod_wells, cum_prod, prod_rate, cum_prod_title, prod_rate_title