import plotly.express as px
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import pycountry_convert as pc
import pathlib
import pandas as pd
from app import app
loupe_icon = html.Img(src=app.get_asset_url("loupe.png"),
                      style={'height': '30px', 'margin-right': 10})

# from utils.demo_data_process import get_continent_name, country_code_to_continent_name

# DATA_PATH = '../data/surveys'
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data/surveys").resolve()

continent_dict = {
    "NA": "North America",
    "SA": "South America",
    "AS": "Asia",
    "AF": "Africa",
    "OC": "Oceania",
    "EU": "Europe",
    "AQ": "Antarctica"
}

def get_continent_name(continent_code: str) -> str:   #print(get_continent_name('NA'))  --> Outputs: North America

    return continent_dict[continent_code]

def country_code_to_continent_name(country_code):
    try:
        code_a2 = pc.country_alpha3_to_country_alpha2(country_code)
        continent_code = pc.country_alpha2_to_continent_code(code_a2)
        continent_name = get_continent_name(continent_code)
        return continent_name
    except (KeyError, TypeError):
        return 'Unknown'

def process_and_clean_survey_data():

    #Approaches when dealing with anxiety and depression processing
    approaches_df = pd.read_csv(DATA_PATH.joinpath("dealing-with-anxiety-depression-approaches.csv"))
    approaches_df['Continent'] = approaches_df['Code'].apply(country_code_to_continent_name)
    approaches_df.rename(columns={
        'Share - Question: mh8b - Engaged in religious/spiritual activities when anxious/depressed - Answer: Yes - Gender: all - Age_group: all': 'Engaged in Religious or Spiritual Activities when Anxious or Depressed',
        'Share - Question: mh8e - Improved healthy lifestyle behaviors when anxious/depressed - Answer: Yes - Gender: all - Age_group: all': 'Improved Healthy Lifestyle Behaviors when Anxious or Depressed',
        'Share - Question: mh8f - Made a change to work situation when anxious/depressed - Answer: Yes - Gender: all - Age_group: all': 'Made a Change to Work Situation when Anxious or Depressed',
        'Share - Question: mh8g - Made a change to personal relationships when anxious/depressed - Answer: Yes - Gender: all - Age_group: all': 'Made a Change to Personal Relationships when Anxious or Depressed',
        'Share - Question: mh8c - Talked to friends or family when anxious/depressed - Answer: Yes - Gender: all - Age_group: all': 'Talked to Friends or Family when Anxious or Depressed',
        'Share - Question: mh8d - Took prescribed medication when anxious/depressed - Answer: Yes - Gender: all - Age_group: all': 'Took Prescribed Medication when Anxious or Depressed',
        'Share - Question: mh8h - Spent time in nature/the outdoors when anxious/depressed - Answer: Yes - Gender: all - Age_group: all': 'Spent Time in Nature or Outdoors when Anxious or Depressed',
        'Share - Question: mh8a - Talked to mental health professional when anxious/depressed - Answer: Yes - Gender: all - Age_group: all': 'Talked to a Mental Health Professional when Anxious or Depressed'
    }, inplace=True)

    # discomfort speaking anixiety and depression processing
    discomfort_df = pd.read_csv(f'{DATA_PATH}/discomfort-speaking-anxiety-depression.csv')
    discomfort_df.rename(columns={
        'Share - Question: mh5 - Someone local comfortable speaking about anxiety/depression with someone they know - Answer: Not at all comfortable - Gender: all - Age_group: all': 'Not Comfortable Discussing Anxiety/Depression with Acquaintances'
    }, inplace=True)  
    discomfort_df['Continent'] = discomfort_df['Code'].apply(country_code_to_continent_name)

    # fund research on anxiety and depression processing
    fund_df = pd.read_csv(f'{DATA_PATH}/fund-research-anxiety-depression.csv')
    fund_df.rename(columns={
        'Share - Question: mh4b - Important for national government to fund research on anxiety/depression - Answer: Extremely important - Gender: all - Age_group: all': 'View on National Government Funding for Anxiety/Depression Research as Extremely Important'
    }, inplace=True)
    
    fund_df['Continent'] = fund_df['Code'].apply(country_code_to_continent_name)

    fund_df = fund_df.dropna(subset=[
        'View on National Government Funding for Anxiety/Depression Research as Extremely Important',
    ])
    fund_df = fund_df.drop(columns=[
        'Population (historical estimates)',
        'GDP per capita, PPP (constant 2017 international $)'
    ])

    return approaches_df, discomfort_df, fund_df

