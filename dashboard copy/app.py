from dash import Dash, dcc, html, Output, Input
import dash
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[
           dbc.themes.COSMO], use_pages=True)

app.layout = html.Div(dash.page_container)

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True, port=8080)
