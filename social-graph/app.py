# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import base64

import git_get

###################################  Logic Goes Here ################################### 
repos = pd.read_csv('../data/repos_info.csv')
commits = pd.read_csv('../data/commits_info.csv')



commits_count = pd.DataFrame(pd.merge(repos, 
         commits, 
         left_on='Id', 
         right_on='Repo Id', 
         how = 'left').groupby('Id').size().reset_index())
commits_count.columns = ['Id', 'Commits count']

repos = pd.merge(repos, commits_count, on = 'Id')

repo_names = repos['Name']
commits = repos['Commits count']

color = np.array(['rgb(255,255,255)']*commits.shape[0])
color[commits>=1] = 'c6e48b' # pale green
color[commits>=200] = '7bc96f' # green
color[commits>=500] = '#239a3b' # olive green
color[commits>=1000] = '#196127' # dark green


list_of_languages = []
for languages in repos['Languages']:
    if type(languages) == str:
        for language in languages.split(','):
            list_of_languages.append(language.strip())

languages_count = pd.Series(list_of_languages).value_counts()



github = 'assets/github_blue.png'
openai = 'assets/openai.png'

encoded_github = base64.b64encode(open(github, 'rb').read()).decode('ascii')
encoded_openai = base64.b64encode(open(openai, 'rb').read()).decode('ascii')

###################################  Logic Goes Here  ################################### 



###################################  Custom Styles  ################################### 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

title = {
    "font-weight" : "bold",
    "text-align": "center",
}

subheading = {
    'text-align' : 'center',
    'font-style': 'italic'
}

row = {
    'text-align' : 'center',
}


image = {
    'display': 'inline-block',
    'width': '100px',
    'height': '100px',
    'padding': '10px'
}



###################################  Custom Styles  ################################### 



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



app.layout = html.Div(children=[
    html.H1("Github Social Graph", style=title),
    html.H3("A Visualisation of OpenAI's Github Data", style=subheading),

    html.Div(children=[
        html.Img(src='data:image/png;base64,{}'.format(encoded_github), style=image),
        html.Img(src='data:image/png;base64,{}'.format(encoded_openai), style=image)
    ], style=row),

    html.Div([
        html.Div([
            dcc.Graph(
                id='commits_per_repo',
                figure={
                    'data': [
                        {'x': repo_names, 'y': commits, 'type': 'bar', 'marker':dict(color=color.tolist())}
                    ],
                    'layout': {
                        'title': 'Commits per Repository',
                        'paper_bgcolor': 'rgba(0,0,0,0)',
                        'plot_bgcolor': 'rgba(0,0,0,0)',
                        'xaxis': {
                            'title': {
                                'text': 'Repository'
                            }
                        },
                        'yaxis': {
                            'title': {
                                'text': 'Commit Count'
                            }
                        }
                    }
                }
            )
        ], className="six columns"),

        html.Div([
            dcc.Graph(
                id='languages_donut',
                figure={
                    'data': [
                        go.Pie(
                            labels=list_of_languages, 
                            values=languages_count, 
                            hole=.3
                        )
                    ],
                    'layout': {
                        'title': 'Popular Languages',
                        'paper_bgcolor': 'rgba(0,0,0,0)',
                        'plot_bgcolor': 'rgba(0,0,0,0)'
                    }
                }
            )
        ], className="six columns")
    ], className="row"),

    dcc.Dropdown(
        id='repo-select',
        options=[
            {'label': 'gym', 'value': 'gym'},
            {'label': 'baselines', 'value': 'baselines'},
            {'label':'roboschool', 'value': 'roboschool'},
            {'label': 'mujoco-py', 'value': 'mujoco-py'},
            {'label': 'spinningup', 'value': 'spinningup'},
            {'label': 'retro', 'value': 'retro'}
        ],
        value= 'gym',
        style= {
            'width': '130px',
            'margin-left': 'auto',
            'margin-right': 'auto',
            'margin-top': '5em'
        }
    ),

    html.Div([
        html.Div(id='violin-graph', className='six columns'),
        html.Div(id='output-container', className='six columns')
    ], className = 'row')
])

@app.callback(
    Output('output-container', 'children'),
    [Input('repo-select', 'value')]
)
def update_contribs_graph(value):
    if value != None:
        info = git_get.get_contributors_info(value)
        
        trace1 = go.Bar(
            x=info['User'], y=info['Additions'],
            name="additions"
        )
        trace2 = go.Bar(
            x=info['User'], y=info['Deletions'],
            name="deletions"
        )
        data = [trace2, trace1]
        layout = go.Layout(
            barmode= 'stack',
            title={
                'text': 'Additions vs. Deletions For Top 10 Contributors',
                'xanchor': 'center',
                'yanchor': 'top',
                'x': 0.5,
                'y': 0.9
            }
        )

        fig = go.Figure(data=data, layout=layout)

        return dcc.Graph(figure=fig)

@app.callback(
    Output('violin-graph', 'children'),
    [Input('repo-select', 'value')]
)
def update_active_hours(value):
    if value != None:
        info = git_get.contributor_punchcard(value)
        days = list('Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday'.split(","))
        data = []

        i = 0
        for day in info:
            trace = go.Scatter(
                x=[days[i]] * 22,
                y=day['Hour'],
                mode='markers',
                marker=dict(
                    size=day['Commits'],
                    sizemode='area',
                    sizeref=2.*max(day['Commits'])/(25.**2),
                    sizemin=4
                ),
                hovertext=day['Commits'],
                name=days[i]
            )
            data.append(trace)
            i += 1

        layout = go.Layout(
            title={
                'text': 'Active Hours',
                'xanchor': 'center',
                'yanchor': 'top',
                'x': 0.5,
                'y': 0.9
            },
            yaxis={
                'rangemode':'tozero'
            }
        )
        fig = go.Figure(data=data, layout=layout)
        fig.update_yaxes(tick0=0, dtick=1)

        return dcc.Graph(figure=fig)



if __name__ == '__main__':
    app.run_server(debug=True)


