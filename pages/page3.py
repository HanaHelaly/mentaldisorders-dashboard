# Import necessary libraries
import dash
from dash import html
from dash import dcc
# import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app
import dash_bootstrap_components as dbc

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

anxiety = pd.read_csv(DATA_PATH.joinpath("anxiety.csv"))
depressive = pd.read_csv(DATA_PATH.joinpath("depressive.csv"))

anxiety = anxiety.sort_values(by='Year')
depressive = depressive.sort_values(by='Year')

loupe_icon = html.Img(src=app.get_asset_url("loupe.png"),
                      style={'height': '34px', 'margin-right': 10})
# Define the layout of the app
layout = dbc.Container(children=[
        dbc.Row([
            html.Div([
                html.H2("The Correlation between GDP and",
                        className='mb-4',
                        style={'color': '#144a51', 'font-weight': 'bold', 'padding-top': '80px', 'text-align': 'left'}),
                dcc.Dropdown(
                    id='disorder-dropdown',
                    options=[

                        {"label": html.Span(['Anxiety'], style={'color': '#144a51', 'font-size': 30,'font-weight':'bold'}),
                         'value': 'anxiety'},
                        {"label": html.Span(['Depression'], style={'color': '#144a51', 'font-size': 30,'font-weight':'bold'}),
                         'value': 'depressive'}
                    ],
                    value='anxiety',
                    style={'width': '13rem','margin-top':37,
                           'fontSize': 50, 'color': '#2b6269', 'outline': 'none', 'border': 'none'}
                )
            ], style={'display': 'inline-flex'}),

            html.H6([loupe_icon,
                     "Explore the interplay between economic development, as measured by Gross Domestic Product (GDP), and the prevalence of selected mental health disorders"],
                    style={'text-align': 'left', 'margin-top': '10px', 'font-size': 20, 'color': '#333131'},
                    className='mb-4'
                    ),
            html.Hr(style={'border-color': '#367d85'}),
            html.Br(),
            dbc.Row([
            dbc.Col([
            dcc.Graph(id='myGraph')],width=10)],
                justify='center'),

            html.P("Filter by Continent",
                   style={'color': '#367d85', 'padding-left': '10px'}),

            dcc.Dropdown(
                id='my-dropdown',
                options=[{'label': region, 'value': region} for region in ['Asia', 'Europe', 'Africa', 'North America', 'South America', 'Oceania']],
                multi=True,
                value=None
            )

            ])
        ])


# Callback to update single graph based on slider and dropdown values
@app.callback(
    Output('myGraph', 'figure'),
    [Input('my-dropdown', 'value'), Input('disorder-dropdown', 'value')]
)
def update_graph(dropdownvalue, selected_disorder):

    if selected_disorder:
        if selected_disorder == 'anxiety':
            filtered_df = anxiety.copy()
        elif selected_disorder == 'depressive':
            filtered_df = depressive.copy()

        if dropdownvalue is not None:
            filtered_df = filtered_df[filtered_df['Continent'].isin(dropdownvalue)]

        fig = px.scatter(filtered_df, x="GDP", y="Prevalence", size="Population (historical estimates)",
                         color="Continent", hover_data=['Entity'], animation_frame='Year', log_x=True, size_max=60)

        fig.update_layout(plot_bgcolor='white',
                          xaxis=dict(
                              linecolor='#5e216f',
                              linewidth=2
                          ),
                          yaxis=dict(
                              linecolor='#5e216f',
                              linewidth=2
                          ),
                          height=470)

        return fig
