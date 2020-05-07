# -*- coding: utf-8 -*-
import json
import dash
import numpy as np
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import tracker
import app_view

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

height_left_figs = 300
height_right_figs = 175

app.layout = app_view.layout()

@app.callback([
    Output('init-viewport', 'className'),
    Output('Total-Cases', 'figure'),
    Output('Active-Cases', 'figure'),
    Output('Gamma', 'figure'),
    Output('Beta', 'figure'),
    Output('R-0', 'figure'),
    ], [Input('state', 'value')]
)
def display_state(input_state):
    if input_state is None:
        state = False
        input_state = 'IN'
    else:
        state = True

    data = tracker.data_analyser(input_state, False)

    total_cases = {
        'x': data.dates,
        'y': data.np_data[data.members['total_count'], :],
        'name': 'Total Cases',
        'type': 'line',
        'line':{'color':'#FF8B72'}
    }

    recovered_cases = {
        'x': data.dates,
        'y': data.np_data[data.members['total_count'], :] - data.np_data[data.members['active_cases'], :],
        'name': 'Recovered Cases',
        'type': 'line',
        'line':{'color':'green'}
    }

    active_cases = {
        'x': data.dates,
        'y': data.np_data[data.members['active_cases'], :],
        'name': 'Active Cases',
        'type': 'line',
        'line':{'color':'orangered'}
    }

    gamma = {
        'x': data.dates[data.offset_days:],
        'y': data.np_data[data.members['gamma'], :],
        'name': 'Gamma',
        'type': 'line',
        'line':{'color':'mediumspringgreen'}
    }

    beta = {
        'x': data.dates[data.offset_days:],
        'y': data.np_data[data.members['beta'], :],
        'name': 'Beta',
        'type': 'line',
        'line':{'color':'gold'}
    }

    r_0 = {
        'x': data.dates[data.offset_days:],
        'y': data.np_data[data.members['reproductive_number'], :],
        'name': 'Reproductive Number',
        'type': 'line',
        'line':{'color':'dodgerblue'}        
    }

    layout_left = {
        'showlegend': False,
        'margin': {'t':'20', 'b':'40'},
        'height': height_left_figs,
        'paper_bgcolor': 'rgba(255, 255, 255, 0.35)',
        'plot_bgcolor': 'rgba(255, 255, 255, 0.35)'
    }

    layout_right = {
        'margin': {'t':'5', 'b':'40'},
            'height': height_right_figs,
            'paper_bgcolor': 'rgba(255, 255, 255, 0.35)',
            'plot_bgcolor': 'rgba(255, 255, 255, 0.35)'
    }
    
    total_cases_fig = {
        'data':[total_cases],
        'layout': layout_left
    }

    active_cases_fig = {
        'data':[active_cases, recovered_cases],
        'layout': layout_left
    }

    gamma_fig = {
        'data':[gamma],
        'layout': layout_right
    }

    beta_fig = {
        'data':[beta],
        'layout': layout_right
    }

    reproductive_number_fig = {
        'data':[r_0],
        'layout': layout_right
    }
    if not state:
        return 'large-display', total_cases_fig, active_cases_fig, gamma_fig, beta_fig, reproductive_number_fig
    else:
        return 'large-display convert-display-to-navbar', total_cases_fig, active_cases_fig, gamma_fig, beta_fig, reproductive_number_fig



if __name__ == "__main__":
    app.run_server(debug=True, port=8080)