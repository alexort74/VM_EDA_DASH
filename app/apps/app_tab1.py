# Wells
# Imports ----
import dash
from dash import dcc
from dash import html
#from dash import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash_table.Format import Format, Scheme, Trim

import pandas as pd
import plotly.graph_objects as go

#import pathlib

from my_pandas_extensions.plotting_plotly import *
#from my_pandas_extensions.database import collect_data

from app import app
import geopandas as gdp
import json

# Data ----
#wells_final_df, production_final_df = collect_data()
wells_final_df = pd.read_pickle("datasets/wells_final_Q42021_df.pkl")
production_final_df = pd.read_pickle("datasets/production_final_Q42021_df.pkl")

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

production_df = production_final_df.copy()
production_df['area_code'] = production_df['area'].map(areas_dict)

# Building App Layout ----
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
                                    html.H6("Producing Wells"),
                                    html.H3(id="prod_wells", children="", style={'fontWeight':'bold'})
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
                                    html.H6("Total Oil Prod. Rate, bpd"),
                                    html.H3(id="oil_prod", children="", style={'fontWeight':'bold'})
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
                                    html.H6("Total Cum. Oil Prod., MMbbl"),
                                    html.H3(id="oil_cum", children="", style={'fontWeight':'bold'})
                                ], className="p-1"
                            )
                        ],className="mt-2 mb-2 pb-2",
                    )
                ], style={"height": "100%"}, width={'size': 2, "offset": 0, 'order': 2}
            ),
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H6("Total Gas Prod. Rate, Mscf/d"),
                                    html.H3(id="gas_prod", children="", style={'fontWeight':'bold'})
                                ], className="p-1"
                            )
                        ], className="mt-2 mb-2 pb-2",
                    )
                ], style={"height": "100%"}, width={'size': 2, "offset": 0, 'order': 5}
            ),
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H6("Total Cum. Gas Prod., Bcf"),
                                    html.H3(id="gas_cum", children="", style={'fontWeight':'bold'})
                                ], className="p-1"
                            )
                        ],className="mt-2 mb-2 pb-2",
                    )
                ], style={"height": "100%"}, width={'size': 2, "offset": 0, 'order': 4}
            )
        ], className="h-10", justify='start'
    ),   
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Graph(
                        id = 'well_map', className='mh-10'
                    )
                ], width={'size':6, 'offset':0}, style={"height": "100%"}
            ),
            dbc.Col(
                [
                    dcc.Graph(
                            id = 'radio_plots', className='mh-10'
                    )
                ],width={'size':4, 'offset':0}, style={"height": "100%"}
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
                                        id = 'fluid_well_type',
                                        options=[
                                            {'label': 'Well Type', 'value': 'well_type'},
                                            {'label': 'Fluid Type', 'value': 'fluid_type'}],
                                        value='well_type',
                                        labelClassName="mt-0 ml-3",
                                        style = {'font-size': '13px'}
                                    ),
                                ], className="p-1"
                            )
                        ], className="mt-2 mb-1 pb-0"
                    ),
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.P(
                                        "Choose the Well Type:",
                                        className="card-text",
                                    ),
                                    dcc.Dropdown(id='drop_well_type',
                                            options=[
                                                {'label': 'Horizontal', 'value': 'Horizontal'},
                                                {'label': 'Vertical', 'value': 'Vertical'},
                                            ],
                                            value=['Horizontal','Vertical'],
                                            clearable = False,
                                            placeholder="Select a well type",
                                            multi=True,
                                            style = {'font-size': '13px', 'white-space': 'nowrap', 'text-overflow': 'ellipsis'}
                                    )    
                                ], className="p-1"
                            )
                        ], className="mt-5 mb-1 pb-0",
                        #color="dark",   # https://bootswatch.com/default/ for more card colors
                        #inverse=True,   # change color of text (black or white)
                        outline=True,  # True = remove the block colors from the background and header
                    ),
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.P(
                                    "Choose the Fluid Type:",
                                    className="card-text",
                                    ),
                                    dcc.Dropdown(id='drop_fluid_type',
                                            options=[
                                                {'label': 'Black Oil', 'value': 'Black_Oil'},
                                                {'label': 'Volatile Oil', 'value': 'Volatile_Oil'},
                                                {'label': 'Dry Gas', 'value': 'Dry_Gas'},
                                                {'label': 'Wet Gas', 'value': 'Wet_Gas'},
                                            ],
                                            value=['Black_Oil','Volatile_Oil','Dry_Gas','Wet_Gas'],
                                            clearable = False,
                                            placeholder="Select a fluid type",
                                            multi=True,
                                            style = {'font-size': '13px', 
                                                     #'white-space': 'nowrap', 
                                                     #'overflow':'scroll', 
                                                     'text-overflow': 'ellipsis'}
                                    )
                                ], className="p-1"
                            )
                        ], style={"height": "16vh"}, className="mt-5 mb-1 pb-0",
                        #color="dark",   # https://bootswatch.com/default/ for more card colors
                        #inverse=True,   # change color of text (black or white)
                        outline=True,  # True = remove the block colors from the background and header
                    ) 
                ], style={"height": "100%"}, width={'size': 2, "offset": 0, 'order': 4}
            ),
            dcc.Store(id='well_df'),
            dcc.Store(id='prod_df')
        ], className="h-40", align="center", justify='start'  # align Vertical: start, center, end
    ),                                                      # justify Horizontal:start,center,end,between,around
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Graph(
                        id = 'prod_fig',
                    )
                ], width={'size':6, 'offset':0}, style={"height": "100%"}
            ),
            dbc.Col(
                [
                    dcc.Graph(
                            id = 'table_plots', className='mh-10'
                    )
                ], width={'size':4, 'offset':0}, style={"height": "100%"}
            ),
            dcc.Store(id='map_well_df')
        ], className="h-50", align="start", justify='start'
    )
    ], style={"height": "100vh"}, fluid=True
 )

