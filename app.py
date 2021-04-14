import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import pandas as pd
import numpy as np

app = dash.Dash(name = __name__, external_stylesheets=[dbc.themes.SUPERHERO])


helpModal = dbc.Modal([
    dbc.ModalHeader("Help"),
    dbc.ModalBody(children = [
        html.H5('Purpose of the app'),
        html.H5('How to use the app')
    ]),
    dbc.ModalFooter(
        dbc.Button("Close", id="closeHelpModel", className="ml-auto")
    ),
], id="helpModal", size="lg")

app.layout = dbc.Container(children = [
    helpModal,
    dbc.Row(children = [
        dbc.Col(children = [
            html.Br(),
            html.H4('COLLEGE FOOTBALL'),
            html.H6('How does your team\'s brand stack up against the competition?')
        ], width = 4, style = {'text-align':'left'}),
        dbc.Col(children = [
            html.Br(),
            dbc.Row(children = [
                dbc.Col(children = [
                    html.Label('Choose a team:')
                ], width = 4, style = {'text-align':'right'}),
                dbc.Col(children = [
                    dcc.Dropdown(id = 'selectedTeam')
                ], width = 8)
            ])
            
        ], width = 4),
        dbc.Col(children = [
            html.Br(),
            dbc.Button("Help", id="openHelpModal", outline = True, 
                       className="ml-auto", color = 'info')
        ], width = 3, style = {'text-align':'right'}),
        dbc.Col(children = [
            html.Img(src = 'https://upload.wikimedia.org/wikipedia/commons/b/b2/Southeastern_Conference_logo.svg', style = {
                'height' : '75%',
                'width' : '75%',
                'vertical-align': 'top',
                'float' : 'right',
                'position' : 'relative',
                'padding-top' : 5,
                'padding-right' : 0,
                'padding-left':0,
                'padding-bottom':0
            })
        ], width = 1, style = {'text-align':'right'})
    ]),
    html.Hr(style = {'background-color':'white'}),
], fluid = True)

@app.callback(
    Output("helpModal", "is_open"),
    [Input("openHelpModal", "n_clicks"), Input("closeHelpModel", "n_clicks")],
    [State("helpModal", "is_open")],
)
def toggle_help_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(debug = True)