# Production
# Imports ----
import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash_table.Format import Format, Scheme, Trim

import pandas as pd
from mizani.formatters import date_format, comma_format
number_comma_format = comma_format(digits=0)
number_date_format = date_format("%Y-%m-%d")
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

# Building App ----

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [ 
                        dcc.Graph(
                            id = 'graph_tab1b_avg_prod', figure = {},
                            className='mh-10'
                        ),  
                    ], width={'size':5, 'offset':0}, style={"height": "100%"}
                ),
                dbc.Col(
                    [
                        dcc.Graph(
                            id = 'graph_tab1b_cum_prod', figure = {},
                            className='mh-10'
                        ),  
                    ], width={'size':5, 'offset':0}, style={"height": "100%"}
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
                                            id = 'ri_tab1b_prod_fluid',
                                            options=[
                                                {'label': 'Oil', 'value': 'Oil'},
                                                {'label': 'Gas', 'value': 'Gas'}],
                                            value='Oil',
                                            labelClassName="mt-0 ml-3",
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
                                            id = 'ri_tab1b_well_fluid_type',
                                            options=[
                                                {'label': 'Well Type', 'value': 'well_type'},
                                                {'label': 'Fluid Type', 'value': 'fluid_type'},
                                                {'label': 'Area', 'value': 'area'},
                                                {'label': 'Campaign', 'value': 'campaign'}],
                                            value='well_type',
                                            labelClassName="mt-0 ml-3",
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
                                        "Choose agreggation variable:",
                                        className="card-text",
                                        ),
                                        dcc.Dropdown(id='dd_tab1b_aggregation',
                                                #options=groups_all,
                                                value=['All'],
                                                #clearable = False,
                                                placeholder="Select variables (leave blank to include all)",
                                                multi=True,
                                                style = {'font-size': '13px','text-overflow': 'ellipsis'}
                                        )
                                    ], className="p-2"
                                )
                            ], className="mt-2 mb-2 pb-2", outline=True,
                        ),
                    ], width={'size':2, 'offset':0}, style={"height": "100%"}
                ),
            ], className="h-80", align="center", justify='start'
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        
                    ], width={'size':1, 'offset':0}, style={"height": "100%"}
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.P(
                                                "Plot Type:",
                                                className="card-text",
                                            ),
                                        dcc.RadioItems(
                                            id = 'ri_tab2_plot',
                                            options=[
                                                {'label': 'Line', 'value': 'line'},
                                                {'label': 'Area', 'value': 'area'},
                                                {'label': 'Bar', 'value': 'bar'}],
                                            value='area',
                                            labelClassName="mt-0 ml-3",
                                            style = {'font-size': '13px'}
                                        ),
                                    ], className="p-1"
                                )
                            ], className="mb-2 pb-2"
                        ),
                    ], width={'size':1, 'offset':0}, style={"height": "100%"}
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.P(
                                                "Production Variable:",
                                                className="card-text",
                                            ),
                                        dcc.RadioItems(
                                            id = 'ri_tab2_rate_volume',
                                            options=[
                                                {'label': 'Rate', 'value': 'Rate'},
                                                {'label': 'Volume', 'value': 'Volume'}],
                                            value='Rate',
                                            labelClassName="mt-0 ml-3",
                                            style = {'font-size': '13px'}
                                        ),
                                    ], className="p-1"
                                ),
                                dbc.CardBody(
                                    [
                                        dcc.RadioItems(
                                            id = 'ri_tab2_avg_total',
                                            options=[
                                                {'label': 'Average', 'value': 'Average'},
                                                {'label': 'Total', 'value': 'Total'}],
                                            value='Average',
                                            labelClassName="mt-0 ml-3",
                                            style = {'font-size': '13px'}
                                        ),
                                    ], className="p-1"
                                )
                            ], className="mb-2 pb-2"
                        ),
                    ], width={'size':2, 'offset':0}, style={"height": "100%"}
                )
            ], className="h-20", align="center", justify='start'
        )
    ], style={"height": "100vh"}, fluid=True
)

##------------------------------------------------------------------------
# # Callback to configure the dropdown ----
@app.callback(
    [Output('dd_tab1b_aggregation', 'options'),
    Output('dd_tab1b_aggregation', 'value')],
    [Input('ri_tab1b_well_fluid_type', 'value')])

def dd_options(ri_well_fluid_type):
    
    agg_groups = production_final_df[ri_well_fluid_type].unique()
    agg_groups_all_2 = [{'label' : k, 'value' : k} for k in sorted(agg_groups)]
    agg_groups_all_1 = [{'label' : '(Select All)', 'value' : 'All'}]
    agg_groups_all = agg_groups_all_1 + agg_groups_all_2
    
    agg_groups_all_value = ["All"]

    return agg_groups_all, agg_groups_all_value

