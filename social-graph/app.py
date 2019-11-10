# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
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
commits = repos['Commits count']

github = 'github.png'
openai = 'openai.png'
encoded_github = base64.b64encode(open(github, 'rb').read())
encoded_openai = base64.b64encode(open(openai, 'rb').read())
###################################  Logic Goes Here  ################################### 



###################################  Custom Styles  ################################### 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

title = {
    "font-weight" : "bold"
}

subheading = {
    'text-align' : 'center'
}



###################################  Custom Styles  ################################### 



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(children=[
    html.H1("Github Social Graph", id="title", style=title),
    html.H3("A Year in Review...", id="subheading", style=subheading),
    html.Img(src='data:image/png;base64,{}'.format(encoded_github)),
    html.Img(src='data:image/png;base64,{}'.format(encoded_openai)),

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
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
