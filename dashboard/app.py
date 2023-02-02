from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv
import dash

app = Dash(__name__, use_pages=True)

app.layout =html.Div(children=[
    html.H1('DELOTON'),
    html.Div(
        [
            html.Div(
                dcc.Link(
                     f"{page['name']} - {page['path']}", href=page["relative_path"]
                )
            )
            for page in dash.page_registry.values()
        ]
    ),
    dash.page_container
])

"""Putting this here for now, to test locally"""
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True, port=8080)
    