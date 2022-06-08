# Production Indicators
# Imports ----
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
#from dash_table.Format import Format, Scheme, Trim

import pandas as pd
import json

from my_pandas_extensions.plotting_plotly import *
#from my_pandas_extensions.database import collect_data

from app import app

# Data ----
#wells_final_df, production_final_df = collect_data()
wells_final_df = pd.read_pickle("datasets/wells_final_Q42021_df.pkl")
production_final_df = pd.read_pickle("datasets/production_final_Q42021_df.pkl")

wells_final_df = wells_final_df \
    .query(f"well_type == 'Horizontal'") \
    .assign(proppant_intensity_lbm_ft = lambda x: x.proppant_volume_lbm / (x.horizontal_length*3.28084)) \
    .assign(fluid_intensity_bbl_ft = lambda x: x.fluid_volume_m3*6.28981 / (x.horizontal_length*3.28084)) \
    .assign(proppant_fluid_ratio_lbm_gal = lambda x: x.proppant_volume_lbm / (x.fluid_volume_m3*264.172)) \
    .assign(fluid_volume_bbl = lambda x: x.fluid_volume_m3*6.28981) \
    .query(f"proppant_volume_lbm > 0") \
    .query(f"fluid_volume_m3 > 0") \
    .query(f"horizontal_length > 0")
    
#app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])   

x_features = ['number_of_stages', 'horizontal_length','stage_spacing',
                # 'max_qo_bpd', 'cum180_oil_bbl', 'cum360_oil_bbl',
                'proppant_volume_lbm', 'fluid_volume_m3',
                'proppant_intensity_lbm_ft', 'fluid_intensity_bbl_ft'
                ]

y_features_oil = [
                #'number_of_stages', 'proppant_volume_lbm', 'fluid_volume_bbl',
                'max_qo_bpd', 'cum180_oil_bbl',
                #'max_qg_mscfd', 'cum180_gas_mscf',
                #'cum360_oil_bbl',
                'eur_total_mboeq',
                ]

y_features_gas = [
                #'number_of_stages', 'proppant_volume_lbm', 'fluid_volume_bbl',
                #'max_qo_bpd', 'cum180_oil_bbl',
                'max_qg_mscfd', 'cum180_gas_mscf',
                #'cum360_oil_bbl',
                'eur_total_mboeq',
                ]

group_features = ['campaign', 'operator', 'area', 'fluid_type',
                    # 'number_of_stages', 'horizontal_length',
                    # 'stage_spacing', 'proppant_intensity_lbm_ft', 
                    # 'fluid_intensity_bbl_ft',
                ]