#----------------------------------------------
# Callbacks

# Callback to filter well_df dataframe
@app.callback(
    [Output('well_df', 'data'), 
    Output('prod_df', 'data')],
    [Input('drop_well_type', 'value'),
    Input('drop_fluid_type', 'value')]
)

def process_data(well_type_list, fluid_type_list):

    if (len(well_type_list) > 0) & (len(fluid_type_list) > 0):
        # well_df
        well_df=wells_df  \
            .query(f"well_name != 'BCeCg-111(h)'") \
            .query(f"well_name != 'BCeCf-101(h)'") \
            .query(f"well_name != 'BCeCf-105(h)'") \
            .query(f"well_name != 'BCeCg-112(h)'") \
            .query(f"well_name != 'BCeAe-113(h)'") \
            .query(f"well_name != 'BCeCf-108(h)'") \
            .query(f"well_name != 'BCeCf-106(h)'")

        well_df=well_df[well_df['well_type'].isin(well_type_list)]
        well_df=well_df[well_df['fluid_type'].isin(fluid_type_list)]
        well_df = well_df.rename(columns={'completion_date':'date'})

        #prod_df
        prod_df=production_df  \
            .query(f"well_name != 'BCeCg-111(h)'") \
            .query(f"well_name != 'BCeCf-101(h)'") \
            .query(f"well_name != 'BCeCf-105(h)'") \
            .query(f"well_name != 'BCeCg-112(h)'") \
            .query(f"well_name != 'BCeAe-113(h)'") \
            .query(f"well_name != 'BCeCf-108(h)'") \
            .query(f"well_name != 'BCeCf-106(h)'")

        prod_df=prod_df[prod_df['well_type'].isin(well_type_list)]
        prod_df=prod_df[prod_df['fluid_type'].isin(fluid_type_list)]

        prod_df = prod_df.rename(columns={'production_date':'date'})
    
    else:
        raise dash.exceptions.PreventUpdate 

    well_df_json = well_df.to_json()
    prod_df_json = prod_df.to_json()

    return well_df_json, prod_df_json

#----------------------------------------------
# Callback to update radio figure

@app.callback(
            Output('radio_plots', 'figure'),
             [Input('well_df', 'data'),
             Input('fluid_well_type', 'value')]
             )

def radio_figure_content(df_json, plot_type):
        df = pd.read_json(df_json, convert_axes=True, convert_dates=True)

        df = df.rename(columns={
                'date':'completion_date'
            })

        fig=df.column_date_agg('completion_date','well_name',plot_type,
                        x_label = 'Campaign',
                        y_label = 'Well Count',
                        title = f"Well Count per Year by {plot_type}")

        fig.update_layout(height=500, margin=dict(t=60, r=40, l=40, b=40), font=dict(size=10))
        return fig

#----------------------------------------------
# Callback to update table figure

@app.callback(Output('table_plots', 'figure'),
             [Input('well_df', 'data'),
             Input('fluid_well_type', 'value')]
             )

