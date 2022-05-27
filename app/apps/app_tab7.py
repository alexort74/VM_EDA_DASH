# Completion
# Imports ----
import dash
from dash import dcc
from dash import html
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash_table.Format import Format, Scheme, Trim

import pandas as pd
import geopandas as gdp
import json

from my_pandas_extensions.plotting_plotly import *
#from my_pandas_extensions.database import collect_data

from app import app

# Data ----
#wells_final_df, production_final_df = collect_data()
wells_final_df = pd.read_pickle("datasets/wells_final_Q42021_df.pkl")
production_final_df = pd.read_pickle("datasets/production_final_Q42021_df.pkl")
    
wells_df_oil = wells_final_df \
    .query(f"produced_fluid == 'Oil'") \
    .query(f"well_type == 'Horizontal'") \
    .query(f"horizontal_length > 0") \
    .query(f"proppant_volume_lbm > 0") \
    .query(f"fluid_volume_m3 > 0") \
    .query(f"max_qo_bpd == max_qo_bpd") \
    .query(f"cum180_oil_bbl == cum180_oil_bbl") \
    .query(f"eur_total_mboeq == eur_total_mboeq") \
    .assign(fluid_volume_bbl = lambda x: x.fluid_volume_m3*6.28981) \
    .assign(proppant_intensity_lbm_ft = lambda x: x.proppant_volume_lbm / (x.horizontal_length*3.28084)) \
    .assign(fluid_intensity_bbl_ft = lambda x: x.fluid_volume_m3*6.28981 / (x.horizontal_length*3.28084)) \
    .assign(proppant_fluid_ratio_lbm_gal = lambda x: x.proppant_volume_lbm / (x.fluid_volume_m3*264.172))
    
wells_df_gas = wells_final_df \
    .query(f"produced_fluid == 'Gas'") \
    .query(f"well_type == 'Horizontal'") \
    .query(f"horizontal_length > 0") \
    .query(f"proppant_volume_lbm > 0") \
    .query(f"fluid_volume_m3 > 0") \
    .query(f"max_qg_mscfd == max_qg_mscfd") \
    .query(f"cum180_gas_mscf == cum180_gas_mscf") \
    .query(f"eur_total_mboeq == eur_total_mboeq") \
    .assign(fluid_volume_bbl = lambda x: x.fluid_volume_m3*6.28981) \
    .assign(proppant_intensity_lbm_ft = lambda x: x.proppant_volume_lbm / (x.horizontal_length*3.28084)) \
    .assign(fluid_intensity_bbl_ft = lambda x: x.fluid_volume_m3*6.28981 / (x.horizontal_length*3.28084)) \
    .assign(proppant_fluid_ratio_lbm_gal = lambda x: x.proppant_volume_lbm / (x.fluid_volume_m3*264.172))

#wells_df['campaign'] = wells_df['campaign'].astype("category")
#wells_df = wells_df.astype({'campaign': 'int32'}).dtypes

