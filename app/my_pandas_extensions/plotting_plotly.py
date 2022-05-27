from re import X
from numpy.core.fromnumeric import size
import pandas as pd
import numpy as np

import statsmodels.api as sm
import datetime as dt

# Plotting
import plotly.express as px
import plotly.graph_objects as go

import pandas_flavor as pf
from plydata.cat_tools import cat_reorder

# from my_pandas_extensions.database import collect_data
# wells_final_df, production_final_df = collect_data()

#af_type_curve = pd.read_csv('00_data_raw/PHz_2.5_L1_20_UN.csv')
#af_type_curve = af_type_curve[af_type_curve['prod_month']<=36]

def remove_unused_categories(data):
    """ The `remove_unused_categories` method in pandas
        removes categories from a Series if there are no
        elements of that category.
        
        This function is a convenience function that removes
        unused categories for all categorical columns
        of a data frame.
        
        The reason this is useful is that when we
        fit a linear regression, `statsmodels` will
        create a coefficient for every category in a column,
        and so unused categories pollute the results.
    """
    for cname in data:
        col = data[cname]
        if pd.api.types.is_categorical_dtype(col):
            data[cname] = col.cat.remove_unused_categories()
    return data

def get_col_names(col_list):

    names_dict = {
        'production_date' : 'Production Date',
        'cum_eff_prod_day' : 'Production Days',
        'production_status':'Well Count',
        'production_status_count':'Well Count',
        'well_name_count' : 'Well Count',
        'completion_date' : 'Completion Date',
        'campaign' : 'Campaign',
        'well_type' : 'Well Type',
        'fluid_type' : 'Fluid Type',
        'operator' : 'Operator',
        'well_name' : 'Well Name',
        'area' : 'Area',
        'horizontal_length' : 'Horizontal Length, m',
        'total_depth': 'Total Length, m',
        'number_of_stages' : 'Number of Stages',
        'number_of_stages_mean' : 'Avg Number of Stages',
        'hor_length_group' : 'Horizontal Length Bin, m',
        'stages_group' : 'Number of Stages Bin',
        'spacing_group' : 'Stage Spacing Bin, m',
        'prop_int_group' : 'Proppant Intensity Bin, lbm/ft',
        'fluid_int_group' : 'Fluid Intensity Bin, bbl/ft',
        'prop_fluid_group' : 'Proppant/Fluid Ratio Bin, lbm/gal',
        'stage_spacing' : 'Stage Spacing, m',
        'fluid_volume_m3' : 'Fluid Volume, m3',
        'fluid_volume_bbl' : 'Fluid Volume, bbl',
        'proppant_volume_lbm' : 'Proppant Volume, lbm',
        'proppant_stage_lbm' : 'Proppant per Stage, lbm',
        'fluid_stage_m3' : 'Fluid per Stage, m3',
        'proppant_intensity_lbm_ft' : 'Proppant Intensity, lbm/ft',
        'proppant_fluid_ratio_lbm_gal' : 'Proppant/Fluid Ratio, lbm/gal',
        'fluid_intensity_bbl_ft' : 'Fluid Intensity, bbl/ft',
        'max_qo_bpd' : 'Initial Oil Rate, bbl/day',
        'max_qo_bpd_mean' : 'Avg Initial Oil Rate, bbl/day',
        'max_qg_mscfd' : 'Initial Gas Rate, Mscf/day',
        'eur_total_mboeq' : 'EUR, mboe',
        'eur_total_mboeq_mean' : 'Avg EUR, mboe',
        'cum180_oil_bbl' : '180-Day Cum. Oil, bbl',
        'cum180_oil_bbl_mean' : 'Avg 180-Day Cum. Oil, bbl',
        'cum180_gas_mscf' : '180-Day Cum. Gas, Mscf',
        'oil_month_bpd' : 'Oil Production Rate, bbl/day',
        'oil_month_bbl' : 'Oil Production, bbl',
        'norm_oil_month_bpd' : 'Normalized Oil Production Rate, bbl/day',
        'cum_oil_bbl' : 'Cumulative Oil Prod., bbl',
        'cum_gas_mscf' : 'Cumulative Gas Prod., mscf',
        'norm_cum_oil_bbl' : 'Normalized Cumulative Oil Prod., bbl',
        'gas_month_mscf' : 'Gas Production, Mscf',
        'gas_month_mscf_d' : 'Gas Production Rate, Mscf/day',
        'max_qo_bpd_stage' : 'Average Initial Oil Rate per Stage, bbl/day',
        'cum180_oil_bbl_stage' : 'Average Cum. Oil Prod. per Stage, bbl',
        'avg_rate' : 'Avg Oil Rate, bbl/day',
        'avg_cum_volume' : 'Avg Cumulative Oil Prod., bbl',
        'diff_months' : 'Production Time, Months',
        'landing' : 'Landing Zone',
    }
 
    name_list = []
    for col in col_list:
        col_name = names_dict[col]
        name_list.append(col_name)

    return name_list

def d_months(s, df):
    grp = df.loc[s.index]
    first_date = grp.production_date.iloc[0]
    diff_months = round((
        (grp['production_date'] - first_date)/np.timedelta64(1, 'M')
        ) + 1)
    return diff_months

# SCATTER PLOT ----