def table_figure_content(df_json, plot_type):
        df = pd.read_json(df_json)

        # Table 2
        table2_df = df \
                .pivot_table(values='well_name',
                                index=['well_type'], aggfunc=['count']) \
                .reset_index() 

        table2_df = table2_df.set_axis(
                ["_".join(col).rstrip("_") for col in table2_df.columns.tolist()],
                axis = 1) \
                .rename(columns={
                    'well_type':'Well Type',
                    'count_well_name':'Total Number of Wells'
                })

        # Table 3
        table3_df = df \
                .pivot_table(values='well_name',
                                index=['fluid_type'], aggfunc=['count']) \
                .reset_index() 

        table3_df = table3_df.set_axis(
                ["_".join(col).rstrip("_") for col in table3_df.columns.tolist()],
                axis = 1) \
                .rename(columns={
                    'fluid_type':'Fluid Type',
                    'count_well_name':'Total Number of Wells'
                }) \
                .sort_values(by='Total Number of Wells', ascending=False)

        if plot_type == 'well_type':
            fig = px.pie(
                data_frame=table2_df,
                values='Total Number of Wells',
                names='Well Type',
                color='Well Type',                            
                title='Number of Wells by Well Type'
                )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(showlegend=False)
            fig.update_layout(height=420, margin=dict(t=60, r=40, l=40, b=40), font=dict(size=10))

        else:
            fig = px.treemap(
                data_frame=table3_df, 
                path=['Fluid Type'], 
                values='Total Number of Wells',
                #color='Total Number of Wells'
                color_discrete_map={'Black_Oil':'blue', 
                    'Volatile_Oil':'green', 'Dry_Gas':'red', 
                    'Wet_Gas':'purple'},
                title='Number of Wells by Fluid Type'
            )
            fig.update_traces(root_color="white")
            fig.update_traces(textinfo='label+percent entry')
            fig.update_layout(coloraxis_showscale=False)
            fig.update_layout(height=420, margin=dict(t=60, r=40, l=40, b=40), font=dict(size=10))
        
        return fig

#----------------------------------------------
# Callback to update producing wells figure

@app.callback(
            Output('prod_fig', 'figure'),
             [Input('prod_df', 'data')]
             )

def prod_figure_content(df_json):
    df = pd.read_json(df_json, convert_axes=True, convert_dates=True)

    df = df.rename(columns={
            'date':'production_date'
        })   

    fig=df \
        .query(f"production_status == 'Producing'") \
        .column_date_agg_no_group('production_date','production_status',
            rule = 'M', agg_func = pd.Series.count,
            title = 'Number of Producing Wells in Vaca Muerta per Year',
            y_label = 'Number of Wells', show_scale = False)

    fig.update_layout(height=415, margin=dict(t=60, r=20, l=20, b=0), font=dict(size=10)) 

    return fig 

#----------------------------------------------
# Callback to update cards

@app.callback(
    Output('prod_wells','children'),
    Output('oil_cum', 'children'),
    Output('oil_prod', 'children'),
    Output('gas_cum', 'children'),
    Output('gas_prod', 'children'),
    [Input('prod_df', 'data')]
    )

