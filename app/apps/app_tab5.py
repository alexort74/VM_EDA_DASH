# Type Curves
# Imports ----
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output#, Event
import dash_bootstrap_components as dbc
from dash_table.Format import Format, Scheme, Trim

import pandas as pd
import json

from my_pandas_extensions.plotting_plotly import *
#from my_pandas_extensions.database import collect_data

from app import app

# Data ----
#wells_final_df, production_final_df = collect_data()
wells_final_df = pd.read_pickle("datasets/wells_final_Q42021_df.pkl")
production_final_df = pd.read_pickle("datasets/production_final_Q42021_df.pkl")

production_df = production_final_df.copy()
production_df = production_df \
    .query(f"well_type == 'Horizontal'")

production_df_oil = production_df \
    .query(f"produced_fluid == 'Oil'")
    
production_df_gas = production_df \
    .query(f"produced_fluid == 'Gas'")

wells_df = wells_final_df.copy()
wells_df = wells_df \
    .query(f"well_type == 'Horizontal'")
    
wells_df_oil = wells_df \
    .query(f"produced_fluid == 'Oil'")
    
wells_df_gas = wells_df \
    .query(f"produced_fluid == 'Gas'")

columns_select=['well_name', 'operator', 'area', 'fluid_type', 'campaign']
wells_dict = wells_df[columns_select].to_dict(orient='index')
wells_dict_oil = wells_df_oil[columns_select].to_dict(orient='index')
wells_dict_gas = wells_df_gas[columns_select].to_dict(orient='index')
    
#app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])   

operator_groups = wells_df["operator"].unique()
area_groups = wells_df["area"].unique()
fluid_type_groups = wells_df["fluid_type"].unique()
campaign_groups = wells_df["campaign"].unique()
wells_groups = wells_df["well_name"].unique()

operator_groups_oil = wells_df_oil["operator"].unique()
area_groups_oil = wells_df_oil["area"].unique()
fluid_type_groups_oil = wells_df_oil["fluid_type"].unique()
campaign_groups_oil = wells_df_oil["campaign"].unique()
wells_groups_oil = wells_df_oil["well_name"].unique()