#scatter_date_no_agg - 20 plots
@pf.register_dataframe_method
def scatter_date_no_agg(
    data, date_column, y_column, group_column, id_column,
    bins = None,
    title = None,
    x_label = None,
    y_label = None
    ):

    # Filter by well type and produced fluid
    df = data[[date_column, y_column, group_column, id_column]]
    df = df \
        .query(f"{y_column} == {y_column}")

    if bins == 'stages_bins':
        df = df \
            .query(f"{group_column} == {group_column}") \
            .assign(stages_group = lambda x: pd.qcut(x[group_column], 
                q=[0,0.08,0.18,0.45,0.65,0.85,0.95,1], 
                labels=['stg05', 'stg15', 'stg20', 'stg25', 'stg35', 'stg40', 'stg50']
                        )) \
            .drop('number_of_stages', axis = 1)

        group_column = 'stages_group'
        df = df[[date_column, y_column, group_column, id_column]]

    if bins == 'horizontal_length_bins':
        df = df \
            .query(f"{group_column} == {group_column}") \
            .assign(hor_length_group = lambda x: pd.qcut(x[group_column], 
                q=[0,0.02,0.09,0.14,0.5,0.75,0.975,1], 
            labels=['hz500', 'hz1000', 'hz1300', 'hz1500', 'hz2000', 'hz2500', 'hz3000']
                        )) \
            .drop('horizontal_length', axis = 1)

        group_column = 'hor_length_group'
        df = df[[date_column, y_column, group_column, id_column]]

    if bins == 'stage_spacing_bins':
        df = df \
            .query(f"{group_column} == {group_column}") \
            .assign(spacing_group = lambda x: pd.qcut(x[group_column], 
                q=[0,0.025,0.17,0.37,0.96,1.0], 
            labels=['stg_spc_050', 'stg_spc_060', 'stg_spc_070', 'stg_spc_080', 'stg_spc_100']
                        )) \
            .drop('stage_spacing', axis = 1)

        group_column = 'spacing_group'
        df = df[[date_column, y_column, group_column, id_column]]

    # Grouping variable as category
    df[group_column] = df[group_column].astype('category')
    
    # Remove unused categories
    remove_unused_categories(df)

    # Rename columns
    date_column, y_column, group_column, id_column = get_col_names(df.columns)
    df.columns = [date_column, y_column, group_column, id_column]

    # Defining Labs
    if title == None:
        title = f"Plot of {y_column} vs. {date_column} by {group_column}"
    
    if x_label == None:
        x_label = date_column

    if y_label == None:
        y_label = y_column

    # Visualize

    df = df.sort_values(by=[date_column], ascending=[True])

    # data for time series linear regression
    #df['timestamp']=pd.to_datetime(df['completion_date'])
    df['serialtime']=[(d-dt.datetime(1970,1,1)).days for d in df[date_column]]

    x = sm.add_constant(df['serialtime'])
    model = sm.OLS(df[y_column], x).fit()
    df['bestfit']=model.fittedvalues

    # Find the different groups
    groups = df[group_column].unique()

    # Create as many traces as different groups there are and save them in data list
    data = []
    for group in groups:
        df_group = df[df[group_column] == group]
        trace = go.Scatter(
                        x=df_group[date_column], 
                        y=df_group[y_column],
                        mode='markers',
                        #opacity=0.5,
                        marker = dict(
                            size = 8,
                            #size=0.1*df[y_column],
                            line=dict(
                                color='white',
                                width=0.5),
                            opacity = 0.5
                        ),
                        hovertext=df_group[id_column],
                        hoverinfo = 'text + x + y',
                        name=group
                        )
        data.append(trace)

    # Layout of the plot
    layout = go.Layout(title=title,
                # xaxis = dict(title = x_label),
                # yaxis = dict(title = y_label),
                hovermode = 'closest'
                )
    fig = go.Figure(data=data, layout=layout)

    # regression data
    fig.add_trace(go.Scatter(x=df[date_column],
                            y=df['bestfit'],
                            mode='lines',
                            name='Overall Trendline',
                            #line=dict(color='firebrick', width=2)
                            ))

    #fig.update_traces(marker = dict(size=0.01*df[y_column],sizemin = 3))
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        legend_title=group_column,
        # font=dict(
        #     family="Courier New, monospace",
        #     size=18,
        #     color="RebeccaPurple"
    )

    return fig

#scatter_no_agg - 54 plots
@pf.register_dataframe_method
def scatter_no_agg(
    data, x_column, y_column, group_column, id_column,
    bins = None,
    trendline="lowess",
    trend = 'overall',
    title = None,
    x_label = None,
    y_label = None
    ):

    # Filter by well type and produced fluid
    df = data[[x_column, y_column, group_column, id_column]]
    df = df \
        .query(f"{x_column} == {x_column}") \
        .query(f"{y_column} == {y_column}")

    if bins == 'stages_bins':
        df = df \
            .query(f"{group_column} == {group_column}") \
            .assign(stages_group = lambda x: pd.qcut(x[group_column], 
                q=[0,0.08,0.18,0.45,0.65,0.85,0.95,1], 
                labels=['stg05', 'stg15', 'stg20', 'stg25', 'stg35', 'stg40', 'stg50']
                        )) \
            .drop('number_of_stages', axis = 1)

        group_column = 'stages_group'
        df = df[[x_column, y_column, group_column, id_column]]

    if bins == 'horizontal_length_bins':
        df = df \
            .query(f"{group_column} == {group_column}") \
            .assign(hor_length_group = lambda x: pd.qcut(x[group_column], 
                q=[0,0.02,0.09,0.14,0.5,0.75,0.975,1], 
            labels=['hz500', 'hz1000', 'hz1300', 'hz1500', 'hz2000', 'hz2500', 'hz3000']
                        )) \
            .drop('horizontal_length', axis = 1)

        group_column = 'hor_length_group'
        df = df[[x_column, y_column, group_column, id_column]]

    if bins == 'stage_spacing_bins':
        df = df \
            .query(f"{group_column} == {group_column}") \
            .assign(spacing_group = lambda x: pd.qcut(x[group_column], 
                q=[0,0.025,0.17,0.37,0.96,1.0], 
            labels=['stg_spc_050', 'stg_spc_060', 'stg_spc_070', 'stg_spc_080', 'stg_spc_100']
                        )) \
            .drop('stage_spacing', axis = 1)

        group_column = 'spacing_group'
        df = df[[x_column, y_column, group_column, id_column]]

    if bins == 'prop_fluid_bins':
        df = df \
            .query(f"{group_column} == {group_column}") \
            .assign(prop_fluid_group = lambda x: pd.qcut(x[group_column], 
                q=[0,0.09,0.45,0.75,0.94,1.0], 
            labels=['prop_fluid_1.1', 'prop_fluid_1.3', 'prop_fluid_1.6', 'prop_fluid_2.0', 'prop_fluid_2.2']
                        )) \
            .drop('proppant_fluid_ratio_lbm_gal', axis = 1)

        group_column = 'prop_fluid_group'
        df = df[[x_column, y_column, group_column, id_column]]

    if bins == 'prop_int_bins':
        df = df \
            .query(f"{group_column} == {group_column}") \
            .assign(prop_int_group = lambda x: pd.qcut(x[group_column], 
                q=[0,0.21,0.65,0.93,0.97,1.0], 
            labels=['prop_int_1600', 'prop_int_2000', 'prop_int_2400', 'prop_int_2700', 'prop_int_3700']
                        )) \
            .drop('proppant_intensity_lbm_ft', axis = 1)

        group_column = 'prop_int_group'
        df = df[[x_column, y_column, group_column, id_column]]

    if bins == 'fluid_int_bins':
        df = df \
            .query(f"{group_column} == {group_column}") \
            .assign(fluid_int_group = lambda x: pd.qcut(x[group_column], 
                q=[0,0.13,0.6,0.91,0.9625,1.0], 
            labels=['fluid_int_20', 'fluid_int_30', 'fluid_int_40', 'fluid_int_50', 'fluid_int_60']
                        )) \
            .drop('fluid_intensity_bbl_ft', axis = 1)

        group_column = 'fluid_int_group'
        df = df[[x_column, y_column, group_column, id_column]]

    # Grouping variable as category
    df[group_column] = df[group_column].astype('category')
    
    # Remove unused categories
    remove_unused_categories(df)

    # Rename columns
    x_column, y_column, group_column, id_column = get_col_names(df.columns)
    df.columns = [x_column, y_column, group_column, id_column]

    # Defining Labs
    if title == None:
        title = f"Plot of {y_column} vs. {x_column} by {group_column}"
    
    if x_label == None:
        x_label = x_column

    if y_label == None:
        y_label = y_column

    # Visualize
    import statsmodels.api as sm

    fig = px.scatter(
            df, 
            x=x_column, y=y_column,
            color=group_column, 
            size = y_column,
            size_max=20,
            opacity=0.5,
            trendline=trendline,
            trendline_scope=trend,
            labels = {
                x_column : x_label,
                y_column : y_label
            },
            title = title,
            #size='petal_length', 
            hover_data=[id_column]
            )

    fig.update_traces(marker_line_width=0.5, 
                        marker_line_color='white')

    return fig

