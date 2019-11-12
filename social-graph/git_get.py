import json
import requests
import numpy as np
import pandas as pd

import requests
from requests.auth import HTTPBasicAuth

def data_to_csv():
    credentials = json.loads(open('credentials.json').read())
    authentication = HTTPBasicAuth(credentials['username'], credentials['password'])

    data = requests.get('https://api.github.com/users/' + 'openai', auth=authentication)
    data = data.json()

    # print("Information about user {}:\n".format(credentials['username']))
    # print("Name: {}".format(data['name']))
    # print("Email: {}".format(data['email']))
    # print("Location: {}".format(data['location']))
    # print("Public repos: {}".format(data['public_repos']))
    # print("Public gists: {}".format(data['public_gists']))
    # print("About: {}\n".format(data['bio']))

    print("Collecting repositories information")
    url = data['repos_url']
    page_no = 1
    repos_data = []
    while (True):
        response = requests.get(url, auth = authentication)
        response = response.json()
        repos_data = repos_data + response
        repos_fetched = len(response)
        # print("Total repositories fetched: {}".format(repos_fetched))
        if (repos_fetched == 30):
            page_no = page_no + 1
            url = data['repos_url'] + '?page=' + str(page_no)
        else:
            break

    repos_information = []
    for i, repo in enumerate(repos_data):
        data = []
        data.append(repo['id'])
        data.append(repo['name'])
        data.append(repo['description'])
        data.append(repo['created_at'])
        data.append(repo['updated_at'])
        data.append(repo['owner']['login'])
        data.append(repo['open_issues_count'])
        data.append(repo['url'])
        data.append(repo['commits_url'].split("{")[0])
        data.append(repo['url'] + '/languages')
        repos_information.append(data)


    repos_df = pd.DataFrame(repos_information, columns = ['Id', 'Name', 'Description', 'Created on', 'Updated on', 
                                                        'Owner', 'Issues count',
                                                        'Repo URL', 'Commits URL', 'Languages URL'])

    print("Collecting language data")
    for i in range(repos_df.shape[0]):
        response = requests.get(repos_df.loc[i, 'Languages URL'], auth=authentication)
        response = response.json()
        if response != {}:
            languages = []
            for key, value in response.items():
                languages.append(key)
            languages = ', '.join(languages)
            repos_df.loc[i, 'Languages'] = languages
        else:
            repos_df.loc[i, 'Languages'] = ""
    print("Language data collection complete")
    repos_df.to_csv('repos_info.csv', index = False)
    print("Saved repositories information to repo_info.csv\n")

    print("Collecting commits information")
    commits_information = []
    for i in range(repos_df.shape[0]):
        url = repos_df.loc[i, 'Commits URL']
        page_no = 1
        while (True):
            response = requests.get(url, auth=authentication)
            response = response.json()
            print("URL: {}, commits: {}".format(url, len(response)))
            for commit in response:
                commit_data = []
                commit_data.append(repos_df.loc[i, 'Id'])
                commit_data.append(repos_df.loc[i, 'Name'])
                commit_data.append(str(commit['sha']))
                commit_data.append(commit['commit']['committer']['date'])
                commits_information.append(commit_data)
            if (len(response) == 30):
                page_no = page_no + 1
                url = repos_df.loc[i, 'Commits URL'] + '?page=' + str(page_no)
            else:
                break

    commits_df = pd.DataFrame(commits_information, columns = ['Repo Id', 'Repo Name', 'Commit Id', 'Date'])
    commits_df.to_csv('commits_info.csv', index = False)
    print("Saved commits information to commits_info.csv")


if __name__ == "__main__":
    data_to_csv()