# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np

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
###################################  Logic Goes Here  ################################### 



###################################  Custom Styles  ################################### 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

###################################  Custom Styles  ################################### 



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(children=[
    html.H1("Github Social Graph", style={"font-weight" : "bold"}),
    html.H3("A Year in Review...", style={'text-align' : 'center'}),

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