#scatter_agg - 3 plots
@pf.register_dataframe_method
def scatter_agg(
    data, x_column, y_column, group_column,
    bins = None,
    title = None,
    x_label = None,
    y_label = None
    ):

    # Filter by well type and produced fluid
    df = data[[x_column, y_column, group_column]]
    df = df \
        .query(f"{x_column} == {x_column}") \
        .query(f"{y_column} == {y_column}")

    if bins == 'stages_bins':
        df = df \
            .query(f"{group_column} == {group_column}") \
            .assign(stages_group = lambda x: pd.qcut(x[group_column], 
                q=[0,0.08,0.18,0.45,0.65,0.85,0.95,1], 
                labels=['stg05', 'stg15', 'stg20', 'stg25', 'stg35', 'stg40', 'stg50']
                        )) \
            .drop('number_of_stages', axis = 1)

        group_column = 'stages_group'
        df = df[[x_column, y_column, group_column]]

    if bins == 'horizontal_length_bins':
        df = df \
            .query(f"{group_column} == {group_column}") \
            .assign(hor_length_group = lambda x: pd.qcut(x[group_column], 
                q=[0,0.02,0.09,0.14,0.5,0.75,0.975,1], 
            labels=['hz500', 'hz1000', 'hz1300', 'hz1500', 'hz2000', 'hz2500', 'hz3000']
                        )) \
            .drop('horizontal_length', axis = 1)

        group_column = 'hor_length_group'
        df = df[[x_column, y_column, group_column]]

    # Grouping variable as category
    df[group_column] = df[group_column].astype('category')
    
    # Remove unused categories
    remove_unused_categories(df)

    df = df \
        .groupby(group_column) \
        .agg({
            x_column : ['mean'],
            y_column : ['mean']
        }) \
        .reset_index()

    df = df.set_axis(
        ["_".join(col).rstrip("_") for col in df.columns.tolist()],
        axis = 1)

    # Rename columns
    group_column, x_column, y_column = get_col_names(df.columns)
    df.columns = [group_column, x_column, y_column]

    # Defining Labs
    if title == None:
        title = f"Plot of {y_column} vs. {x_column} by {group_column}"
    
    if x_label == None:
        x_label = x_column

    if y_label == None:
        y_label = y_column

    # Visualize

    fig = px.scatter(
            df, 
            x=x_column, y=y_column,
            color=group_column, 
            size = y_column,
            #trendline="ols", trendline_scope="overall",
            labels = {
                x_column : x_label,
                y_column : y_label
            },
            title = title
            #hover_data=['petal_width']
            )

    return fig

# SCATTER AND LINE PLOT ----

#scatter_line_agg - 2 plots
@pf.register_dataframe_method
def scatter_line_agg(
    data, x_column, y_column, group_column, agg_column,
    title = None,
    x_label = None,
    y_label = None
    ):

    # Filter by well type and produced fluid
    df = data[[x_column, y_column, 
            group_column, agg_column]]

    df = df \
        .groupby(group_column) \
        .tail(6)

    if agg_column == 'campaign':
        df[agg_column] = df[agg_column].astype('category')     

    # Rename columns
    x_column, y_column, group_column, agg_column = get_col_names(df.columns)
    df.columns = [x_column, y_column, group_column, agg_column]

    # Defining Labs
    if title == None:
        title = f"Plot of {y_column} vs. {x_column}"
    
    if x_label == None:
        x_label = x_column

    if y_label == None:
        y_label = y_column

    # Visualize

    fig = px.line(
            df, 
            x=x_column, y=y_column,
            line_group=group_column,
            color = agg_column,
            #symbol = group_column, 
            labels = {
                x_column : x_label,
                y_column : y_label
            },
            title = title,
            hover_data=[group_column]
            )

    fig.update_traces(marker_size=6)
    fig.update_traces(mode = 'markers+lines')
    fig.update_layout(showlegend=True)

    return fig

# HISTOGRAM ----
#hist_no_agg - 7 plots
@pf.register_dataframe_method
def hist_no_agg(
    data, x_column, 
    well_type = 'Horizontal',
    produced_fluid = 'Oil',
    nbins=20,
    title = None,
    x_label = None,
    y_label = None
    ):

    # Filter by well type and produced fluid
    df = data[['well_type', 'produced_fluid', x_column]]
    df = df \
        .query(f"well_type == '{well_type}'") \
        .query(f"produced_fluid == '{produced_fluid}'") \
        .query(f"{x_column} == {x_column}") \
        .drop(['well_type', 'produced_fluid'], axis = 1)

    # Rename columns
    x_column = get_col_names(df.columns)[0]
    df.columns = [x_column]

    # Defining Labs
    if title == None:
        title = f"Histogram of {x_column}"
    
    if x_label == None:
        x_label = x_column

    if y_label == None:
        y_label = 'Count'

    # Visualize

    fig = px.histogram(df, 
            x=x_column, 
            nbins=nbins,
            color_discrete_sequence=['blue'],
            labels = {
                x_column : x_label,
            },
            title = title)

    return fig