def wells_prod(df_json):

    df = pd.read_json(df_json, convert_axes=True, convert_dates=True)

    df = df.rename(columns={'date':'production_date'})

    table1_df = df[["well_name", 'production_date',  'cum_oil_bbl', 'cum_gas_mscf',
                            'oil_month_bpd', 'gas_month_mscf_d', 'production_status']] \
            .assign(max_prod_date = lambda x: x.production_date.max()) \
            .query(f"production_date == max_prod_date") \
            .query(f"production_status == 'Producing'") \
            .agg({'well_name' : ['count'],
                'cum_oil_bbl' : ['sum'],
                'oil_month_bpd' : ['sum'],
                'cum_gas_mscf' : ['sum'],
                'gas_month_mscf_d' : ['sum']}) \
            .reset_index(drop=True) \
            .fillna(0) \
            .agg({'well_name' : ['sum'],
                'cum_oil_bbl' : ['sum'],
                'oil_month_bpd' : ['sum'],
                'cum_gas_mscf' : ['sum'],
                'gas_month_mscf_d' : ['sum']
                }) \
            .reset_index(drop=True) \
            .rename({'well_name':'Producing Wells',
                    'cum_oil_bbl': 'Total Cum. Oil Prod., bbl',
                    'oil_month_bpd': 'Total Oil Prod. Rate, bbl/day',
                    'cum_gas_mscf': 'Total Cum. Gas Prod., Mscf',
                    'gas_month_mscf_d': 'Total Gas Prod. Rate, Mscf/day'
                    }, axis=1)

    table1_df['Producing Wells']=table1_df['Producing Wells'].map("{:,.0f}".format)
    table1_df['Total Cum. Oil Prod., MMbbl']=(table1_df['Total Cum. Oil Prod., bbl']/1000000).map("{:,.2f}".format)
    table1_df['Total Oil Prod. Rate, bbl/day']=table1_df['Total Oil Prod. Rate, bbl/day'].map("{:,.0f}".format)
    table1_df['Total Cum. Gas Prod., Bcf']=(table1_df['Total Cum. Gas Prod., Mscf']/1000000).map("{:,.2f}".format)
    table1_df['Total Gas Prod. Rate, Mscf/day']=table1_df['Total Gas Prod. Rate, Mscf/day'].map("{:,.0f}".format)

    prod_wells = table1_df['Producing Wells']
    oil_cum = table1_df['Total Cum. Oil Prod., MMbbl']
    oil_prod = table1_df['Total Oil Prod. Rate, bbl/day']
    gas_cum = table1_df['Total Cum. Gas Prod., Bcf']
    gas_prod = table1_df['Total Gas Prod. Rate, Mscf/day']

    return prod_wells, oil_cum, oil_prod, gas_cum, gas_prod

#----------------------------------------------
# Callback to update map
@app.callback(
            Output('well_map', 'figure'),
             [Input('well_df', 'data'),
              Input('prod_df', 'data'),
              Input('fluid_well_type','value')]
             )

def map_figure_update(df_well_json, df_prod_json, well_fluid_sel):
    df_well = pd.read_json(df_well_json, convert_axes=True, convert_dates=True)
    df_prod = pd.read_json(df_prod_json, convert_axes=True, convert_dates=True)

    df_well = df_well.rename(columns={'date':'completion_date'})
    df_prod = df_prod.rename(columns={'date':'production_date'})
    
    oil_prod_df = df_prod.assign(max_prod_date = lambda x: x.production_date.max()) \
                        .query(f"production_date == max_prod_date") \
                        .query(f"production_status == 'Producing'") \
                        .groupby(['area','area_code', 'operator'])["well_name"].count().reset_index(name="well_count")
    
    #.groupby(['area','area_code', 'operator'])["oil_month_bpd"].sum().reset_index(name="oil_prod")
    
    if well_fluid_sel == 'well_type':
        colorsIdx = {'Vertical': 'red', 'Horizontal': 'blue'}
        cols      = df_well['well_type'].map(colorsIdx)
    else:
        colorsIdx = {'Black_Oil': 'blue', 'Volatile_Oil': 'green', 'Dry_Gas': 'red', 'Wet_Gas': 'purple'}
        cols      = df_well['fluid_type'].map(colorsIdx)
    
    fig = go.Figure(go.Choroplethmapbox(geojson=json_dict, 
                                        locations=oil_prod_df.area_code, 
                                        z=oil_prod_df.well_count,
                                        colorscale = 'Greens',
                                        zmin = 0,
                                        zmid = 30,
                                        zmax = 300,
                                        featureidkey="properties.CODIGODESE",
                                        text=oil_prod_df.area,
                                        hovertemplate=
                                                    "<b>%{text}</b><br><br>" +
                                                    "Well Count: %{z:,.0f}<br>" +
                                                    "<extra></extra>",
                                        marker_opacity=0.5, marker_line_width=1))
    
    fig.add_scattermapbox(lat = df_well['latitude'],
                        lon = df_well['longitude'],
                        mode = 'markers',    
                        below='',
                        text = df_well['well_type'] + "<br>" + df_well['fluid_type'],               
                        customdata=df_well['well_name'],
                        hovertemplate = "%{customdata}</b><br><br>" +
                                        "%{text}<br>" +
                                        "<extra></extra>",
                        marker = dict(
                                color = cols,
                                size = 6,
                                opacity = 0.5,
                                symbol = 'circle'))
    
    fig.update_layout(hovermode='closest',
                      mapbox_style="carto-positron",
                      mapbox_zoom=8, 
                      mapbox_center = {"lat": -38.0986, "lon": -68.746998})
    fig.update_layout(height=500, margin={"r":0,"t":0,"l":60,"b":0})
         
    return fig

