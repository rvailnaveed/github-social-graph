# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import base64

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
commits = repos['Commits count'].sort_values(ascending=False)

list_of_languages = []
for languages in repos['Languages']:
    if type(languages) == str:
        for language in languages.split(','):
            list_of_languages.append(language.strip())

languages_count = pd.Series(list_of_languages).value_counts()



github = 'github.png'
openai = 'openai.png'
chain = 'chain.png'

encoded_github = base64.b64encode(open(github, 'rb').read()).decode('ascii')
encoded_openai = base64.b64encode(open(openai, 'rb').read()).decode('ascii')
encoded_chain = base64.b64encode(open(chain, 'rb').read()).decode('ascii')

###################################  Logic Goes Here  ################################### 



###################################  Custom Styles  ################################### 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

title = {
    "font-weight" : "bold",
    "text-align": "center",
    "font-family": 'Roboto Mono'
}

subheading = {
    'text-align' : 'center'
}

row = {
    'text-align' : 'center',
}


image = {
    'display': 'inline-block',
    'width': '100px',
    'height': '100px'
}

openai_image = {
    'display': 'inline-block',
    'width': '300px',
    'height': '120px'
}



###################################  Custom Styles  ################################### 



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(children=[
    html.H1("Github Social Graph", style=title),
    html.H3("A Visualisation of OpenAI's Github Data", style=subheading),

    html.Div(children=[
        html.Img(src='data:image/png;base64,{}'.format(encoded_github), style=image),
        html.Img(src='data:image/png;base64,{}'.format(encoded_chain), style=image),
        html.Img(src='data:image/png;base64,{}'.format(encoded_openai), style=image)
    ], style=row),


    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': repo_names, 'y': commits, 'type': 'bar'}
            ],
            'layout': {
                'title': 'Commits per Repository',
                
            }
        }
    ),

    dcc.Graph(
        id='languages',
        figure={
            'data': [
                go.Pie(
                    labels=list_of_languages, 
                    values=languages_count, 
                    hole=.3
                )
            ]
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)