# COLUMN PLOT ----

#column_date_agg_no_group - 5 plots
@pf.register_dataframe_method
def column_date_agg_no_group(
    data, date_column, agg_column,
    well_type = None,
    produced_fluid = None,
    rule = 'Q',
    kind = 'timestamp',
    agg_func = np.sum,
    title = None,
    x_label = None,
    y_label = None,
    show_scale = False,
    ):

    if (well_type == 'Horizontal') & (produced_fluid == 'Oil'):
        df = data[['well_type', 'produced_fluid', date_column, agg_column]]

        # Filter by well type and produced fluid
        df = df \
            .query(f"well_type == '{well_type}'") \
            .query(f"produced_fluid == '{produced_fluid}'") \
            .query(f"{agg_column} == {agg_column}") \
            .drop(['well_type', 'produced_fluid'], axis = 1)
    else:
        df = data[[date_column, agg_column]]

    df = df \
        .set_index(date_column) \
        .resample(rule = rule, kind = kind) \
        .agg({
            agg_column : agg_func
        }) \
        .reset_index()

    # Renaming Columns
    date_column, agg_column = get_col_names(df.columns)
    df.columns = [date_column, agg_column]

    # Defining Labs
    if title == None:
        title = f"Plot of {agg_column} vs. {date_column}"
    
    if x_label == None:
        x_label = date_column

    if y_label == None:
        y_label = agg_column

    # Visualize

    fig = px.bar(df, 
            x=date_column,  
            y=agg_column,
            color=agg_column,
            color_continuous_scale='viridis',
            labels = {
                date_column : x_label,
            },
            title=title
            )

    fig.update_layout(coloraxis_showscale=show_scale)
 
    return fig

#column_date_agg - 7 plots
@pf.register_dataframe_method
def column_date_agg(
    data, date_column, id_column, group_column,
    rule = 'AS',
    kind = 'timestamp',
    agg_func = pd.Series.nunique,
    title = None,
    x_label = None,
    y_label = None
    ):

    df = data[[date_column, id_column, group_column]]
    
    df = df \
        .set_index(date_column) \
        .groupby(group_column) \
        .resample(rule = rule, kind = kind) \
        .agg({
            id_column : agg_func
        }) \
        .reset_index()

    # Rename columns
    group_column, date_column, id_agg_column = get_col_names(df.columns)
    df.columns = [group_column, date_column, id_agg_column]

    # Defining Labs
    if title == None:
        title = f"Plot of {id_agg_column} vs. {date_column} by {group_column}"
    
    if x_label == None:
        x_label = date_column

    if y_label == None:
        y_label = id_agg_column

    # Visualize

    fig = px.bar(df, 
            x=date_column,  
            y=id_agg_column,
            color=group_column,
            #color_discrete_sequence='viridis',
            labels = {
                date_column : x_label,
                id_agg_column : y_label,
            },
            title=title
            )

    return fig

#column_agg - 2 plots
@pf.register_dataframe_method
def column_agg(
    data, id_column, group_column,
    well_type = 'Horizontal',
    agg_func = 'count',
    title = None,
    x_label = None,
    y_label = None, 
    show_scale = False,
    ):

    df = data[['well_type', id_column, group_column]]
    df = df \
        .query(f"well_type == '{well_type}'") \
        .drop('well_type', axis = 1)
    
    df = df \
        .groupby(group_column) \
        .agg({
            id_column : [agg_func]
        }) \
        .reset_index()

    df = df \
        .set_axis(
        ["_".join(col).rstrip("_") for col in df.columns.tolist()],
        axis = 1)

    # Rename columns
    group_column, id_agg_column = get_col_names(df.columns)
    df.columns = [group_column, id_agg_column]

    df = df \
            .sort_values(id_agg_column) \
            .assign(
                group_cat = lambda x: cat_reorder(x[group_column], 
                x[id_agg_column], ascending=True)
            ) \
            .drop(group_column, axis = 1)

    df = df \
        .rename(columns={
            'group_cat' : group_column
        })

    df[group_column] = df[group_column].astype('category')

    df = df[df[id_agg_column] > 0]

    remove_unused_categories(df)

    if len(df[group_column]) > 20:
        df = df.tail(20)

    # Defining Labs
    if title == None:
        title = f"Plot of {id_agg_column} by {group_column}"
    
    if x_label == None:
        x_label = group_column

    if y_label == None:
        y_label = id_agg_column

    # Visualize

    fig = px.bar(df, 
            y=group_column,  
            x=id_agg_column,
            color=id_agg_column,
            color_continuous_scale='viridis',
            labels = {
                group_column : x_label,
                id_agg_column : y_label,
            },
            title=title
            )

    fig.update_layout(coloraxis_showscale=show_scale)

    return fig

#column_ranking - 2 plots
@pf.register_dataframe_method
def column_ranking(
    data, y_column, group_column, 
    well_type = 'Horizontal',
    produced_fluid = 'Oil',
    title = None,
    x_label = None,
    y_label = None,
    select_largest = True,
    n_largest = 20,
    sort_category = False,
    flip_coord = False,
    show_scale = False,
    ):

    # Filter by well type and produced fluid
    df = data[['well_type', 'produced_fluid', y_column, group_column]]
    df = df \
        .query(f"well_type == '{well_type}'") \
        .query(f"produced_fluid == '{produced_fluid}'") \
        .query(f"{y_column} == {y_column}") \
        .drop(['well_type', 'produced_fluid'], axis = 1)

    remove_unused_categories(df)

    # Select n-largest
    if select_largest:
        df = df \
            .nlargest(n=n_largest, columns = y_column)

    # Sort category
    if sort_category:
        df = df \
            .sort_values(y_column) \
            .assign(
                sorted_column = lambda x: cat_reorder(x[group_column], 
                x[y_column], ascending=True)) \
            .drop(group_column, axis = 1)

        df = df \
            .rename(columns={
                'sorted_column' : group_column
            })

    # Rename columns
    y_column, group_column = get_col_names(df.columns)
    df.columns = [y_column, group_column]

    df[group_column] = df[group_column].astype('category')

    # Defining Labs
    if title == None:
        title = f"Plot of {y_column} by {group_column}"
    
    if x_label == None:
        x_label = group_column

    if y_label == None:
        y_label = y_column

    # Visualize

    if not flip_coord:

        fig = px.bar(df, 
                x=group_column,  
                y=y_column,
                color=y_column,
                color_continuous_scale='viridis',
                labels = {
                    group_column : x_label,
                    y_column : y_label,
                },
                title=title
                )
        if sort_category:
            fig.update_xaxes(categoryorder='total ascending')

    else:
        fig = px.bar(df, 
                y=group_column,  
                x=y_column,
                color=y_column,
                color_continuous_scale='viridis',
                labels = {
                    group_column : x_label,
                    y_column : y_label,
                },
                title=title
                )
        if sort_category:
            fig.update_yaxes(categoryorder='total ascending')

    fig.update_layout(font=dict(size=10))
    fig.update_layout(coloraxis_showscale=show_scale)
    
    return fig