operator_groups_gas = wells_df_gas["operator"].unique()
area_groups_gas = wells_df_gas["area"].unique()
fluid_type_groups_gas = wells_df_gas["fluid_type"].unique()
campaign_groups_gas = wells_df_gas["campaign"].unique()
wells_groups_gas = wells_df_gas["well_name"].unique()
    
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
                                            id = 'ri_tab5_prod_fluid',
                                            options=[
                                                {'label': 'Oil', 'value': 'Oil'},
                                                {'label': 'Gas', 'value': 'Gas'}],
                                            value='Oil',
                                            labelClassName="mt-0 ml-2",
                                            style = {'font-size': '13px'}
                                        ),
                                    ], className="p-2"
                                )
                            ], className="mt-2 mb-1 pb-1"
                        ),
                    ], style={"height": "100%"}, width={'size': 2, "offset": 0, 'order': 1}
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.P(
                                                "Choose the grouping variable:",
                                                className="card-text",
                                            ),
                                        dcc.RadioItems(
                                            id = 'ri_tab5_filter',
                                            options=[
                                                {'label': 'Campaign', 'value': 'campaign'},
                                                {'label': 'Fluid Type', 'value': 'fluid_type'},
                                                {'label': 'Operator', 'value': 'operator'},
                                                {'label': 'Area', 'value': 'area'},
                                                ],
                                            value='campaign',
                                            labelClassName="mt-0 ml-1",
                                            style = {'font-size': '13px'}
                                        ),
                                    ], className="p-2"
                                )
                            ], className="mt-2 mb-1 pb-1",
                        ),
                    ], style={"height": "100%"}, width={'size': 3, "offset": 0, 'order': 2}
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                   [
                                        html.P(
                                                "Normalize production (2500 m):",
                                                className="card-text",
                                            ),
                                        dcc.RadioItems(
                                            id = 'ri_tab5_norm',
                                            options=[
                                                {'label': 'Yes', 'value': True},
                                                {'label': 'No', 'value': False}],
                                            value=False,
                                            labelClassName="mt-0 ml-2",
                                            style = {'font-size': '13px'}
                                        ),
                                    ], className="p-2"
                                )
                            ], className="mt-2 mb-1 pb-1"
                        ),
                    ], style={"height": "100%"}, width={'size': 2, "offset": 5, 'order': 3}
                ),
            ], className="h-10", justify='start'
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id = 'graph_tab5_rate', figure = {})
                    ], style={"height": "100%"}, width={'size': 5, "offset": 0}
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'graph_tab5_volume', figure = {}),
                    ], style={"height": "100%"}, width={'size': 5, "offset": 0}
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.P(
                                        "Choose the Operator:",
                                        className="card-text",
                                        ),
                                        dcc.Dropdown(id='dd_tab5_operator',
                                                #options=operator_groups_all_oil,
                                                value=[''],
                                                clearable = False,
                                                placeholder="Select Operators (leave blank to include all)",
                                                multi=True,
                                                style = {'font-size': '13px','text-overflow': 'ellipsis'},
                                        )
                                    ], className="p-2"
                                )
                            ], className="mt-5 mb-1 pb-0", outline=True,
                        ),
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.P(
                                        "Choose the Area:",
                                        className="card-text",
                                        ),
                                        dcc.Dropdown(id='dd_tab5_area',
                                                #options=area_groups_all_oil,
                                                value=[''],
                                                clearable = False,
                                                placeholder="Select areas (leave blank to include all)",
                                                multi=True,
                                                style = {'font-size': '13px','text-overflow': 'ellipsis'}
                                                #style = {'font-size': '13px', 'color' : corporate_colors['medium-blue-grey'], 'white-space': 'nowrap', 'text-overflow': 'ellipsis'}
                                        )
                                    ], className="p-2"
                                )
                            ], className="mt-2 mb-1 pb-0", outline=True,
                        ),
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.P(
                                        "Choose the Fluid Type:",
                                        className="card-text",
                                        ),
                                        dcc.Dropdown(id='dd_tab5_fluid_type',
                                                #options=fluid_type_groups_all_oil,
                                                value=[''],
                                                clearable = False,
                                                placeholder="Select fluid types (leave blank to include all)",
                                                multi=True,
                                                style = {'font-size': '13px','text-overflow': 'ellipsis'}
                                        )
                                    ], className="p-2"
                                )
                            ], className="mt-2 mb-1 pb-0", outline=True,
                        ),
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.P(
                                        "Choose the Campaign:",
                                        className="card-text",
                                        ),
                                        dcc.Dropdown(id='dd_tab5_campaign',
                                                #options=campaign_groups_all_oil,
                                                value=[''],
                                                clearable = False,
                                                placeholder="Select Campaigns (leave blank to include all)",
                                                multi=True,
                                                style = {'font-size': '13px', 'text-overflow': 'ellipsis'}
                                        )
                                    ], className="p-2"
                                )
                            ], className="mt-2 mb-1 pb-0", outline=True,
                        ),
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.P(
                                        "Choose the Wells:",
                                        className="card-text",
                                        ),
                                        dcc.Dropdown(id='dd_tab5_wells',
                                                #options=campaign_groups_all_oil,
                                                value=[''],
                                                clearable = False,
                                                placeholder="Select Wells (leave blank to include all)",
                                                multi=True,
                                                style = {'font-size': '13px', 'text-overflow': 'ellipsis'}
                                        )
                                    ], className="p-2"
                                )
                            ], className="mt-2 mb-1 pb-0", outline=True,
                        )
                    ],style={"height": "100%"}, width={'size': 2, "offset": 0}
                ),
                dcc.Store(id='store_tab5_data')
            ], className="h-80", align="center", justify='around'
        )
], style={"height": "100vh"}, fluid=True)

