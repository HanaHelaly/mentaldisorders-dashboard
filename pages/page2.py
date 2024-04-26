import dash
from dash import html, dcc, Dash, Input, Output, State
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import pathlib
from app import app
import plotly.graph_objects as go

#data frame for geographical distributions
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

df1 = pd.read_csv(DATA_PATH.joinpath("mental disorders.csv"))
anxiety_age = pd.read_csv(DATA_PATH.joinpath("anxiety-disorders-prevalence-by-age.csv"))
anxiety_sex = pd.read_csv(DATA_PATH.joinpath("anxiety-disorders-prevalence-gender.csv"))
bipolar_age = pd.read_csv(DATA_PATH.joinpath("bipolar-disorders-prevalence-by-age.csv"))
bipolar_sex = pd.read_csv(DATA_PATH.joinpath("bipolar-disorders-prevalence-gender.csv"))
depressive_age = pd.read_csv(DATA_PATH.joinpath("depressive-disorders-prevalence-by-age.csv"))
depressive_sex = pd.read_csv(DATA_PATH.joinpath("depressive-disorders-prevalence-gender.csv"))
schizo_age = pd.read_csv(DATA_PATH.joinpath("schizophrenia-prevalence-by-age.csv"))
schizo_sex = pd.read_csv(DATA_PATH.joinpath("schizophrenia-prevalence-gender.csv"))

years = df1['Year'].unique()
marks = {str(year): str(year) for year in years if year % 5 == 0 or year == 2019}
mental_disorders = ['anxiety', 'bipolar', 'depressive', 'schizophrenia']
# app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY, "https://your_custom_stylesheet.css"])
loupe_icon = html.Img(src=app.get_asset_url("loupe.png"),
                      style={'height': '32px', 'margin-right': 10})

layout = dbc.Container(
    [
        dbc.Row(
            [
                html.H2("Mental Trends Around The World", className='mb-5',
                            style={'color': '#144a51', 'font-weight': 'bold',
                                   'padding-top': '50px',
                                   'text-align': 'center', 'font-size': '30px'}
                            ),
                html.Hr(),
                html.H6([loupe_icon,"Explore how geographic and demographic factors influence the prevalence of various mental health disorders."],
                    style={'text-align': 'left', 'margin-top': '10px', 'font-size': 20,'color':'#333131'},
                    className='mb-4'
                    )
            ]
        ),
        dbc.Tabs(
            [
                dbc.Tab(
                    [
                        html.Br(),
                        html.H6('Mental Geographical Distribution Worldwide',
                                style={'text-align':'center','color':'#6c857e'}),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col([
                                    dcc.Slider(
                                        id="year_slider",
                                        min=df1['Year'].min(),
                                        max=2019,
                                        step=None,
                                        value=2019,
                                        marks=marks)],
                                        width=6,
                                        align='center'
                                    )
                            ], justify='center',
                            style={'margin-bottom': '0px'}
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(
                                        dcc.Graph(id="map_holder"),
                                        style={'position': 'relative'}
                                    )
                                )
                            ]
                        )
                    ],
                    label="Geographic",
                    active_tab_style={"font-weight": "bold","color": "#333131"}
                ),
                dbc.Tab(
                    [
                        dbc.Row(

                            [
                                html.Div([
                                    html.H6("Choose a mental disorder:",
                                            style={'text-align': 'left','margin-top': '30px',
                                                   }),
                                    dcc.Dropdown(
                                        id='disorder_dropdown',
                                        options=[{'label': disorder.capitalize(), 'value': disorder} for disorder in
                                                 mental_disorders],
                                        value=mental_disorders[0],
                                        style={'width': '200px',
                                            'margin-top': '10px','margin-left': '10px','text-align': 'left'}
                                    )
                                ], style={'display': 'flex', 'justify-content': 'flex-end'}),

                                dbc.Row([
                                    html.H6(id='graph_title',style={'text-align':'center','color':'#6c857e'}),
                                    dbc.Col([
                                    dcc.Graph(id="age")],
                                    width=8),
                                    dbc.Col([
                                    dcc.Graph(id="gender")],
                                    width=4),
                                ],justify="around",style={'padding':'40px'})

                            ]
                        )

                    ],
                    label="Demographic",
                    active_tab_style={"font-weight": "bold"}
                )
            ]
        )
    ]
)


@app.callback(
    Output('map_holder', 'figure'),
    [Input('year_slider', 'value')]
)
def update_graph(selected_year):
    filtered_data = df1[df1['Year'] == selected_year]

    if filtered_data.empty:
        fig = px.scatter()
    else:
        fig = px.scatter_geo(filtered_data, locations="Code",
                             color="Mental Disorder",
                             hover_name="Entity",
                             size="Prevalence",
                             projection="natural earth",
                             labels={"Mental Disorder": "Disorder"})

        fig.update_layout(legend=dict(x=0.8))
    return fig


@app.callback(
[Output('age', 'figure'),
    Output('gender', 'figure'),
    Output('graph_title','children')],
    Input('disorder_dropdown', 'value')
)
def update_age_sex_graph(selected_disorder):
    # Determine which DataFrame to use based on selected disorder
    if selected_disorder == 'anxiety':
        age_df = anxiety_age
        sex_df = anxiety_sex

    elif selected_disorder == 'bipolar':
        age_df = bipolar_age
        sex_df = bipolar_sex

    elif selected_disorder == 'depressive':
        age_df = depressive_age
        sex_df = depressive_sex

    elif selected_disorder == 'schizophrenia':
        age_df = schizo_age
        sex_df = schizo_sex
    else:
        raise ValueError(f"Invalid disorder selected: {selected_disorder}")

    gender_colors = {'Female': '#ae86bc', 'Male': '#4db0c7'}
    age_colors = {'5-19 years':'#B4A7D6', '20-34 years': '#9FC5E8', '35-54 years': '#B7ECEC', '55-64 years': '#98dab8',
                  '65+ years': '#FFE599'}

    fig1 = px.histogram(age_df,
                        x='Age Group',
                        y='Population Share',
                        # histfunc='avg',
                        color='Age Group',
                        color_discrete_map=age_colors,
                        text_auto=True,
                        labels={"Age Group": "Age Group", "Population Share": "Population Share"})

    fig1.update_yaxes(showticklabels=False)
    fig2 = px.box(sex_df, x='Gender', y='Population Share', color='Gender', color_discrete_map=gender_colors)

    fig1.update_layout(plot_bgcolor='white',
                       font_color="#647585",width=800)

    fig1.update_traces(marker=dict(cornerradius=5), textposition="outside",
                       showlegend=False)

    fig2.update_layout(plot_bgcolor='white',font_color="#647585",height=450,width=500)
    fig2.update_traces(showlegend=False)
    # fig2.update_yaxes(title='')

    return fig1, fig2, f"Population Distribution of {selected_disorder.capitalize()} by Age and Gender"