# Building App ----
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
                                        html.P(
                                                "Choose produced fluid:",
                                                className="card-text",
                                            ),
                                        dcc.RadioItems(
                                            id = 'ri_tab3_prod_fluid',
                                            options=[
                                                {'label': 'Oil', 'value': 'Oil'},
                                                {'label': 'Gas', 'value': 'Gas'}],
                                            value='Oil',
                                            labelClassName="mt-0 ml-2",
                                            style = {'font-size': '13px'}
                                        ),
                                    ], className="p-2"
                                )
                            ], className="mt-2 mb-1 ml-4 pb-1"
                        ),
                    ], style={"height": "100%"}, width={'size': 2, "offset": 0}
                ),
                dbc.Col(
                    [
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
                                            #value=['Black_Oil','Volatile_Oil'],
                                            multi=True,
                                            style = {'font-size': '13px', 'white-space': 'nowrap', 'text-overflow': 'ellipsis'}
                                        ) 
                                    ], className="p-1"
                                )
                            ], className="mt-2 mb-2"
                        )       
                    ], style={"height": "100%"}, width={'size': 4, "offset": 1,}
                ),
                #dbc.Col(
                #    [
                #        
                #    ], style={"height": "100%"}, width={'size': 3, "offset": 3,}
                #),
            ], className="h-10", justify='start'
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.P(
                                            "Choose Scatter Plot X-variable:",
                                            className="card-text",
                                        ),
                                        dcc.Dropdown(
                                            id='xaxis',
                                            options=[{'label':i.title(), 'value':i} for i in x_features],
                                            value='number_of_stages',
                                            style = {'font-size': '13px', 'white-space': 'nowrap', 'text-overflow': 'ellipsis'}
                                        )
                                    ], className="p-1"
                                )   
                            ], className="mt-4 mb-2"
                        ),
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.P(
                                            "Choose Scatter Plot Y-variable:",
                                            className="card-text",
                                        ),
                                        dcc.Dropdown(
                                            id='yaxis',
                                            #options=[],
                                            #value='cum180_oil_bbl',
                                            clearable = False,
                                            multi=False,
                                            style = {'font-size': '13px', 'white-space': 'nowrap', 'text-overflow': 'ellipsis'}
                                        )
                                    ], className="p-1"
                                )
                            ], className="mt-5 mb-5"
                        ),
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.P(
                                            "Choose Scatter Plot Group-variable:",
                                            className="card-text",
                                        ),
                                        dcc.Dropdown(
                                            id='group',
                                            options=[{'label':i.title(), 'value':i} for i in group_features],
                                            value='campaign',
                                            style = {'font-size': '13px', 'white-space': 'nowrap', 'text-overflow': 'ellipsis'}
                                        )
                                    ], className="p-1"
                                )
                            ], className="mt-5 mb-0"
                        )
                    ], style={"height": "100%"}, width={'size': 2, "offset": 0,}
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'scatter_no_agg')
                    ], style={"height": "100%"}, width={'size': 5, "offset": 0}
                ),
                # dbc.Col(
                #     [
                        
                #     ], style={"height": "100%"}, width={'size': 2, "offset": 0,}
                # ),     
                dbc.Col(
                    [
                        dcc.Graph(id = 'line-rate'),
                        dcc.Graph(id = 'line-cum')
                    ], style={"height": "100%"}, width={'size': 4, "offset": 0}
                ),
                dcc.Store(id='tab2_well_df')
            ], className="h-80", align="start", justify='around'
        ),
], style={"height": "100vh"}, fluid=True)

#----------------------------------------------
# Callback to configure the dropdown
@app.callback( 
    [Output('yaxis', 'options'),
     Output('yaxis', 'value')],
    [Input('ri_tab3_prod_fluid','value')]
)

def drop_yaxis_options(ri_fluid):
    
    if ri_fluid == 'Oil':
        y_options=[{'label':i.title(), 'value':i} for i in y_features_oil]
        y_value='cum180_oil_bbl'
    
    if ri_fluid == 'Gas':
        y_options=[{'label':i.title(), 'value':i} for i in y_features_gas]
        y_value='cum180_gas_mscf'
    
    return y_options, y_value

# Callback to configure the dropdown
@app.callback( 
    Output('drop_fluid_type', 'value'),
    [Input('ri_tab3_prod_fluid','value')]
)

def drop_fluid_type_options(ri_fluid):
    
    if ri_fluid == 'Oil':
        fluid_type_value=['Black_Oil','Volatile_Oil']
    
    if ri_fluid == 'Gas':
        fluid_type_value=['Dry_Gas','Wet_Gas']
    
    return fluid_type_value

# Callback to filter well_df dataframe

@app.callback(
    Output('tab2_well_df', 'data'),
    [Input('drop_fluid_type', 'value')])