#----------------------------------------------
# Callback to configure PRODUCED FLUID radio item 
@app.callback( 
     [Output('dd_tab5_operator', 'value'),
      Output('dd_tab5_area','value'),
      Output('dd_tab5_fluid_type','value'),
      Output('dd_tab5_campaign','value'),
      Output('dd_tab5_wells','value')],
     [Input('ri_tab5_prod_fluid', 'value')]
 )

def dd_operator_options(ri_fluid):

    operator_value=['']
    area_value=['']
    fluid_type_value=['']
    campaign_value=['']
    wells_value=['']
    
    return operator_value, area_value, fluid_type_value, campaign_value, wells_value

# Callback to configure OPERATOR dropdowns 
@app.callback( 
     Output('dd_tab5_operator', 'options'),
     [
      #Input('dd_tab5_area','value'),
      #Input('dd_tab5_fluid_type','value'),
      #Input('dd_tab5_campaign','value'),
      #Input('dd_tab5_wells','value'),
      Input('ri_tab5_prod_fluid', 'value')]
 )

def dd_operator_options(
    #dd_area_value, dd_fluid_type_value, dd_campaign_value, dd_wells_value, 
    ri_fluid):
    
    if ri_fluid == 'Oil':
        clean_filter_dic = wells_dict_oil
    else:
        clean_filter_dic = wells_dict_gas
    
    #dd_values = [dd_area_value, dd_fluid_type_value, dd_campaign_value, dd_wells_value]

    #for dd_item in dd_values:
        
    #    isselect_all = 'Start' #Initialize isselect_all
    
        #Rembember that the dropdown value is a list !
    #    for i in dd_item:
    #        if i == 'All':
    #            isselect_all = 'Y'
    #            break
    #        elif i != '':
    #            isselect_all = 'N'
    #        else:
    #            pass
        
    #    if isselect_all == 'N':
    #        results_dic={k1: {k2:v2 for k2, v2 in v1.items() if v2 in dd_item} for k1, v1 in clean_filter_dic.items()}
    #        clean_dic = {i:j for i,j in results_dic.items() if j != {}}
    #        index_list = [i for i,j in clean_dic.items()]
    #        filter_dic={k1: {k2:v2 for k2, v2 in v1.items() if k1 in index_list} for k1, v1 in clean_filter_dic.items()}
    #        clean_filter_dic = {i:j for i,j in filter_dic.items() if j != {}}
            
    #    #Create options for select all or none
    #    else:
    #        pass
    
    dd_option_operator = np.unique([item['operator'] for item in clean_filter_dic.values()]).tolist()
    options_final_1 = [{'label' : k, 'value' : k} for k in sorted(dd_option_operator)]
    options_final_0 = [{'label' : '(Select All)', 'value' : 'All'}]
    options_final_operator = options_final_0 + options_final_1
    
    return options_final_operator

#----------------------------------------------
# Callback to configure AREA dropdown
@app.callback( 
     
      Output('dd_tab5_area', 'options'),
     [Input('dd_tab5_operator','value'),
      Input('dd_tab5_fluid_type','value'),
      Input('dd_tab5_campaign','value'),
      Input('dd_tab5_wells','value'),
      Input('ri_tab5_prod_fluid', 'value')]
 )