# BOXPLOT

#boxplot_no_agg - 22 plots
@pf.register_dataframe_method
def boxplot_no_agg(
    data, y_column, group_column, 
    well_type = 'Horizontal',
    produced_fluid = 'Oil',
    bins = None,
    title = None,
    x_label = None,
    y_label = None,
    sort_category = False,
    cat_order = None,
    flip_coord = False
    ):

    # Filter by well type and produced fluid
    df = data[['well_type', 'produced_fluid', y_column, group_column]]
    df = df \
        .query(f"well_type == '{well_type}'") \
        .query(f"produced_fluid == '{produced_fluid}'") \
        .query(f"{y_column} == {y_column}") \
        .drop(['well_type', 'produced_fluid'], axis = 1)

    if bins == 'stage_spacing_bins':
        df = df \
            .query(f"{group_column} == {group_column}") \
            .assign(spacing_group = lambda x: pd.qcut(x[group_column], 
                q=[0,0.025,0.17,0.37,0.96,1.0], 
            labels=['stg_spc_050', 'stg_spc_060', 'stg_spc_070', 'stg_spc_080', 'stg_spc_100']
                        )) \
            .drop('stage_spacing', axis = 1)

        cat_order = ['stg_spc_050', 'stg_spc_060', 'stg_spc_070', 'stg_spc_080', 'stg_spc_100']

        group_column = 'spacing_group'
        df = df[[y_column, group_column]]

    if bins == 'prop_fluid_bins':
        df = df \
            .query(f"{group_column} == {group_column}") \
            .assign(prop_fluid_group = lambda x: pd.qcut(x[group_column], 
                q=[0,0.09,0.45,0.75,0.94,1.0], 
            labels=['prop_fluid_1.1', 'prop_fluid_1.3', 'prop_fluid_1.6', 'prop_fluid_2.0', 'prop_fluid_2.2']
                        )) \
            .drop('proppant_fluid_ratio_lbm_gal', axis = 1)

        cat_order = ['prop_fluid_1.1', 'prop_fluid_1.3', 'prop_fluid_1.6', 'prop_fluid_2.0', 'prop_fluid_2.2']

        group_column = 'prop_fluid_group'
        df = df[[y_column, group_column]]

    if bins == 'prop_int_bins':
        df = df \
            .query(f"{group_column} == {group_column}") \
            .assign(prop_int_group = lambda x: pd.qcut(x[group_column], 
                q=[0,0.21,0.65,0.93,0.97,1.0], 
            labels=['prop_int_1600', 'prop_int_2000', 'prop_int_2400', 'prop_int_2700', 'prop_int_3700']
                        )) \
            .drop('proppant_intensity_lbm_ft', axis = 1)

        cat_order = ['prop_int_1600', 'prop_int_2000', 'prop_int_2400', 'prop_int_2700', 'prop_int_3700']

        group_column = 'prop_int_group'
        df = df[[y_column, group_column]]

    if bins == 'fluid_int_bins':
        df = df \
            .query(f"{group_column} == {group_column}") \
            .assign(fluid_int_group = lambda x: pd.qcut(x[group_column], 
                q=[0,0.13,0.6,0.91,0.9625,1.0], 
            labels=['fluid_int_20', 'fluid_int_30', 'fluid_int_40', 'fluid_int_50', 'fluid_int_60']
                        )) \
            .drop('fluid_intensity_bbl_ft', axis = 1)

        cat_order = ['fluid_int_20', 'fluid_int_30', 'fluid_int_40', 'fluid_int_50', 'fluid_int_60']

        group_column = 'fluid_int_group'
        df = df[[y_column, group_column]]

    remove_unused_categories(df)

    # Sort category
    if sort_category:
        df = df \
            .sort_values(y_column) \
            .assign(
                sorted_column = lambda x: cat_reorder(x[group_column], 
                x[y_column], ascending=True)) \
            .drop(group_column, axis = 1)

        df = df \
            .rename(columns={
                'sorted_column' : group_column
            })

    # Rename columns
    y_column, group_column = get_col_names(df.columns)
    df.columns = [y_column, group_column]

    df[group_column] = df[group_column].astype('category')

    # Defining Labs
    if title == None:
        title = f"Boxplot of {y_column} by {group_column}"
    
    if x_label == None:
        x_label = group_column

    if y_label == None:
        y_label = y_column

    # Visualize

    if not flip_coord:
        if cat_order == None:
            fig = px.box(df, 
                    x=group_column,  
                    y=y_column,
                    color=group_column,
                    #category_orders= {group_column : cat_order},
                    labels = {
                        group_column : x_label,
                        y_column : y_label,
                    },
                    title=title
                    )
        else:
            fig = px.box(df, 
                    x=group_column,  
                    y=y_column,
                    color=group_column,
                    category_orders= {group_column : cat_order},
                    labels = {
                        group_column : x_label,
                        y_column : y_label,
                    },
                    title=title
                    )

        if sort_category:
            fig.update_xaxes(categoryorder='total ascending')

    else:
        fig = px.box(df, 
                y=group_column,  
                x=y_column,
                color=group_column,
                orientation='h',
                labels = {
                    group_column : x_label,
                    y_column : y_label,
                },
                title=title
                )

        if sort_category:
            fig.update_yaxes(categoryorder='total ascending')

    fig.update_traces(showlegend=False)

    if group_column=='campaign':
        fig.update_xaxes(tick0=2012, dtick=1)

    return fig

# LINE PLOT

