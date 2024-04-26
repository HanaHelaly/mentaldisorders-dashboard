import pathlib
import dash
from dash import html, dcc, Dash, Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from app import app


PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

df1 = pd.read_csv(DATA_PATH.joinpath("mental disorders.csv"))

indices = df1[df1['Year']<1999].index
df1 = df1.drop(indices, axis=0).reset_index(drop = True)

download_icon = DashIconify(icon="lets-icons:arrow-drop-down-big", style={'margin-right': 5})
stress_icon = html.Img(src=app.get_asset_url('anxious.png'),
                      style={'height': '48px', 'margin-right': 10})
depression_icon = html.Img(src=app.get_asset_url('tired.png'),
                           style={'height': '48px', 'margin-right': 10})
bipolar_icon = html.Img(src=app.get_asset_url('bipolar.png'),
                           style={'height': '48px', 'margin-right': 10})
schizophrenia_icon = html.Img(src=app.get_asset_url('schizophrenia.png'),
                           style={'height': '48px', 'margin-right': 10})
eat_icon = html.Img(src=app.get_asset_url('eating-disorder.png'),
                           style={'height': '48px', 'margin-right': 10})
submit_icon = DashIconify(icon="game-icons:click", style={'margin-right': 5,'height':40})
people_icon = DashIconify(icon="akar-icons:people-group", style={'height': '48px'})


layout = dbc.Container([
    dbc.Row([
    html.Br(),

    dbc.Col([
        dbc.Row([
            html.H2("The Influence of Demographic, Economic, and Geographic Factors on Mental Health Disorders",
                    className='mb-5',
                    style={'color': '#144a51', 'font-weight': 'bold', 'padding-top': '100px', 'text-align': 'justify'}),
            dbc.Col([
            dbc.Button([download_icon, "Show Description"], outline=True, color='info',
                       id="proj_des_button",className='mb-2', size=3)],width={'size': 4}),
            html.Div(id="proj_des")
        ],
            className='float-left mb-4'),
        dbc.Row([
        dbc.Col([
            dbc.Accordion(
                [
                    dbc.AccordionItem(
                        [
                            html.P(
                                "Anxiety disorders cover a spectrum of mental health issues marked by intense anxiety and fear. These conditions may present as general anxiety, panic attacks, specific phobias, social anxiety, and other forms. Typical symptoms include excessive worry, restlessness, and difficulty concentrating, often interfering with daily functioning."
                                , style={'text-align': 'justify', 'color':'#272727'}),
                        ],
                        title=html.Div([

                            html.Span(stress_icon),
                            html.Div([
                                html.P("Anixety Disorder",
                                       style={'color':'#272727', 'font-size':16}),

                                html.P("Types and Impact",
                                       style={'font-size': 14, 'color': '#999999', 'margin-bottom': 0,
                                              })])

                        ], style={'display': 'inline-flex', 'align-items': 'center'})
                    ),

                    dbc.AccordionItem(
                        [
                            html.P(
                                "Depressive disorders represent a group of conditions marked by persistent feelings of sadness and loss of interest. Major depression, persistent depressive disorder, and seasonal affective disorder are among the types. Symptoms can vary but often include changes in sleep, appetite, energy level, and self-esteem."
                                , style={'text-align': 'justify', 'color':'#272727'}),
                        ],
                         title = html.Div([

                            html.Span(depression_icon),
                            html.Div([
                                html.P("Depressive Disorder",
                                       style={'color': '#272727', 'font-size': 16}),

                                html.P("More than just Sadness",
                                       style={'font-size': 14, 'color': '#999999', 'margin-bottom': 0,
                                              })])

                        ], style={'display': 'inline-flex', 'align-items': 'center'})
                    ),
                    dbc.AccordionItem(
                        [
                            html.P(
                                "Bipolar disorder is characterized by extreme mood swings, from manic highs to depressive lows. These shifts in mood, energy, and activity levels can affect an individual's ability to carry out day-to-day tasks. Diagnosis and management require a careful and comprehensive approach."
                                , style={'text-align': 'justify', 'color':'#272727'}),
                        ],
                        title = html.Div([

                        html.Span(bipolar_icon),
                        html.Div([
                            html.P("Bipolar Disorder",
                                   style={'color': '#272727', 'font-size': 16}),

                            html.P("Emotional Rollercoaster",
                                   style={'font-size': 14, 'color': '#999999', 'margin-bottom': 0,
                                          })])

                    ], style={'display': 'inline-flex', 'align-items': 'center'})

                    ),
                    dbc.AccordionItem(
                        [
                            html.P(
                                "Schizophrenia is a complex and chronic mental disorder characterized by disturbances in thought, perception, and behavior. It often presents with symptoms like hallucinations, delusions, and disorganized thinking, profoundly impacting daily functioning."
                                , style={'text-align': 'justify', 'color':'#272727'}),
                        ],
                        title = html.Div([

                        html.Span(schizophrenia_icon),
                        html.Div([
                            html.P("Schizophrenia Disorder",
                                   style={'color': '#272727', 'font-size': 16}),

                            html.P("Reality Distortion and Disconnection",
                                   style={'font-size': 14, 'color': '#999999', 'margin-bottom': 0,
                                          })])

                         ], style={'display': 'inline-flex', 'align-items': 'center'})
                    ),
                    dbc.AccordionItem(
                        [
                            html.P(
                                "Eating disorders are serious conditions affecting eating behaviors and related thoughts and emotions. Common types include anorexia nervosa, bulimia nervosa, and binge-eating disorder. These disorders can have significant physical and psychological impacts and often require comprehensive treatment.",
                                style={'text-align': 'justify', 'color':'#272727'}),
                        ],
                        title = html.Div([

                        html.Span(eat_icon),
                        html.Div([
                            html.P("Eating Disorder",
                                   style={'color': '#272727', 'font-size': 16}),

                            html.P("Unhealthy Relationship with Food",
                                   style={'font-size': 14, 'color': '#999999', 'margin-bottom': 0,
                                          })])

                        ], style={'display': 'inline-flex', 'align-items': 'center'})
                    ),

                ],style={'margin-top': '20px'}
            )

            ],className='float-left')
            ])
            ], width={'size': 7}),

        dbc.Col([
            dbc.Row([
                    html.Div([
                                    dbc.Button(id='live-card',
                                            className="text-center m-4 bg-white border-white ",
                                               ),
                                    dbc.Popover(id='popover',
                                                target="live-card",
                                                trigger="hover",
                                                placement="bottom")

                    ],style={"height": "80px", "padding-top": 60, "margin-left": "200px", "margin-bottom": "20px",'width': '70%'}),

                    dcc.Interval(
                            id='interval-component',
                            interval=6000,  # in milliseconds
                            n_intervals=0
                    )
                    ]),

            html.Div(children=[html.H6('Average Prevalence Rate of Mental Health Conditions',
                                       style={'text-align':'center','color':'#6c857e'}),
                    dcc.Graph(id='bar_plot'),
                    dcc.Slider(df1['Year'].min(),
                               df1['Year'].max(),
                               marks={str(year): year for year in df1['Year'].unique() if (year%2 != 0)},
                               step=None,
                               id="year_slider",
                               value=df1['Year'].max(),className='mb-3'),
                    html.Div([
                                html.Div([
                                    html.P('select by country or worldwide :',
                                    style={'font-size' : 12}),
                                    dcc.Dropdown(df1['Entity'].unique(),
                                                 id='entity_dropdown',
                                                 value='World',
                                                 className='mb-4 me-5',
                                                 style={'width': '250px',
                                                        'border-color': '#a3dfe8'
                                                        }
                                                 )
                                    ],style={'margin-right': '150px'}),

                    dbc.Button([submit_icon, "submit"], outline=True, color='info',
                               id="submit_button",className='custom-button text-end')
                        ],style={'display': 'flex', 'align-items': 'center'})


                    ],style={'margin-top': 160})

                    ], width={'size': 5},align='top')

            ], justify='start')
    ])