def dd_area_options(dd_operator_value, dd_fluid_type_value, dd_campaign_value, dd_wells_value, ri_fluid):
    
    if ri_fluid == 'Oil':
        clean_filter_dic = wells_dict_oil
    
    else:
        clean_filter_dic = wells_dict_gas
        
    dd_values = [dd_operator_value, dd_fluid_type_value, dd_campaign_value, dd_wells_value]

    for dd_item in dd_values:
        
        isselect_all = 'Start' #Initialize isselect_all
    
        #Rembember that the dropdown value is a list !
        for i in dd_item:
            if i == 'All':
                isselect_all = 'Y'
                break
            elif i != '':
                isselect_all = 'N'
            else:
                pass
        
        if isselect_all == 'N':
            results_dic={k1: {k2:v2 for k2, v2 in v1.items() if v2 in dd_item} for k1, v1 in clean_filter_dic.items()}
            clean_dic = {i:j for i,j in results_dic.items() if j != {}}
            index_list = [i for i,j in clean_dic.items()]
            filter_dic={k1: {k2:v2 for k2, v2 in v1.items() if k1 in index_list} for k1, v1 in clean_filter_dic.items()}
            clean_filter_dic = {i:j for i,j in filter_dic.items() if j != {}}
            
        #Create options for select all or none
        else:
            pass
    
    dd_option_area = np.unique([item['area'] for item in clean_filter_dic.values()]).tolist()
    options_final_1 = [{'label' : k, 'value' : k} for k in sorted(dd_option_area)]
    options_final_0 = [{'label' : '(Select All)', 'value' : 'All'}]
    options_final_area = options_final_0 + options_final_1
    
    return options_final_area

#----------------------------------------------
# Callback to configure FLUID TYPE dropdowns
@app.callback( 
      Output('dd_tab5_fluid_type', 'options'),
     [Input('dd_tab5_operator','value'),
      Input('dd_tab5_area','value'),
      Input('dd_tab5_campaign','value'),
      Input('dd_tab5_wells','value'),
      Input('ri_tab5_prod_fluid', 'value')]
 )

def dd_fluid_type_options(dd_operator_value, dd_area_value, dd_campaign_value, dd_wells_value, ri_fluid):
    
    if ri_fluid == 'Oil':
        clean_filter_dic = wells_dict_oil
    else:
        clean_filter_dic = wells_dict_gas
        
    dd_values = [dd_operator_value, dd_area_value, dd_campaign_value, dd_wells_value]
    
    for dd_item in dd_values:
        
        isselect_all = 'Start' #Initialize isselect_all
    
        #Rembember that the dropdown value is a list !
        for i in dd_item:
            if i == 'All':
                isselect_all = 'Y'
                break
            elif i != '':
                isselect_all = 'N'
            else:
                pass
        
        if isselect_all == 'N':
            results_dic={k1: {k2:v2 for k2, v2 in v1.items() if v2 in dd_item} for k1, v1 in clean_filter_dic.items()}
            clean_dic = {i:j for i,j in results_dic.items() if j != {}}
            index_list = [i for i,j in clean_dic.items()]
            filter_dic={k1: {k2:v2 for k2, v2 in v1.items() if k1 in index_list} for k1, v1 in clean_filter_dic.items()}
            clean_filter_dic = {i:j for i,j in filter_dic.items() if j != {}}
            
        #Create options for select all or none
        else:
            pass
    
    dd_option_fluid_type = np.unique([item['fluid_type'] for item in clean_filter_dic.values()]).tolist()
    options_final_1 = [{'label' : k, 'value' : k} for k in sorted(dd_option_fluid_type)]
    options_final_0 = [{'label' : '(Select All)', 'value' : 'All'}]
    options_final_fluid_type = options_final_0 + options_final_1
    
    return options_final_fluid_type

#----------------------------------------------
# Callback to configure CAMPAIGN dropdowns
@app.callback( 
      Output('dd_tab5_campaign', 'options'),
     [Input('dd_tab5_operator','value'),
      Input('dd_tab5_area','value'),
      Input('dd_tab5_fluid_type','value'),
      Input('dd_tab5_wells','value'),
      Input('ri_tab5_prod_fluid', 'value')]
 )