mark_values = {2011:'2011',2012:'2012',2013:'2013',2014:'2014',
               2015:'2015',2016:'2016',2017:'2017',2018:'2018',
               2019:'2019',2020:'2020',2021:'2021'}
     
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
                                        html.P(
                                                "Choose filter variable (marker color):",
                                                className="card-text",
                                                style = {'font-size': '16px'}
                                            ),
                                        dcc.RadioItems(
                                            id = 'ri_tab7_filter_var',
                                            options=[
                                                {'label': 'Fluid Intensity', 'value': 'fluid_intensity_bbl_ft'},
                                                {'label': 'Proppant Intensity', 'value': 'proppant_intensity_lbm_ft'},
                                                {'label': 'Stage Spacing', 'value': 'stage_spacing'}],
                                            value='proppant_intensity_lbm_ft',
                                            labelClassName="mt-0 ml-5",
                                            style = {'font-size': '13px'}
                                        ),
                                    ], className="p-1"
                                ),
                                dbc.CardBody(
                                    [
                                        html.P(
                                                "Choose production indicator (marker size):",
                                                className="card-text ",
                                                style = {'font-size': '16px'}
                                            ),
                                        dcc.RadioItems(
                                            id = 'ri_tab7_filter_ind',
                                            #options=[
                                            #    {'label': 'Max. Production', 'value': 'max_qo_bpd'},
                                            #    {'label': '180-day Cum. Oil Prod.', 'value': 'cum180_oil_bbl'},
                                            #    {'label': 'EUR', 'value': 'eur_total_mboeq'}],
                                            #value='cum180_oil_bbl',
                                            labelClassName="mt-0 ml-5",
                                            style = {'font-size': '13px'}
                                        ),
                                    ], className="mt-2 p-1"
                                )
                            ], className="mt-2 mb-2 pb-2"
                        ),
                    
                    ], width={'size':6, 'offset':0}, style={"height": "100%"}
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
                                            id = 'ri_tab7_prod_fluid',
                                            options=[
                                                {'label': 'Oil', 'value': 'Oil'},
                                                {'label': 'Gas', 'value': 'Gas'}],
                                            value='Oil',
                                            labelClassName="mt-0 ml-5",
                                            style = {'font-size': '13px'}
                                        ),
                                    ], className="p-1"
                                ),
                                dbc.CardBody(
                                    [
                                        html.P(
                                                "Select chart:",
                                                className="card-text",
                                                style = {'font-size': '16px'}
                                            ),
                                        dcc.Dropdown(id='dd_tab7_graphs',
                                                #options = [],
                                                #value=[],
                                                clearable = False,
                                                placeholder="Select chart",
                                                multi=False,
                                                style = {'font-size': '13px','text-overflow': 'ellipsis'}
                                        ),
                                    ], className="p-1"
                                ),
                            ], className="mt-2 mb-1 ml-5 pb-2"
                        ),
                    ], width={'size':4, 'offset':0}, style={"height": "100%"}
                ),
        ]),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(
                            id = 'graph_tab7_map', config={'displayModeBar': False, 'scrollZoom': True}, 
                            className='mh-100 mt-4'
                        ),
                    
                    ], width={'size':6, 'offset':0}, style={"height": "100%"}
                ),
                dbc.Col(
                    [
                        dcc.Graph(
                            id = 'graph_tab7_completion', className='mh-100 mt-3'
                        ),
                    
                    ], width={'size':6, 'offset':0}, style={"height": "100%"}
                ),
            ], className="h-80", align="start", justify='start'
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
                                                "Drag the slider to change the campaign:",
                                                className="card-text",
                                                style = {'font-size': '16px'}
                                            ),
                                        dcc.RangeSlider(id='slider_tab7_campaign',
                                            min=2011,
                                            max=2021,
                                            value=[2015,2021],
                                            marks=mark_values,
                                            step=None
                                        )
                                    ], className="p-1"
                                )
                            ], className="mt-2 mb-2 pb-2"
                        )
                        
                    ], width={'size':6, 'offset':0}, style={"height": "100%"}
                ),
                dbc.Col(
                    [
                    
                    ], width={'size':4, 'offset':0}, style={"height": "100%"}
                ),
            ], className="h-80", align="start", justify='start'
        )
    ], style={"height": "100vh"}, fluid=True
)

# Callbacks-------------------------------------------------------------------------------------
# Callback to configure the dropdown
@app.callback( 
    [Output('ri_tab7_filter_ind', 'options'),
     Output('ri_tab7_filter_ind', 'value')],
    [Input('ri_tab7_prod_fluid','value')]
)

def drop_yaxis_options(ri_fluid):
    
    if ri_fluid == 'Oil':
        y_options = [
            {"label": "Initial Oil Rate, bbl/d",
             "value": "max_qo_bpd"},
            {"label": "180-day Cum. Oil Prod., bbl",
             "value": "cum180_oil_bbl"},
            {"label": "Total EUR, Mboeq",
             "value": "eur_total_mboeq"}
            ]
        y_value='cum180_oil_bbl'
    
    if ri_fluid == 'Gas':
        y_options = [
            {"label": "Initial Gas Rate, Mscf/d",
             "value": "max_qg_mscfd"},
            {"label": "180-day Cum. Gas Prod., Mscf",
             "value": "cum180_gas_mscf"},
            {"label": "Total EUR, Mboeq",
             "value": "eur_total_mboeq"}
            ]
        y_value='cum180_gas_mscf'
    
    return y_options, y_value