def clean_duplicated_columns(df):
    df = df[[col for col in df.columns if not col.endswith('_y')]]
    df.columns = [col.replace('_x', '') for col in df.columns]
    return df


approaches_df, discomfort_df, fund_df = process_and_clean_survey_data()
merged_survey_df = clean_duplicated_columns(approaches_df.merge(discomfort_df, on='Entity', how='inner'))
merged_survey_df = clean_duplicated_columns(merged_survey_df.merge(fund_df, on='Entity', how='inner'))

PATH = pathlib.Path(__file__).parent
data_path = PATH.joinpath("../data").resolve()

df = pd.read_csv(data_path.joinpath("output_approaches_df.csv"))

basic_cols = ['Entity', 'Code', 'Year', 'Continent']
all_questions = [question for question in merged_survey_df.columns if question not in basic_cols]
all_continents = [continent for continent in merged_survey_df['Continent'].unique() if continent != 'Unknown']

values_to_remove = ['High-income countries','Lower-middle-income countries', 'Low- and middle-income countries','Upper-middle-income countries','Low-income countries']

df_country = df[~df['Entity'].isin(values_to_remove)]

# print(df)

income_levels = [
    'Low-income countries',
    'Lower-middle-income countries',
    'Upper-middle-income countries',
    'High-income countries'
]

def filter_on_entity(df, entity_list):
    mask = df['Entity'].isin(entity_list)
    return df[mask]

df_income = filter_on_entity(df, income_levels)
#  print(df_income)


minty_colors = ['#3EB489', '#2CA58D', '#207F74', '#2F5D62', '#1E474C']

layout = dbc.Container([
    dbc.Row([
    dbc.Row([
        dbc.Col(html.H2("Insights from Global Mental Health Survey",
                        style={'color': '#144a51','font_size':'28px','font-weight': 'bold', 'padding-top': '50px'}),
                width=12, className="justify-title fade-in"),
        html.P([loupe_icon,
                     """Explore key findings and patterns from 2020 global mental health surveys, specifically 
                            focusing on anxiety and depressive disorders. Uncover trends in public perception, 
                            approaches to managing anxiety and depression, and the societal impact of these conditions 
                            during this period."""],
                    style={'text-align': 'left', 'margin-top': '10px', 'font-size': 18, 'color': '#333131'})],
                    className='mb-4'),
    dbc.Row([
    dbc.Col([
        html.Div([
            html.Label('Select a condition:', className="fade-in", 
                       style={'margin-bottom': '10px', 'display': 'block', 'color': '#333','font-weight':'bold'}),
            dcc.Dropdown(
                id='condition-dropdown',
                options=[{'label': condition, 'value': condition} for condition in all_questions],
                value=all_questions[0],
                className="fade-in",
                style={
                    'width': '100%',        
                    'color': '#333',       
                    'backgroundColor': '#fff',  
                    'padding': '5px',    
                    'borderRadius': '6px',
                    'font-size': '16px',
                },
            ),
        ], style={'padding-right': '15px', 'padding-left': '15px'}),  # Adjust the padding to align with your grid system
    ], width=6),

    dbc.Col([
        html.Div([
            html.Label('Select a continent:', className="fade-in", 
                       style={'fontWeight': 'bold', 'margin-bottom': '10px', 'display': 'block', 'color': '#333'}),
            dcc.Dropdown(
                id='continent-dropdown',
                options=[{'label': continent, 'value': continent} for continent in sorted(all_continents)],
                value=all_continents[0],
                className="fade-in",
                style={
                    'width': '100%',        
                    'color': '#333',       
                    'backgroundColor': '#fff',  
                    'padding': '5px',    
                    'borderRadius': '6px', 
                    'font-size': '16px',
                },
            ),
        ], style={'padding-right': '15px', 'padding-left': '15px'}),  # Adjust the padding to align with your grid system
    ], width=6),
], justify="start", align="start"),

    dbc.Row([
        dbc.Col(html.Div(id='selection-output',className="text-center" ,style={'color': '#3EB489','fontWeight': 'bold',
})),
        dbc.Col(dbc.Progress(id='survey-progress',color=minty_colors,label=f"{0}%"),width=6,style={'width':'50%','color':minty_colors,'padding':'5px','borderRadius':'7px'},
               align='center', className="mb-3" ),
        dbc.Tooltip(
            '''
            Represents the proportion of the surveyed population 
            that reported experiencing the condition",
            target="survey-progress
            ''',  
        )
    ], align="center", className="mb-3"),


    dbc.Row([
        dbc.Col(html.Div("Country Specific Rate", className="mb-2 text-center right"
            ), width=6),
        dbc.Col(html.Div(
        "Income Specific Rate", className="text-left",style={'text-align': 'center'}
        ), width=6),
]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='question-graph'), width=6),
        dbc.Col(dcc.Graph(id='income-graph'), width=6) 

        ])
], justify='around')
])