def dd_campaign_options(dd_operator_value, dd_area_value, dd_fluid_type_value, dd_wells_value, ri_fluid):
    
    if ri_fluid == 'Oil':
        clean_filter_dic = wells_dict_oil
    else:
        clean_filter_dic = wells_dict_gas
    
    dd_values = [dd_operator_value, dd_area_value, dd_fluid_type_value, dd_wells_value]
    
    for dd_item in dd_values:
        
        isselect_all = 'Start' #Initialize isselect_all
    
        #Rembember that the dropdown value is a list !
        for i in dd_item:
            if i == 'All':
                isselect_all = 'Y'
                break
            elif i != '':
                isselect_all = 'N'
            else:
                pass
        
        if isselect_all == 'N':
            results_dic={k1: {k2:v2 for k2, v2 in v1.items() if v2 in dd_item} for k1, v1 in clean_filter_dic.items()}
            clean_dic = {i:j for i,j in results_dic.items() if j != {}}
            index_list = [i for i,j in clean_dic.items()]
            filter_dic={k1: {k2:v2 for k2, v2 in v1.items() if k1 in index_list} for k1, v1 in clean_filter_dic.items()}
            clean_filter_dic = {i:j for i,j in filter_dic.items() if j != {}}
            
        #Create options for select all or none
        else:
            pass
    
    dd_option_campaign = np.unique([item['campaign'] for item in clean_filter_dic.values()]).tolist()
    options_final_1 = [{'label' : k, 'value' : k} for k in sorted(dd_option_campaign)]
    options_final_0 = [{'label' : '(Select All)', 'value' : 'All'}]
    options_final_campaign = options_final_0 + options_final_1
    
    return options_final_campaign

#----------------------------------------------
# Callback to configure WELLS dropdowns
@app.callback( 
      Output('dd_tab5_wells', 'options'),
     [Input('dd_tab5_operator','value'),
      Input('dd_tab5_area','value'),
      Input('dd_tab5_fluid_type','value'),
      Input('dd_tab5_campaign','value'),
      Input('ri_tab5_prod_fluid', 'value')]
 )

def dd_wells_options(dd_operator_value, dd_area_value, dd_fluid_type_value, dd_campaign_value, ri_fluid):
    
    if ri_fluid == 'Oil':
        clean_filter_dic = wells_dict_oil
    else:
        clean_filter_dic = wells_dict_gas
    
    dd_values = [dd_operator_value, dd_area_value, dd_fluid_type_value, dd_campaign_value]
    
    for dd_item in dd_values:
        
        isselect_all = 'Start' #Initialize isselect_all
    
        #Rembember that the dropdown value is a list !
        for i in dd_item:
            if i == 'All':
                isselect_all = 'Y'
                break
            elif i != '':
                isselect_all = 'N'
            else:
                pass
        
        if isselect_all == 'N':
            results_dic={k1: {k2:v2 for k2, v2 in v1.items() if v2 in dd_item} for k1, v1 in clean_filter_dic.items()}
            clean_dic = {i:j for i,j in results_dic.items() if j != {}}
            index_list = [i for i,j in clean_dic.items()]
            filter_dic={k1: {k2:v2 for k2, v2 in v1.items() if k1 in index_list} for k1, v1 in clean_filter_dic.items()}
            clean_filter_dic = {i:j for i,j in filter_dic.items() if j != {}}
            
        #Create options for select all or none
        else:
            pass
    
    dd_option_wells = np.unique([item['well_name'] for item in clean_filter_dic.values()]).tolist()
    options_final_1 = [{'label' : k, 'value' : k} for k in sorted(dd_option_wells)]
    options_final_0 = [{'label' : '(Select All)', 'value' : 'All'}]
    options_final_wells = options_final_0 + options_final_1
    
    return options_final_wells

#----------------------------------------------
# Callback to filter production_df dataframe
@app.callback( 
    Output('store_tab5_data', 'data'),
    [Input('dd_tab5_operator', 'value'),
     Input('dd_tab5_area', 'value'),
     Input('dd_tab5_fluid_type', 'value'),
     Input('dd_tab5_campaign', 'value'),
     Input('dd_tab5_wells', 'value'),
     Input('ri_tab5_prod_fluid', 'value')]
)