@app.callback(
    Output("proj_des", "children"),
    Input("proj_des_button", "n_clicks")
)
def show_text(n_clicks):
    if n_clicks % 2 != 0:
        dp = html.P('This dashboard focuses on exploring mental health by examining how different factors such as demographics, economics, and geography impact the occurrence and treatment of mental disorders in different groups and areas. By using reliable data sources, our goal is to reveal disparities and patterns in mental health care, highlighting both the obstacles and possibilities for enhancing support and treatment.',
                    className="text-monospace float-none mt-3",
                    style={'color': '#272727', 'text-align': 'justify'})
        return dp
    else:
        return None

@app.callback(
    Output(component_id="bar_plot",component_property="figure"),
    State(component_id="year_slider",component_property="value"),
    State(component_id="entity_dropdown",component_property="value"),
    Input(component_id="submit_button",component_property="n_clicks")
)
def update_figure(selected_year, selected_entity, n):

    colors = {'Anxiety': '#B4A7D6', 'Depression': '#9FC5E8', 'Bipolar': '#B7ECEC', 'Schizophrenia': '#98dab8',
              'Eating': '#FFE599'}
    filtered_df = df1[(df1['Year'] == selected_year) & (df1['Entity'] == selected_entity)]
    fig=px.bar(filtered_df, x='Mental Disorder', y='Prevalence', color='Mental Disorder',color_discrete_map=colors, text='Prevalence')
    fig.update_layout(
    plot_bgcolor='white',
    font_color="#647585",
    height=550,
    showlegend=False,
    yaxis=dict(showticklabels=False),
    xaxis=dict(tickangle=0)
    )

    fig.update_traces(marker=dict(cornerradius=5),textfont_size=12,textposition="outside",texttemplate='%{text:.2s%}%')

    fig.add_annotation(
        x='Anxiety',
        y=max(filtered_df['Prevalence']),
        text='Always no. 1',
        showarrow=True,
        arrowhead=1,
        arrowcolor='orange',
        ay=-30,
        yref='y',
        yshift=30
    )
    return fig

@app.callback(
    [Output('live-card', 'children'),
     Output('popover', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_display_value(n):
    # Determine the index of the value to display based on the number of intervals passed
    live_text = ['319.9', '280M', '70 M', '40M', '24M', '15M']
    mental_disorders = ['anxiety', 'depression', 'eating disorder', 'bipolar', 'schizophrenia', 'eating']
    index = n % len(live_text)

    # Create the contents of the card
    button_contents = [html.H1(children=[html.I(className="bi bi-people-fill m-2"), live_text[index]],
                              style={'color':'#144a51','font-weight':'bold'})]
    popover = dbc.PopoverBody("Estimated affected people by {} in millions".format(mental_disorders[index]),style={'color': '#272727'})

    return button_contents, popover