# Callback to update progress and text output
@app.callback(
    [Output('survey-progress', 'value'),Output('survey-progress', 'label'),Output('selection-output', 'children')],
    [Input('condition-dropdown', 'value'), Input('continent-dropdown', 'value')]
)
def update_output(selected_condition, selected_continent):
    progress_value = (all_questions.index(selected_condition) + 1) * (all_continents.index(selected_continent) + 1) * 10 % 100
    output_text = f"{selected_condition} in {selected_continent} "

    return progress_value,f"{progress_value}%", output_text 



@app.callback(
    Output('question-graph','figure'),
    Output('income-graph', 'figure'),
    Input('condition-dropdown', 'value'),
    Input('continent-dropdown', 'value')
)

def update_graph(selected_condition, selected_continent):

    filtered_df = df_country[(df_country['Continent'] == selected_continent)]

    filtered_df = filtered_df.sort_values(by=selected_condition, ascending=False)
    print(filtered_df.head(10))
    

    fig = px.bar(filtered_df, x=selected_condition, y='Entity', 
                    color='Entity',
                    template='plotly_white',
                    height=400,
                    width=600,
                    color_discrete_sequence=minty_colors,
)

    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        yaxis=dict(showgrid=True, showticklabels=True),
        xaxis=dict(showgrid=False, showticklabels=False),
        showlegend=False,
        bargap=0.7,

        
    )
    fig.update_traces(
    hoverlabel=dict(
        bgcolor='rgba(11, 6, 81, 0.8)',
        bordercolor='rgba(11, 6, 81, 0.8)',
        font=dict(color='white')
    )
)

    # filtered_income_df = df_income[df_income['Continent'] == selected_continent]
    print(selected_condition)
    # print(len(filtered_income_df))
    fig_income = px.bar(df_income, x=selected_condition, y='Entity', 
                     color='Entity',
                     template='plotly_white',
                     height=400,
                     width=600,
                    color_discrete_sequence=minty_colors,

                     )
    fig_income.update_layout(
        xaxis_title="",
        yaxis_title="",
        yaxis_side='right', 
        bargap=0.7,
        bargroupgap=0.1,
        yaxis_tickprefix='   ',    
        yaxis=dict(showgrid=True, showticklabels=True),
        xaxis=dict(showgrid=False, showticklabels=False),
        showlegend=False)
        
    return fig , fig_income     