def process_data(dd_operator,dd_area,dd_fluid_type,dd_campaign,dd_wells, ri_fluid):
    
    # Filter based on the dropdowns
    isselect_all_operator = 'Start' #Initialize isselect_all
    isselect_all_area = 'Start' #Initialize isselect_all
    isselect_all_fluid_type = 'Start' #Initialize isselect_all
    isselect_all_campaign = 'Start' #Initialize isselect_all
    isselect_all_wells = 'Start' #Initialize isselect_all
    
    if ri_fluid == 'Oil':    
        prod_df=production_df_oil  \
            .query(f"well_name != 'BCeCg-111(h)'") \
            .query(f"well_name != 'BCeCf-101(h)'") \
            .query(f"well_name != 'BCeCf-105(h)'") \
            .query(f"well_name != 'BCeCg-112(h)'") \
            .query(f"well_name != 'BCeAe-113(h)'") \
            .query(f"well_name != 'BCeCf-108(h)'") \
            .query(f"well_name != 'BCeCf-106(h)'")
    
    if ri_fluid == 'Gas':    
        prod_df=production_df_gas  \
            .query(f"well_name != 'BCeCg-111(h)'") \
            .query(f"well_name != 'BCeCf-101(h)'") \
            .query(f"well_name != 'BCeCf-105(h)'") \
            .query(f"well_name != 'BCeCg-112(h)'") \
            .query(f"well_name != 'BCeAe-113(h)'") \
            .query(f"well_name != 'BCeCf-108(h)'") \
            .query(f"well_name != 'BCeCf-106(h)'")
    
    if ri_fluid == 'Oil': 
        # =======================================================================
        ## Operator selection (dropdown value is a list!) ----
        for i in dd_operator:
            if i == 'All':
                isselect_all_operator = 'Y'
                break
            elif i != '':
                isselect_all_operator = 'N'
            else:
                pass
        
        # Filter df according to OPERATOR selection
        if isselect_all_operator == 'N':
            value_0 = []
            for i in dd_operator:
                if i not in operator_groups_oil:
                    pass
                else:
                    value_0.append(i)
        
            if value_0 == []:
                prod_df1 = prod_df.copy()
            else:
                prod_df1 = prod_df[prod_df['operator'].isin(dd_operator)]
        else:
            prod_df1 = prod_df.copy()
            
        # =======================================================================
        ## Area selection (dropdown value is a list!) ----
        for i in dd_area:
            if i == 'All':
                isselect_all_area = 'Y'
                break
            elif i != '':
                isselect_all_area = 'N'
            else:
                pass
            
        # Filter df according to AREA selection
        if isselect_all_area == 'N':
            value_0 = []
            for i in dd_area:
                if i not in area_groups_oil:
                    pass
                else:
                    value_0.append(i)
        
            if value_0 == []:
                prod_df2 = prod_df1.copy()
            else:
                prod_df2 = prod_df1[prod_df1['area'].isin(dd_area)]
        else:
            prod_df2 = prod_df1.copy()
            
        # =======================================================================
        ## Fluid type selection (dropdown value is a list!) ----
        for i in dd_fluid_type:
            if i == 'All':
                isselect_all_fluid_type = 'Y'
                break
            elif i != '':
                isselect_all_fluid_type = 'N'
            else:
                pass
            
        # Filter df according to FLUID TYPE selection
        if isselect_all_fluid_type == 'N':
            value_0 = []
            for i in dd_fluid_type:
                if i not in fluid_type_groups_oil:
                    pass
                else:
                    value_0.append(i)
        
            if value_0 == []:
                prod_df3 = prod_df2.copy()
            else:
                prod_df3 = prod_df2[prod_df2['fluid_type'].isin(dd_fluid_type)]
        else:
            prod_df3 = prod_df2.copy()
            
        # =======================================================================
        ## Campaign selection (dropdown value is a list!) ----
        for i in dd_campaign:
            if i == 'All':
                isselect_all_campaign = 'Y'
                break
            elif i != '':
                isselect_all_campaign = 'N'
            else:
                pass
        
        # Filter df according to CAMPAIGN selection
        if isselect_all_campaign == 'N':
            value_0 = []
            for i in dd_campaign:
                if i not in campaign_groups_oil:
                    pass
                else:
                    value_0.append(i)
        
            if value_0 == []:
                prod_df4 = prod_df3.copy()
            else:
                prod_df4 = prod_df3[prod_df3['campaign'].isin(dd_campaign)]
        else:
            prod_df4 = prod_df3.copy()
            
        # =======================================================================
        ## Wells selection (dropdown value is a list!) ----
        for i in dd_wells:
            if i == 'All':
                isselect_all_wells = 'Y'
                break
            elif i != '':
                isselect_all_wells = 'N'
            else:
                pass
        
        # Filter df according to WELLS selection
        if isselect_all_wells == 'N':
            value_0 = []
            for i in dd_wells:
                if i not in wells_groups_oil:
                    pass
                else:
                    value_0.append(i)
        
            if value_0 == []:
                prod_df5 = prod_df4.copy()
            else:
                prod_df5 = prod_df4[prod_df4['well_name'].isin(dd_wells)]
        else:
            prod_df5 = prod_df4.copy() 
    
    if ri_fluid == 'Gas':    
        # =======================================================================
        ## Operator selection (dropdown value is a list!) ----
        for i in dd_operator:
            if i == 'All':
                isselect_all_operator = 'Y'
                break
            elif i != '':
                isselect_all_operator = 'N'
            else:
                pass
        
        # Filter df according to OPERATOR selection
        if isselect_all_operator == 'N':
        
            value_0 = []
            for i in dd_operator:
                if i not in operator_groups_gas:
                    pass
                else:
                    value_0.append(i)
        
            if value_0 == []:
                prod_df1 = prod_df.copy()
            else:
                prod_df1 = prod_df[prod_df['operator'].isin(dd_operator)]
        else:
            prod_df1 = prod_df.copy()
        
        # =======================================================================
        ## Area selection (dropdown value is a list!) ----
        for i in dd_area:
            if i == 'All':
                isselect_all_area = 'Y'
                break
            elif i != '':
                isselect_all_area = 'N'
            else:
                pass
            
        # Filter df according to AREA selection
        if isselect_all_area == 'N':
            value_0 = []
            for i in dd_area:
                if i not in area_groups_gas:
                    pass
                else:
                    value_0.append(i)
        
            if value_0 == []:
                prod_df2 = prod_df1.copy()
            else:
                prod_df2 = prod_df1[prod_df1['area'].isin(dd_area)]
        else:
            prod_df2 = prod_df1.copy()
        
        # =======================================================================
        ## Fluid type selection (dropdown value is a list!) ----
        for i in dd_fluid_type:
            if i == 'All':
                isselect_all_fluid_type = 'Y'
                break
            elif i != '':
                isselect_all_fluid_type = 'N'
            else:
                pass
            
        # Filter df according to FLUID TYPE selection
        if isselect_all_fluid_type == 'N':
            value_0 = []
            for i in dd_fluid_type:
                if i not in fluid_type_groups_gas:
                    pass
                else:
                    value_0.append(i)
        
            if value_0 == []:
                prod_df3 = prod_df2.copy()
            else:
                prod_df3 = prod_df2[prod_df2['fluid_type'].isin(dd_fluid_type)]
        else:
            prod_df3 = prod_df2.copy()
        
        # =======================================================================
        ## Campaign selection (dropdown value is a list!) ----
        for i in dd_campaign:
            if i == 'All':
                isselect_all_campaign = 'Y'
                break
            elif i != '':
                isselect_all_campaign = 'N'
            else:
                pass
        
        # Filter df according to CAMPAIGN selection
        if isselect_all_campaign == 'N':
            value_0 = []
            for i in dd_campaign:
                if i not in campaign_groups_gas:
                    pass
                else:
                    value_0.append(i)
        
            if value_0 == []:
                prod_df4 = prod_df3.copy()
            else:
                prod_df4 = prod_df3[prod_df3['campaign'].isin(dd_campaign)]
        else:
            prod_df4 = prod_df3.copy() 
        
        # =======================================================================
        ## Wells selection (dropdown value is a list!) ----
        for i in dd_wells:
            if i == 'All':
                isselect_all_wells = 'Y'
                break
            elif i != '':
                isselect_all_wells = 'N'
            else:
                pass
        
        # Filter df according to WELLS selection
        if isselect_all_wells == 'N':
            value_0 = []
            for i in dd_wells:
                if i not in wells_groups_gas:
                    pass
                else:
                    value_0.append(i)
        
            if value_0 == []:
                prod_df5 = prod_df4.copy()
            else:
                prod_df5 = prod_df4[prod_df4['well_name'].isin(dd_wells)]
        else:
            prod_df5 = prod_df4.copy()        

    # =======================================================================
    # Rename Date column
    prod_df5 = prod_df5.rename(columns={'production_date':'date'})

    if (len(prod_df5) > 0):
        prod_df_json = prod_df5.to_json()
    else:
        raise dash.exceptions.PreventUpdate
    
    return prod_df_json

