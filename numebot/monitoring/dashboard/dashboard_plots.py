import plotly.graph_objects as go

from numebot.data.data_constants import NC
from numebot.monitoring.dashboard.dashboard_functions import get_color_dict, get_shape_dict


def plot_daily_correlations(full_df, rounds, model_names):

    # I get the dicts including all rounds and models so colors and shapes will be consistent after 
    # filtering.
    shape_dict = get_shape_dict(list_of_items=full_df[NC.round].unique())
    colors_dict = get_color_dict(list_of_items=full_df[NC.model_name].unique())

    fig = go.Figure()
    for model_name, model_df in full_df.groupby(NC.username):
        if model_name not in model_names:
            continue

        for round_number, round_df in model_df.groupby(NC.round):
            if round_number not in rounds:
                continue
            
            fig.add_trace(go.Scatter(x=round_df[NC.date], 
                                     y=round_df[NC.correlation],
                                     line=dict(color=colors_dict[model_name],
                                               dash=shape_dict[round_number]),
                                     name=f'{model_name}-r{round_number}'))
    
    fig.add_hline(y=0.0)
    fig.update_layout(title='Correlation of each model and submission',
                      xaxis_title='Date',
                      yaxis_title='Correlation')

    return fig


def plot_final_correlations(full_df, rounds, model_names):
    # Filter DataFrame keeping the selected models and rounds to plot, and for this plot only
    # the last value for each model and round.
    colors_dict = get_color_dict(list_of_items=full_df[NC.model_name].unique())
    
    final_values_df = full_df.sort_values(NC.date).copy().reset_index(drop=True)
    final_values_df = final_values_df.drop_duplicates([NC.model_name, NC.round], keep='last') 
    final_values_df = final_values_df[final_values_df[NC.round].isin(rounds)]

    
    fig = go.Figure()
    for model_name, model_df in final_values_df.groupby(NC.username):
        if model_name not in model_names:
            continue
        
        model_df.sort_values(NC.round, inplace=True)
        fig.add_trace(go.Scatter(x=model_df[NC.round], 
                                 y=model_df[NC.correlation],
                                 line=dict(color=colors_dict[model_name]),
                                 name=f'{model_name}'))
    
    fig.add_hline(y=0.0)
    fig.update_layout(title='Final correlation of each model for each round',
                      xaxis_title='Round',
                      yaxis_title='Correlation')

    return fig


def plot_final_correlations_mean(full_df, rounds, model_names):
    # Filter DataFrame keeping the selected models and rounds to plot, and for this plot only
    # the last value for each model and round.
    colors_dict = get_color_dict(list_of_items=full_df[NC.model_name].unique())
    
    final_values_df = full_df.sort_values(NC.date).copy().reset_index(drop=True)
    final_values_df = final_values_df.drop_duplicates([NC.model_name, NC.round], keep='last') 
    final_values_df = final_values_df[final_values_df[NC.round].isin(rounds)]

    
    
    fig = go.Figure()
    for model_name, model_df in final_values_df.groupby(NC.username):
        if model_name not in model_names:
            continue
        
        n_samples = len(model_df)
        model_mean = model_df[NC.correlation].mean()

        model_df.sort_values(NC.round, inplace=True)
        fig.add_trace(go.Scatter(x=[n_samples], 
                                 y=[model_mean],
                                 line=dict(color=colors_dict[model_name]),
                                 mode='markers+text',
                                 name=f'{model_name}',
                                 text=model_name,
                                 textposition="top right"))
    
    fig.add_hline(y=0.0)
    fig.update_layout(title='Mean of the final correlations for each model',
                      xaxis_title='Number of rounds running',
                      yaxis_title='Correlation mean')

    return fig
