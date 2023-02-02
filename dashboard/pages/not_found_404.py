from dash import html
import dash

dash.register_page(__name__)
image_path = # TODO: Download deloton logo image from curriculum page

layout = html.Div(
    [html.H1('Deloton'), html.H3('Rider Dashboard'),html.Img(src='image_path')],
    style={
        'textAlign': 'center',
        'border': '1px solid red',
    },
)