# Callback to configure the dropdown ----
@app.callback(
    [Output('dd_tab7_graphs', 'options'),
    Output('dd_tab7_graphs', 'value')],
    [Input('ri_tab7_filter_var', 'value')])

def dd_options(ri_filter_var):
    
    if ri_filter_var == 'fluid_intensity_bbl_ft':
        dd_options = [
            {"label": "Histogram of Fluid Intensity per well",
             "value": "hist_fluid_intensity"},
            {"label": "Boxplot of Fluid Intensity by Campaign",
             "value": "boxplot_fluid_intensity"},
            {"label": "Fluid volume vs. Horizontal Length, by Fluid Intensity",
             "value": "scatter_fluid_volume_hor_length_fluid_int"},
            {"label": "Production Indicator vs. Fluid Intensity binned",
             "value": "boxplot_prod_ind_fluid_int"}
            ]
        dd_value = 'hist_fluid_intensity'

    elif ri_filter_var == 'proppant_intensity_lbm_ft':
        dd_options = [
            {"label": "Histogram of Proppant Intensity per well",
             "value": "hist_proppant_intensity"},
            {"label": "Boxplot of Proppant Intensity by Campaign",
             "value": "boxplot_proppant_intensity"},
            {"label": "Proppant Volume vs. Horizontal Length, by Proppant Intensity",
             "value": "scatter_proppant_volume_hor_length_proppant_int"},
            {"label": "Production Indicator vs. Proppant Intensity binned",
             "value": "boxplot_prod_ind_proppant_int"}
            ]
        dd_value = 'hist_proppant_intensity'
        
    else:
        dd_options = [
            {"label": "Histogram of Stage Spacing per well",
             "value": "hist_stage_spacing"},
            {"label": "Boxplot of Stage Spacing by Campaign",
             "value": "boxplot_stage_spacing"},
            {"label": "Number of Stages vs. Horizontal Length, by Stage Spacing",
             "value": "scatter_number_stages_hor_length_stage_spacing"},
            {"label": "Production Indicator vs. Stage Spacing binned",
             "value": "boxplot_prod_ind_stage_spacing"}
            ]
        dd_value = 'hist_stage_spacing'
        
    return dd_options, dd_value

# Callback to generate map ----
@app.callback(
    Output('graph_tab7_map', 'figure'),
    [Input('ri_tab7_filter_var', "value"),
     Input('ri_tab7_filter_ind', "value"),
     Input('ri_tab7_prod_fluid','value'),
     Input('slider_tab7_campaign', "value")]
)
def update_map(ri_filter_var, ri_filter_ind, ri_fluid, slider_campaign):
    
    if ri_fluid == "Oil":
        dff = wells_df_oil
    if ri_fluid == "Gas":
        dff = wells_df_gas
    
    # filter df rows by slider campaign value
    dff=dff[(dff['campaign']>=slider_campaign[0])&(dff['campaign']<=slider_campaign[1])]
        
    if ri_filter_var == "proppant_intensity_lbm_ft":
        color_range = [1000,3500]
        color_midpoint = 2000
    elif ri_filter_var == "fluid_intensity_bbl_ft":
        color_range = [20,70]
        color_midpoint = 30
    else:
        color_range = [50,100]
        color_midpoint = 70
    
    fig = px.scatter_mapbox(
                    dff,
                    lat="latitude", 
                    lon="longitude",     
                    color=ri_filter_var,
                    range_color = color_range,
                    color_continuous_midpoint = color_midpoint,
                    size=ri_filter_ind,
                    opacity=0.4,
                    hover_name='well_name',
                    hover_data={'well_name':False,ri_filter_var:True,ri_filter_ind:True,
                                "latitude":False,"longitude":False},
                    #color_continuous_scale=px.colors.cyclical.IceFire, 
                    color_continuous_scale=px.colors.sequential.haline, 
                    size_max=30)
    fig.update_layout(hovermode='closest',
                      mapbox_style="carto-positron",
                      mapbox_zoom=8,
                      mapbox_center = {"lat": -38.0986, "lon": -68.746998})
    fig.update_layout(height=600, margin={"r":0,"t":0,"l":60,"b":0})

    return fig