def process_data(fluid_type_list):

    if len(fluid_type_list) > 0:
        # well_df
        well_tab2_df=wells_final_df  \
            .query(f"well_name != 'BCeCg-111(h)'") \
            .query(f"well_name != 'BCeCf-101(h)'") \
            .query(f"well_name != 'BCeCf-105(h)'") \
            .query(f"well_name != 'BCeCg-112(h)'") \
            .query(f"well_name != 'BCeAe-113(h)'") \
            .query(f"well_name != 'BCeCf-108(h)'") \
            .query(f"well_name != 'BCeCf-106(h)'")

        well_tab2_df=well_tab2_df[well_tab2_df['fluid_type'].isin(fluid_type_list)]
        well_tab2_df = well_tab2_df.rename(columns={'completion_date':'date'})
    
    else:
        raise dash.exceptions.PreventUpdate 

    well_tab2_df_json = well_tab2_df.to_json()

    return well_tab2_df_json

# Callback to generate scatter plot ----
@app.callback(
    Output('scatter_no_agg', 'figure'),
    [Input('xaxis','value'),
    Input('yaxis','value'),
    Input('group','value'),
    Input('tab2_well_df', 'data'),
    ])

def update_graph(xaxis_name, yaxis_name, group_name, df_tab2_json):

    df = pd.read_json(df_tab2_json, convert_axes=True, convert_dates=True)
    df = df.rename(columns={'date':'completion_date'})
        
    figure=df.scatter_no_agg(xaxis_name, yaxis_name, group_name, 'well_name',
                             title=f'{yaxis_name} vs. {xaxis_name} by {group_name}')

    figure.update_layout(height=580)
    figure.update_layout(margin=dict(t=40, r=40, l=40, b=0), font=dict(size=10))

    return figure

# Callback to generate rate plot ----
@app.callback(
    Output('line-rate', 'figure'),
    [Input('scatter_no_agg', 'clickData'),
     Input('ri_tab3_prod_fluid','value')])

def callback_image(clickData, ri_fluid):
    if clickData is None:
        if ri_fluid == 'Oil': 
            well_list = ['AF-5(h)']
        if ri_fluid == 'Gas':
            well_list = ['FP-1243(h)']
    else:
        well_list=clickData['points'][0]['customdata']
    
    df = production_final_df[production_final_df['well_name'].isin(well_list)]
    
    if ri_fluid == 'Oil':
        fig = df \
            .line_well_prod_plot_no_agg('cum_eff_prod_day', 'oil_month_bpd', 'well_name',
            plot_type = 'rate', normalized = False,
            title='Oil Production Rate vs. Time')
            
    if ri_fluid == 'Gas':
        fig = df \
            .line_well_prod_plot_no_agg('cum_eff_prod_day', 'gas_month_mscf_d', 'well_name',
            plot_type = 'rate', normalized = False,
            title='Gas Production Rate vs. Time')
    
    fig.update_layout(height=300)
    fig.update_layout(margin=dict(t=40, r=40, l=40, b=40), font=dict(size=10))
    return fig

# Callback to generate cum plot ----
@app.callback(
    Output('line-cum', 'figure'),
    [Input('scatter_no_agg', 'clickData'),
     Input('ri_tab3_prod_fluid','value')])

def callback_image(clickData, ri_fluid):
    if clickData is None:
        if ri_fluid == 'Oil': 
            well_list = ['AF-5(h)']
        if ri_fluid == 'Gas':
            well_list = ['FP-1243(h)']
    else:
        well_list=clickData['points'][0]['customdata']
    
    df = production_final_df[production_final_df['well_name'].isin(well_list)]
    
    if ri_fluid == 'Oil':
        fig = df \
            .line_well_prod_plot_no_agg('cum_eff_prod_day', 'cum_oil_bbl', 'well_name',
            plot_type = 'volume', normalized = False,
            title='Oil Production Volume vs. Time')
            
    if ri_fluid == 'Gas':
        fig = df \
            .line_well_prod_plot_no_agg('cum_eff_prod_day', 'cum_gas_mscf', 'well_name',
            plot_type = 'volume', normalized = False,
            title='Gas Production Volume vs. Time')
    
    fig.update_layout(height=300)
    fig.update_layout(margin=dict(t=40, r=40, l=40, b=40), font=dict(size=10))
    return fig
    
# if __name__ == '__main__':
#     app.run_server(use_reloader=False)