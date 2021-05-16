import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

from numebot.data.data_constants import NC
from numebot.env import NUMERAI_DATA_FOLDER, MODEL_CONFIGS_PATH
from numebot.monitoring.dashboard.dashboard_functions import get_color_dict, get_shape_dict
from numebot.round_manager import RoundManager
from numebot.secret import PUBLIC_ID, SECRET_KEY


rm = RoundManager(
    numerai_folder=NUMERAI_DATA_FOLDER,
    model_configs_path=MODEL_CONFIGS_PATH,
    public_id=PUBLIC_ID,
    secret_key=SECRET_KEY
)

full_df = rm.mm.load_round_details_csv()
model_names = full_df[NC.username].unique()

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# Styling the sidebar from https://morioh.com/p/68e6c284a59c
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# Padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H3(children='Models to show.'),
        dcc.Checklist(
            id="checklist_models",
            options=[{"label": x, "value": x} for x in full_df[NC.username].unique()],
            value=full_df[NC.username].unique(),
            #labelStyle={'display': 'inline-block'}
        ),
        html.H3(children='Rounds to show.'),
        dcc.Checklist(
            id="checklist_rounds",
            options=[{"label": x, "value": x} for x in full_df[NC.round].unique()],
            value=full_df[NC.round].unique(),
            #labelStyle={'display': 'inline-block'}
        ),
    ], 
    className="col-lg-2 left-panel",
    style=SIDEBAR_STYLE#{'width':'20%'}
)

content = html.Div(
    [
        html.H2('Numerai dashboard: Model\'s correlations over time.'),
        dcc.Graph(id="correlation-evolution"),
        dcc.Graph(id="correlation-final"),
    ],
    className="col-lg-10",
    style=CONTENT_STYLE
)

app.layout = html.Div(
    [
        sidebar,
        content
    ],
    className="row",
)


@app.callback(Output("correlation-evolution", "figure"), 
              Input("checklist_rounds", "value"),
              Input("checklist_models", "value"))
def update_line_chart(rounds, model_names):
    
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


@app.callback(Output("correlation-final", "figure"), 
              Input("checklist_rounds", "value"), 
              Input("checklist_models", "value"))
def update_line_chart(rounds, model_names):
    
    # Filter DataFrame keeping the selected models and rounds to plot, and for this plot only
    # the last value for each model and round.
    final_values_df = full_df.sort_values(NC.date).copy()
    final_values_df = final_values_df.drop_duplicates([NC.model_name, NC.round], keep='last') 
    final_values_df = final_values_df[final_values_df[NC.round].isin(rounds)]

    colors_dict = get_color_dict(list_of_items=final_values_df[NC.model_name].unique())
    
    fig = go.Figure()
    for model_name, model_df in final_values_df.groupby(NC.username):
        if model_name not in model_names:
            continue

        fig.add_trace(go.Scatter(x=model_df[NC.date], 
                                 y=model_df[NC.correlation],
                                 line=dict(color=colors_dict[model_name]),
                                 name=f'{model_name}'))
    
    fig.add_hline(y=0.0)
    fig.update_layout(title='Final correlation of each model for each round',
                      xaxis_title='Date',
                      yaxis_title='Correlation')

    return fig

app.run_server(debug=True, host= '0.0.0.0')
