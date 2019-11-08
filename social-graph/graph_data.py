import pandas as pd
import plotly.graph_objects as go
import plotly
from pprint import pprint

import git_get

git_get.data_to_csv()

repos = pd.read_csv('repos_info.csv')
commits = pd.read_csv('commits_info.csv')


commits_count = pd.DataFrame(pd.merge(repos, 
         commits, 
         left_on='Id', 
         right_on='Repo Id', 
         how = 'left').groupby('Id').size().reset_index())
commits_count.columns = ['Id', 'Commits count']

repos = pd.merge(repos, commits_count, on = 'Id')

repo_names = repos['Name']
commits = repos['Commits count']

fig = go.Figure(
    data = [go.Bar(x=repo_names, y=commits)],
    layout_title_text="Commits per Repository",
    
)
fig.show()