#line_plot_no_agg - 2 plots
@pf.register_dataframe_method
def line_plot_no_agg(
    data, date_column, agg_column,
    rule = 'M',
    kind = 'period',
    agg_func = np.sum,
    color = 'green',
    title = None,
    x_label = None,
    y_label = None
    ):
    df = data[[date_column, agg_column]]

    df = df \
        .set_index(date_column) \
        .resample(rule = rule, kind = kind) \
        .agg({agg_column : agg_func}) \
        .reset_index() \
        .assign(date_ts = lambda x: x[date_column].dt.to_timestamp()) \
        .drop(date_column, axis = 1)

    df = df \
        .rename(columns={
            'date_ts' : date_column
        })

     # Rename columns
    agg_column, date_column = get_col_names(df.columns)
    df.columns = [agg_column, date_column]

    # Defining Labs
    if title == None:
        title = f"Plot of {agg_column} by {date_column}"
    
    if x_label == None:
        x_label = date_column

    if y_label == None:
        y_label = agg_column

    # Visualize

    fig = px.line(df, 
                x=date_column,  
                y=agg_column,
                labels = {
                    date_column : x_label,
                    agg_column : y_label,
                },
                title=title
                )

    fig.update_traces(line_color=color)
    fig.update_xaxes(tick0='2012-01-01', dtick="M12")
        
    return fig

#line_plot_agg - 4 plots
@pf.register_dataframe_method
def line_plot_agg(
    data, date_column, agg_column, group_column,
    rule = 'M',
    kind = 'timestamp',
    agg_func = np.sum,
    log_plot = False,
    title = None,
    x_label = None,
    y_label = None
    ):

    # Filter by well type and produced fluid
    df = data[[date_column, agg_column, group_column]]

    df = df \
        .set_index(date_column) \
        .groupby(group_column) \
        .resample(rule = rule, kind = kind) \
        .agg({agg_column : agg_func}) \
        .reset_index()

    df[group_column] = df[group_column].astype('category')
    remove_unused_categories(df)

    # Rename columns
    group_column, date_column, agg_column = get_col_names(df.columns)
    df.columns = [group_column, date_column, agg_column]

    # Defining Labs
    if title == None:
        title = f"Plot of {agg_column} vs. {date_column} by {group_column}"
    
    if x_label == None:
        x_label = date_column

    if y_label == None:
        y_label = agg_column

    # Visualize

    fig = px.line(df, 
                x=date_column,  
                y=agg_column,
                color=group_column,
                labels = {
                    date_column : x_label,
                    agg_column : y_label,
                },
                title=title
                )
   
    if log_plot:
        fig.update_yaxes(type='log')

    return fig

# AREA

#area_plot_agg - 2 plots
@pf.register_dataframe_method
def area_plot_agg(
    data, date_column, agg_column, group_column,
    rule = 'M',
    kind = 'timestamp',
    agg_func = np.sum,
    cumsum = 'N',
    title = None,
    x_label = None,
    y_label = None
    ):
    df = data[[date_column, agg_column, group_column]]

    if cumsum == 'Y':
        df = df \
            .set_index(date_column) \
            .groupby(group_column) \
            .resample(rule = rule, kind = kind) \
            .agg({agg_column : agg_func}) \
            .cumsum() \
            .reset_index()
    else:  
        df = df \
                .set_index(date_column) \
                .groupby(group_column) \
                .resample(rule = rule, kind = kind) \
                .agg({agg_column : agg_func}) \
                .reset_index()

    # Rename columns
    group_column, date_column, agg_column = get_col_names(df.columns)
    df.columns = [group_column, date_column, agg_column]

    # Defining Labs
    if title == None:
        title = f"Plot of {agg_column} vs. {date_column} by {group_column}"
    
    if x_label == None:
        x_label = date_column

    if y_label == None:
        y_label = agg_column

    # Visualize

    fig = px.area(df, 
                x=date_column,  
                y=agg_column,
                color=group_column,
                line_group=group_column,
                labels = {
                    date_column : x_label,
                    agg_column : y_label,
                },
                title=title
                )
        
    return fig

# FACET

#facet_plot_agg - 4 plots
@pf.register_dataframe_method
def facet_plot_agg(
    data, x_column, agg_column, group_column,
    well_type = 'Horizontal',
    produced_fluid = 'Oil',
    title = None,
    x_label = None,
    y_label = None
    ):

    # Filter by well type and produced fluid
    df = data[['well_type', 'produced_fluid',
                x_column, agg_column, group_column]]

    df = df \
        .query(f"well_type == '{well_type}'") \
        .query(f"produced_fluid == '{produced_fluid}'") \
        .query(f"{x_column} == {x_column}") \
        .query(f"{agg_column} == {agg_column}") \
        .drop(['well_type', 'produced_fluid'], axis = 1)

    remove_unused_categories(df)

    # Rename columns
    x_column, agg_column, group_column = get_col_names(df.columns)
    df.columns = [x_column, agg_column, group_column]

    df[group_column] = df[group_column].astype('category')

    # Defining Labs
    if title == None:
        title = f"Facet of {agg_column} vs. {x_column} by {group_column}"
    
    if x_label == None:
        x_label = x_column

    if y_label == None:
        y_label = agg_column

    # Visualize

    fig = px.scatter(
            df, 
            x=x_column, y=agg_column,
            color=group_column, 
            #size = y_column,
            trendline="ols", trendline_scope="trace",
            facet_col = group_column,
            facet_col_wrap = 3,
            facet_col_spacing = 0.05,
            facet_row_spacing = 0.08,
            labels = {
                x_column : x_label,
                agg_column : y_label
            },
            title = title
            #hover_data=['petal_width']
            )

    fig.update_layout(showlegend=False)
    fig.update_xaxes(matches='x')
    fig.update_layout(font=dict(size=10))

    return fig

# LINE PLOT PRODUCTION RATE

