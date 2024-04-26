import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
# Connect to main app.py file
from app import app
from dash_iconify import DashIconify
from app import server

# Connect to your app pages
from pages import Homepage, page2, page3, page4

brain_icon = html.Img(src=app.get_asset_url('mental-disorder.png'),
                      style={'height': '34px', 'margin-right': 10,'margin-bottom':8})

home_icon = DashIconify(icon="fa:home", style={'margin-right': 18,'font-size':25})
world_icon = DashIconify(icon="fa6-solid:earth-americas", style={'margin-right': 18,'font-size':25})
factors_icon = DashIconify(icon="fa6-solid:money-bill-trend-up", style={'margin-right': 18,'font-size':25})
surveys_icon = DashIconify(icon="fa6-solid:clipboard-list", style={'margin-right': 18,'font-size':25})

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.NavbarSimple(
        [
            dbc.NavItem(dbc.NavLink([home_icon],style={"font-weight":"bold"}, href="/pages/homepage")),
            dbc.NavItem(dbc.NavLink([world_icon], style={"font-weight":"bold"},href="/pages/page2")),
            dbc.NavItem(dbc.NavLink([factors_icon],style={"font-weight":"bold"}, href="/pages/page3")),
            dbc.NavItem(dbc.NavLink([surveys_icon], style={"font-weight":"bold"},href="/pages/page4"))
        ],
    brand=html.Div([brain_icon,"Mental Health Analytics"],style={"font-weight":"bold","color":"#fbfffc",'font-size':30}),
    color='#8bc7b3',
    brand_href="#",
    dark=True,
),
    html.Div(id='page-content', children=[])
])




@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pages/homepage':
        return Homepage.layout
    if pathname == '/pages/page2':
        return page2.layout
    if pathname == '/pages/page3':
        return page3.layout
    if pathname == '/pages/page4':
        return page4.layout
    else:
        return Homepage.layout


if __name__ == '__main__':
    app.run_server(port='8051',debug=False)