##--------------------------------------------------------------------
# Callback to generate average production plot ----
@app.callback(
    Output('graph_tab1b_avg_prod', 'figure'),
    [Input('ri_tab1b_prod_fluid', 'value'),
    Input('ri_tab1b_well_fluid_type', 'value'),
    Input('dd_tab1b_aggregation', 'value'),
    Input('ri_tab2_rate_volume', 'value'),
    Input('ri_tab2_avg_total', 'value'),
    Input('ri_tab2_plot', 'value')])

def graph_production_rate(ri_prod_fluid, ri_well_fluid_type, dd_aggregation, ri_rate_vol, ri_avg_total, ri_plot):
    
    if ri_prod_fluid == "Oil":
        if ri_rate_vol == "Rate":
            prod_var = 'oil_month_bpd'
        else:
            prod_var = 'oil_month_bbl'
    else:
        if ri_rate_vol == "Rate":
            prod_var = 'gas_month_mscf_d'
        else:
            prod_var = 'gas_month_mscf'
            
    if ri_avg_total == "Average":
        agg_fun = np.mean
    else:
        agg_fun = np.sum
    
    for i in dd_aggregation:
        if i == 'All':
            isselect_all = 'Y'
            break
        elif i == '':
            isselect_all = 'Y'
            break
        elif i != '':
            isselect_all = 'N'
        
    # Filter df according to selection
    if isselect_all == 'N':
        prod_df = production_final_df[production_final_df[ri_well_fluid_type].isin(dd_aggregation)]
    else:
        prod_df = production_final_df.copy()
        
    if ri_plot == "line":
        fig = prod_df \
            .query(f"production_status == 'Producing'") \
            .query(f"production_date >= '2012-02-01'") \
            .line_plot_agg('production_date', prod_var, ri_well_fluid_type, 
                agg_func = agg_fun, log_plot = False, rule = 'M',
                title=f"{ri_avg_total} {ri_prod_fluid} Well Production {ri_rate_vol} vs. Date by {ri_well_fluid_type}")
    
    elif ri_plot == "area":
        fig = prod_df \
            .query(f"production_status == 'Producing'") \
            .query(f"production_date >= '2012-02-01'") \
            .area_plot_agg('production_date', prod_var, ri_well_fluid_type, 
                    agg_func = agg_fun,
                    title=f"{ri_avg_total} {ri_prod_fluid} Well Production {ri_rate_vol} vs. Date by {ri_well_fluid_type}")
            
    else:
        fig = prod_df \
                .query(f"production_status == 'Producing'") \
                .query(f"production_date >= '2012-02-01'") \
                .column_date_agg('production_date', prod_var, ri_well_fluid_type,
                        agg_func = agg_fun,
                        title=f"{ri_avg_total} {ri_prod_fluid} Well Production {ri_rate_vol} vs. Date by {ri_well_fluid_type}")
        
    # if ri_well_fluid_type == "area":
    #     raise dash.exceptions.PreventUpdate
    # else:
        
    fig.update_layout(height=700, font=dict(size=10))
    #fig.update_layout(margin=dict(t=40, r=40, l=40, b=40))
    return fig

##--------------------------------------------------------------------
# Callback to generate cumulative production plot ----
@app.callback(
    Output('graph_tab1b_cum_prod', 'figure'),
    [Input('ri_tab1b_prod_fluid', 'value'),
     Input('ri_tab1b_well_fluid_type', 'value'),
     Input('dd_tab1b_aggregation', 'value')])

def graph_production_rate(ri_prod_fluid_value, ri_well_fluid_type, dd_aggregation):
    
    for i in dd_aggregation:
        if i == 'All':
            isselect_all = 'Y'
            break
        elif i == '':
            isselect_all = 'Y'
            break
        elif i != '':
            isselect_all = 'N'
        
    # Filter df according to selection
    if isselect_all == 'N':
        prod_df = production_final_df[production_final_df[ri_well_fluid_type].isin(dd_aggregation)]
    else:
        prod_df = production_final_df.copy()
    
    if ri_prod_fluid_value == "Oil":        
        fig = prod_df \
                .query(f"production_status == 'Producing'") \
                .query(f"production_date >= '2012-02-01'") \
                .scatter_line_agg('cum_eff_prod_day', 'cum_oil_bbl', 'well_name', ri_well_fluid_type,
                title = f'Cumulative Oil Production per Well by {ri_well_fluid_type}')
    else:
            fig = prod_df \
                .query(f"production_status == 'Producing'") \
                .query(f"production_date >= '2012-02-01'") \
                .scatter_line_agg('cum_eff_prod_day', 'cum_gas_mscf', 'well_name', ri_well_fluid_type,
                title = f'Cumulative Gas Production per Well by {ri_well_fluid_type}')

    fig.update_layout(height=700, font=dict(size=10))
    #fig.update_layout(margin=dict(t=40, r=40, l=40, b=40))
    return fig