#line_rate_plot_agg - 14 plots
@pf.register_dataframe_method
def line_rate_plot_agg(
    data, date_column, value_column, group_column, id_column,
    well_type = 'Horizontal',
    produced_fluid = 'Oil',
    plot_type = 'rate',
    normalized = False,
    norm_len = 2500,
    agg_func = np.mean,
    title = None,
    x_label = None,
    y_label = None
    ):

    # Filter by well type and produced fluid
    if not normalized:
        df = data[['well_type', 'produced_fluid',
                    date_column, value_column, group_column, id_column]]

        df = df \
            .query(f"well_type == '{well_type}'") \
            .query(f"produced_fluid == '{produced_fluid}'") \
            .drop(['well_type', 'produced_fluid'], axis = 1)

    else:
        df = data[['well_type', 'produced_fluid', 'horizontal_length',
                    date_column, value_column, group_column, id_column]]

        df = df \
            .query(f"well_type == '{well_type}'") \
            .query(f"produced_fluid == '{produced_fluid}'") \
            .query(f"horizontal_length == horizontal_length") \
            .drop(['well_type', 'produced_fluid'], axis = 1) 

    remove_unused_categories(df)

    grouped = df[[id_column,date_column]].groupby(id_column)
    df['diff_months'] = grouped.transform(d_months, df)

    df = df \
            .drop(date_column, axis = 1) 
    
    date_column = 'diff_months'

    if plot_type == 'rate':
        if not normalized:
            df = df \
                .groupby([group_column,date_column]) \
                .apply(lambda x: agg_func(x[value_column])) \
                .reset_index() \
                .rename(columns={0:'avg_volume'}) \
                .assign(avg_rate = lambda x: x.avg_volume / 30.43) \
                .drop('avg_volume', axis = 1) 
        else:
            df = df \
                .groupby([group_column,date_column]) \
                .apply(lambda x: agg_func((x[value_column]/x['horizontal_length'])*norm_len)) \
                .reset_index() \
                .rename(columns={0:'avg_volume'}) \
                .assign(avg_rate = lambda x: x.avg_volume / 30.43) \
                .drop(['avg_volume'], axis = 1) 

        value_column = 'avg_rate'

    if plot_type == 'volume':
        if not normalized:
            df = df \
                .groupby([group_column,date_column]) \
                .apply(lambda x: agg_func(x[value_column])) \
                .reset_index() \
                .rename(columns={0:'avg_volume'})

            df['avg_cum_volume'] = df.groupby([group_column]) \
                                        .avg_volume \
                                        .cumsum()
                                        
            df = df.drop('avg_volume', axis = 1)
        else:
            df = df \
                .groupby([group_column,date_column]) \
                .apply(lambda x: agg_func((x[value_column]/x['horizontal_length'])*norm_len)) \
                .reset_index() \
                .rename(columns={0:'avg_volume'})

            df['avg_cum_volume'] = df.groupby([group_column]) \
                                        .avg_volume \
                                        .cumsum()
                                        
            df = df.drop(['avg_volume'], axis = 1)
        
        value_column = 'avg_cum_volume'

    if group_column == 'campaign':
        
        cat_list = ['2015', '2016', '2017', '2018', '2019', '2020', '2021']
        cat_list =  [int(l) for l in cat_list]

        for item in cat_list:

            df = df[~((df[group_column] == item) & (df[date_column]>((2021-item)*12+6)))]

    # elif group_column == 'operator':

    #     cat_list = ['VISTA', 'SHELL', 'YPF', 'WINTERSHALL']

    #     for item in cat_list:

    #         df = df[~((df[group_column] == item) & (df[date_column]>30))]

    # elif group_column == 'area':

    #     cat_list = ['AGUADA_FEDERAL','BAJADA_DEL_PALO_OESTE',
    #     'BANDURRIA_CENTRO','BANDURRIA_SUR',
    #     'COIRON_AMARGO_SUR_ESTE','COIRON_AMARGO_SUR_OESTE',
    #     'CRUZ_DE_LORENA','LA_AMARGA_CHICA','LINDERO_ATRAVESADO',
    #     'LOMA_CAMPANA','SIERRAS_BLANCAS']

    #     for item in cat_list:

    #         df = df[~((df[group_column] == item) & (df[date_column]>30))]

    # Rename columns
    group_column, date_column, value_column = get_col_names(df.columns)
    df.columns = [group_column, date_column, value_column]

    df[group_column] = df[group_column].astype('category')

    # Defining Labs
    if title == None:
        title = f"Plot of {value_column} vs. {date_column} by {group_column}"
    
    if x_label == None:
        x_label = date_column

    if y_label == None:
        y_label = value_column

    # Visualization
    fig = px.line(df, 
                    x=date_column,  
                    y=value_column,
                    color=group_column,
                    labels = {
                    date_column : x_label,
                    value_column : y_label
                            },
                    title = title
                    )

    #if plot_type == 'rate':
    #    fig.add_scatter(x=af_type_curve['prod_month'], y=af_type_curve['qo_bbl_d'], 
    #        mode='lines', name = 'af_type_curve',
    #        line = dict(color='black', width=1, dash='dot'))
    #else:
    #    fig.add_scatter(x=af_type_curve['prod_month'], y=af_type_curve['qo_bbl'], 
    #            mode='lines', name = 'af_type_curve',
    #            line = dict(color='black', width=1, dash='dot'))

    return fig

#line_rate_plot_no_agg- 2 plots
@pf.register_dataframe_method
def line_rate_plot_no_agg(
    data, date_column, value_column, id_column,
    well_type = 'Horizontal',
    produced_fluid = 'Oil',
    plot_type = 'rate',
    normalized = False,
    norm_len = 2500,
    agg_func = np.mean,
    title = None,
    x_label = None,
    y_label = None
    ):

    # Filter by well type and produced fluid
    if not normalized:
        df = data[['well_type', 'produced_fluid',
                    date_column, value_column, id_column]]

        df = df \
            .query(f"well_type == '{well_type}'") \
            .query(f"produced_fluid == '{produced_fluid}'") \
            .drop(['well_type', 'produced_fluid'], axis = 1)

    else:
        df = data[['well_type', 'produced_fluid', 'horizontal_length',
                    date_column, value_column, id_column]]

        df = df \
            .query(f"well_type == '{well_type}'") \
            .query(f"produced_fluid == '{produced_fluid}'") \
            .query(f"horizontal_length == horizontal_length") \
            .drop(['well_type', 'produced_fluid'], axis = 1) 

    remove_unused_categories(df)

    grouped = df[[id_column,date_column]].groupby(id_column)
    df['diff_months'] = grouped.transform(d_months, df)

    df = df \
            .drop(date_column, axis = 1) 
    
    date_column = 'diff_months'

    if plot_type == 'rate':
        if not normalized:
            df = df \
                .groupby([date_column]) \
                .apply(lambda x: agg_func(x[value_column])) \
                .reset_index() \
                .rename(columns={0:'avg_volume'}) \
                .assign(avg_rate = lambda x: x.avg_volume / 30.43) \
                .drop('avg_volume', axis = 1) 
        else:
            df = df \
                .groupby([date_column]) \
                .apply(lambda x: agg_func((x[value_column]/x['horizontal_length'])*norm_len)) \
                .reset_index() \
                .rename(columns={0:'avg_volume'}) \
                .assign(avg_rate = lambda x: x.avg_volume / 30.43) \
                .drop(['avg_volume'], axis = 1) 

        value_column = 'avg_rate'

    if plot_type == 'volume':
        if not normalized:
            df = df \
                .groupby([date_column]) \
                .apply(lambda x: agg_func(x[value_column])) \
                .reset_index() \
                .rename(columns={0:'avg_volume'})

            df['avg_cum_volume'] = df\
                                    .avg_volume \
                                    .cumsum()
                                        
            df = df.drop('avg_volume', axis = 1)
        else:
            df = df \
                .groupby([date_column]) \
                .apply(lambda x: agg_func((x[value_column]/x['horizontal_length'])*norm_len)) \
                .reset_index() \
                .rename(columns={0:'avg_volume'})

            df['avg_cum_volume'] = df \
                                    .avg_volume \
                                    .cumsum()
                                        
            df = df.drop(['avg_volume'], axis = 1)
        
        value_column = 'avg_cum_volume'

    df = df \
        .query(f"({date_column} <= 25)"
                )

    # Rename columns
    date_column, value_column = get_col_names(df.columns)
    df.columns = [date_column, value_column]

    # Defining Labs
    if title == None:
        title = f"Plot of {value_column} vs. {date_column}"
    
    if x_label == None:
        x_label = date_column

    if y_label == None:
        y_label = value_column

    # Visualization
    fig = px.line(df, 
                    x=date_column,  
                    y=value_column,
                    #color=color_column,
                    labels = {
                    date_column : x_label,
                    value_column : y_label
                            },
                    title = title
                    )

    #if plot_type == 'rate':
    #    fig.add_scatter(x=af_type_curve['prod_month'], y=af_type_curve['qo_bbl_d'], 
    #        mode='lines', name = 'af_type_curve',
    #        line = dict(color='black', width=1, dash='dot'))
    #else:
    #    fig.add_scatter(x=af_type_curve['prod_month'], y=af_type_curve['qo_bbl'], 
    #            mode='lines', name = 'af_type_curve',
    #            line = dict(color='black', width=1, dash='dot'))

    return fig