#----------------------------------------------
# Callback to generate rate figure
@app.callback(
            Output('graph_tab5_rate', 'figure'),
             [Input('store_tab5_data', 'data'),
              Input('ri_tab5_prod_fluid', 'value'),
              Input('ri_tab5_filter', 'value'),
              Input('ri_tab5_norm','value')]
             )

def graph_tab4_rate_fun(df_json, ri_fluid, ri_filter, norm):
    df = pd.read_json(df_json, convert_axes=True, convert_dates=True)

    df = df.rename(columns={
            'date':'production_date'
        })   

    if ri_fluid == 'Oil':
        fig=df \
            .line_rate_plot_agg('production_date', 'oil_month_bbl',
            ri_filter, 'well_name', 
            well_type = 'Horizontal', produced_fluid = ri_fluid,
            plot_type = 'rate', normalized = norm, agg_func = np.mean,
            title='Average Oil Production Rate vs. Time',
            y_label = 'Average Oil Rate, bbl/d')
            
    if ri_fluid == 'Gas':
        fig=df \
            .line_rate_plot_agg('production_date', 'gas_month_mscf',
            ri_filter, 'well_name', 
            well_type = 'Horizontal', produced_fluid = ri_fluid,
            plot_type = 'rate', normalized = norm, agg_func = np.mean,
            title='Average Gas Production Rate vs. Time',
            y_label = 'Average Gas Rate, Mscf/d')

    fig.update_layout(height=600)
    fig.update_layout(margin=dict(t=80, r=20, l=20, b=0), font=dict(size=10)) 

    return fig 