# Callback to update the graph ----
@app.callback(
    Output('graph_tab7_completion', 'figure'),
    [Input('dd_tab7_graphs', 'value'),
     Input('ri_tab7_filter_ind', "value"),
     Input('ri_tab7_prod_fluid','value'),
     Input('slider_tab7_campaign', "value")])

def dd_options(dd_graphs, ri_filter_ind, ri_fluid, slider_campaign):
    
    if ri_fluid == "Oil":
        dff = wells_df_oil
    if ri_fluid == "Gas":
        dff = wells_df_gas
    
    # filter df rows by slider campaign value
    dff=dff[(dff['campaign']>=slider_campaign[0])&(dff['campaign']<=slider_campaign[1])]
    
    if dd_graphs == 'hist_fluid_intensity':
        fig = dff \
            .hist_no_agg('fluid_intensity_bbl_ft',
            produced_fluid = ri_fluid,
            title = 'Histogram of Fluid Intensity, bbl/ft',
            nbins = 50)
    
    elif dd_graphs == 'hist_proppant_intensity':
        fig = dff \
            .hist_no_agg('proppant_intensity_lbm_ft',
            produced_fluid = ri_fluid,
            title = 'Histogram of Proppant Intensity, lbm/ft',
            nbins = 50)
        
    elif dd_graphs == 'hist_stage_spacing':
        fig = dff \
            .hist_no_agg('stage_spacing',
            produced_fluid = ri_fluid,
            title = 'Histogram of Stage Spacing, m',
            nbins = 50)
    
    elif dd_graphs == 'boxplot_fluid_intensity':
        fig = dff \
            .boxplot_no_agg('fluid_intensity_bbl_ft','campaign',
            produced_fluid = ri_fluid,
            title = 'Boxplot of Fluid Intensity by Campaign')
            
    elif dd_graphs == 'boxplot_proppant_intensity':
        fig = dff \
            .boxplot_no_agg('proppant_intensity_lbm_ft','campaign',
            produced_fluid = ri_fluid,
            title = 'Boxplot of Proppant Intensity by Campaign')
            
    elif dd_graphs == 'boxplot_stage_spacing':
        fig = dff \
            .boxplot_no_agg('stage_spacing','campaign',
            produced_fluid = ri_fluid,
            title = 'Boxplot of Stage Spacing by Campaign')
            
    elif dd_graphs == 'scatter_fluid_volume_hor_length_fluid_int':
        fig = dff \
            .query(f"well_name != 'BCeCg-111(h)'") \
            .query(f"well_name != 'BCeCf-101(h)'") \
            .query(f"well_name != 'BCeCf-105(h)'") \
            .query(f"well_name != 'BCeCg-112(h)'") \
            .query(f"well_name != 'BCeAe-113(h)'") \
            .query(f"well_name != 'BCeCf-108(h)'") \
            .query(f"well_name != 'BCeCf-106(h)'") \
            .scatter_no_agg('horizontal_length', 'fluid_volume_bbl', 'fluid_intensity_bbl_ft', 'well_name',
            title = 'Fluid Volume vs. Horizontal Length by Fluid Intensity',
            bins = 'fluid_int_bins',
            trendline = 'ols', trend = 'trace')
            
    elif dd_graphs == 'scatter_proppant_volume_hor_length_proppant_int':
        fig = dff \
            .query(f"well_name != 'BCeCg-111(h)'") \
            .query(f"well_name != 'BCeCf-101(h)'") \
            .query(f"well_name != 'BCeCf-105(h)'") \
            .query(f"well_name != 'BCeCg-112(h)'") \
            .query(f"well_name != 'BCeAe-113(h)'") \
            .query(f"well_name != 'BCeCf-108(h)'") \
            .query(f"well_name != 'BCeCf-106(h)'") \
            .scatter_no_agg('horizontal_length', 'proppant_volume_lbm', 'proppant_intensity_lbm_ft', 'well_name',
            title = 'Proppant Volume vs. Horizontal Length by Proppant Intensity',
            bins = 'prop_int_bins',
            trendline = 'ols', trend = 'trace')         
            
    elif dd_graphs == 'scatter_number_stages_hor_length_stage_spacing':
        fig = dff \
            .query(f"well_name != 'BCeCg-111(h)'") \
            .query(f"well_name != 'BCeCf-101(h)'") \
            .query(f"well_name != 'BCeCf-105(h)'") \
            .query(f"well_name != 'BCeCg-112(h)'") \
            .query(f"well_name != 'BCeAe-113(h)'") \
            .query(f"well_name != 'BCeCf-108(h)'") \
            .query(f"well_name != 'BCeCf-106(h)'") \
            .scatter_no_agg('horizontal_length', 'number_of_stages', 'stage_spacing', 'well_name',
            title = 'Number of Stages vs. Horizontal Length by Stage Spacing binned',
            bins = 'stage_spacing_bins',
            trendline = 'ols', trend = 'trace')
            
    elif dd_graphs == 'boxplot_prod_ind_fluid_int':
        fig = dff \
            .query(f"well_name != 'BCeCg-111(h)'") \
            .query(f"well_name != 'BCeCf-101(h)'") \
            .query(f"well_name != 'BCeCf-105(h)'") \
            .query(f"well_name != 'BCeCg-112(h)'") \
            .query(f"well_name != 'BCeAe-113(h)'") \
            .query(f"well_name != 'BCeCf-108(h)'") \
            .query(f"well_name != 'BCeCf-106(h)'") \
            .boxplot_no_agg(ri_filter_ind,'fluid_intensity_bbl_ft',
            produced_fluid = ri_fluid,
            sort_category = False, flip_coord = False, bins = 'fluid_int_bins',
            title = f'Boxplot of {ri_filter_ind} by Fluid Intensity binned')
            
    elif dd_graphs == 'boxplot_prod_ind_proppant_int':
        fig = dff \
            .query(f"well_name != 'BCeCg-111(h)'") \
            .query(f"well_name != 'BCeCf-101(h)'") \
            .query(f"well_name != 'BCeCf-105(h)'") \
            .query(f"well_name != 'BCeCg-112(h)'") \
            .query(f"well_name != 'BCeAe-113(h)'") \
            .query(f"well_name != 'BCeCf-108(h)'") \
            .query(f"well_name != 'BCeCf-106(h)'") \
            .boxplot_no_agg(ri_filter_ind,'proppant_intensity_lbm_ft',
            produced_fluid = ri_fluid,
            sort_category = False, flip_coord = False, bins = 'prop_int_bins',
            title = f'Boxplot of {ri_filter_ind} by Proppant Intensity binned')
            
    elif dd_graphs == 'boxplot_prod_ind_stage_spacing':
        fig = dff \
            .query(f"well_name != 'BCeCg-111(h)'") \
            .query(f"well_name != 'BCeCf-101(h)'") \
            .query(f"well_name != 'BCeCf-105(h)'") \
            .query(f"well_name != 'BCeCg-112(h)'") \
            .query(f"well_name != 'BCeAe-113(h)'") \
            .query(f"well_name != 'BCeCf-108(h)'") \
            .query(f"well_name != 'BCeCf-106(h)'") \
            .boxplot_no_agg(ri_filter_ind,'stage_spacing',
            produced_fluid = ri_fluid,
            sort_category = False, flip_coord = False, bins = 'stage_spacing_bins',
            title = f'Boxplot of {ri_filter_ind} by Stage Spacing binned')
        
    fig.update_layout(height=600, margin={"r":40,"t":40,"l":60,"b":0}, font=dict(size=10))
    
    return fig