#line_well_prod_plot_no_agg - 18 plots
@pf.register_dataframe_method
def line_well_prod_plot_no_agg(
    data, 
    date_column, value_column, group_column, id_column = None,
    var_dir = None,
    cat_list = None,
    plot_type = 'rate',
    norm_len = 2500,
    normalized = False,
    title = None,
    x_label = None,
    y_label = None,
    ):
    
    if var_dir != None:
        df_list = []

        for k,v in var_dir.items():
            df_key = data[data[id_column] == k]
            df_key['landing'] = v
            df_list.append(df_key)

        data = pd.concat(df_list)
        data['landing'] = data['landing'].astype('category')

    if var_dir != None:
        cat_list = cat_list
        df_list = []

        for item in cat_list:
            df_cat = data[data[group_column] == item]
            df_list.append(df_cat)
            
        data = pd.concat(df_list)
    
    # Convert from days to month
    if id_column == None:
        grouped = data[[group_column,date_column]].groupby(group_column)
        data['diff_months'] = grouped.transform(d_months, data)

        data = data \
                .drop(date_column, axis = 1) 
    
        date_column = 'diff_months'

    else:
        grouped = data[[id_column,date_column]].groupby(id_column)
        data['diff_months'] = grouped.transform(d_months, data)

        data = data \
                .drop(date_column, axis = 1) 
    
        date_column = 'diff_months'

    # Select columns
    if not normalized:
        if id_column == None:
            df = data[[date_column, value_column, group_column]] 
        else:
            df = data[[date_column, value_column, group_column, id_column]]   

    else:
        if plot_type == 'rate':

            if id_column == None:
                df = data[['horizontal_length', date_column, value_column, group_column]] \
                    .assign(norm_oil_month_bpd = lambda x: (x[value_column]/x['horizontal_length'])*norm_len) \
                    .drop('horizontal_length', axis=1)
                value_column = 'norm_oil_month_bpd'
            else:
                df = data[['horizontal_length', date_column, value_column, group_column, id_column]] \
                    .assign(norm_oil_month_bpd = lambda x: (x[value_column]/x['horizontal_length'])*norm_len) \
                    .drop('horizontal_length', axis=1)
                value_column = 'norm_oil_month_bpd'

        if plot_type == 'volume':

            if id_column == None:
                df = data[['horizontal_length', date_column, value_column, group_column]] \
                    .assign(norm_cum_oil_bbl = lambda x: (x[value_column]/x['horizontal_length'])*norm_len) \
                    .drop('horizontal_length', axis=1)
                value_column = 'norm_cum_oil_bbl'
            else:
                df = data[['horizontal_length', date_column, value_column, group_column, id_column]] \
                    .assign(norm_cum_oil_bbl = lambda x: (x[value_column]/x['horizontal_length'])*norm_len) \
                    .drop('horizontal_length', axis=1)
                value_column = 'norm_cum_oil_bbl'

        if id_column == None:
            columns_list = [date_column,value_column, group_column]
            df = df[columns_list]
        else:
            columns_list = [date_column,value_column, group_column, id_column]
            df = df[columns_list]

    # Rename columns
    if id_column == None:
        date_column,  value_column, group_column = get_col_names(df.columns)
        df.columns = [date_column, value_column, group_column]
    else:
        date_column,  value_column, group_column, id_column = get_col_names(df.columns)
        df.columns = [date_column, value_column, group_column, id_column]

    # Defining Labs
    if title == None:
        title = f"Plot of {value_column} vs. {date_column} by {group_column}"
    
    if x_label == None:
        x_label = date_column

    if y_label == None:
        y_label = value_column

    # Visualization
    if id_column == None:
        fig = px.line(df, 
                        x=date_column,  
                        y=value_column,
                        line_group=group_column,
                        color=group_column,
                        labels = {
                        date_column : x_label,
                        value_column : y_label
                                },
                        title = title
                        )
    else:
        fig = px.line(df, 
                        x=date_column,  
                        y=value_column,
                        line_group=id_column,
                        color=group_column,
                        labels = {
                        date_column : x_label,
                        value_column : y_label
                                },
                        title = title
                        )

    #if plot_type == 'rate':
    #    fig.add_scatter(x=af_type_curve['prod_month'], y=af_type_curve['qo_bbl_d'], 
    #        mode='lines', name = 'af_type_curve',
    #        line = dict(color='black', width=1, dash='dot'))
    #else:
    #    fig.add_scatter(x=af_type_curve['prod_month'], y=af_type_curve['qo_bbl'], 
    #            mode='lines', name = 'af_type_curve',
    #            line = dict(color='black', width=1, dash='dot'))
    
    return fig