#----------------------------------------------
# Callback to generate volume figure
@app.callback(
            Output('graph_tab5_volume', 'figure'),
             [Input('store_tab5_data', 'data'),
              Input('ri_tab5_prod_fluid', 'value'),
              Input('ri_tab5_filter', 'value'),
              Input('ri_tab5_norm','value')]
             )

def graph_tab4_rate_fun(df_json, ri_fluid, ri_filter, norm):
    df = pd.read_json(df_json, convert_axes=True, convert_dates=True)

    df = df.rename(columns={
            'date':'production_date'
        })   

    if ri_fluid == 'Oil':
        fig=df \
            .line_rate_plot_agg('production_date', 'oil_month_bbl',
            ri_filter, 'well_name', 
            well_type = 'Horizontal', produced_fluid = ri_fluid,
            plot_type = 'volume', normalized = norm, agg_func = np.mean,
            title='Average Oil Production Volume vs. Time',
            y_label = 'Average Cum. Oil Prod., bbl')
            
    if ri_fluid == 'Gas':
        fig=df \
            .line_rate_plot_agg('production_date', 'gas_month_mscf',
            ri_filter, 'well_name', 
            well_type = 'Horizontal', produced_fluid = ri_fluid,
            plot_type = 'volume', normalized = norm, agg_func = np.mean,
            title='Average Gas Production Volume vs. Time',
            y_label = 'Average Cum. Gas Prod., Mscf')

    fig.update_layout(height=600)
    fig.update_layout(margin=dict(t=80, r=20, l=20, b=0), font=dict(size=10)) 

    return fig 

