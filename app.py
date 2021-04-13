import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import pandas as pd
import numpy as np

app = dash.Dash(name = __name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(

)



if __name__ == '__main__':
    app.run_server(debug = True)