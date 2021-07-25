import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from numebot.data.data_constants import NC
from numebot.env import NUMERAI_DATA_FOLDER, MODEL_CONFIGS_PATH
from numebot.monitoring.dashboard.dashboard_plots import plot_daily_correlations, plot_final_correlations, plot_final_correlations_mean
from numebot.round_manager import RoundManager
from numebot.secret import PUBLIC_ID, SECRET_KEY


rm = RoundManager(
    numerai_folder=NUMERAI_DATA_FOLDER,
    model_configs_path=MODEL_CONFIGS_PATH,
    public_id=PUBLIC_ID,
    secret_key=SECRET_KEY,
    testing=True,
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

content = html.Div([html.H2('Numerai dashboard: Model\'s correlations over time.'),
                    dcc.Graph(id="correlation-evolution"),
                    dcc.Graph(id="correlation-final"),
                    dcc.Graph(id="correlation-mean"),],
                   className="col-lg-10",
                   style=CONTENT_STYLE)

app.layout = html.Div([sidebar, 
                       content],
                      className="row",)

@app.callback(Output("correlation-evolution", "figure"), 
              Input("checklist_rounds", "value"),
              Input("checklist_models", "value"))
def update_line_chart(rounds, model_names):
    fig = plot_daily_correlations(full_df, rounds, model_names)    
    return fig


@app.callback(Output("correlation-final", "figure"), 
              Input("checklist_rounds", "value"), 
              Input("checklist_models", "value"))
def update_line_chart(rounds, model_names):
    fig = plot_final_correlations(full_df, rounds, model_names)
    return fig


@app.callback(Output("correlation-mean", "figure"), 
              Input("checklist_rounds", "value"), 
              Input("checklist_models", "value"))
def update_line_chart(rounds, model_names):
    fig = plot_final_correlations_mean(full_df, rounds, model_names)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, host= '0.0.0.0')
