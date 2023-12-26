
import urllib.request
import json

#documentation of endpoints https://docs.github.com/en/rest/overview/endpoints-available-for-fine-grained-personal-access-tokens
def get_github_user_repositories(username):
    repos = []
    urls = [
        #documentation of endpoint https://docs.github.com/en/rest/repos/repos
        'https://api.github.com/users/{}/repos?sort=pushed&per_page=100&direction=desc'.format(username),
        # 'https://api.github.com/users/{}/gists'.format(username)
        ]
    for url in urls:
        webUrl  = urllib.request.urlopen(url)
        data = webUrl.read()
        json_data = json.loads(data)
        owner = json_data[0]['owner']
        for repo in json_data:
            repo.pop('owner',None)
            # for key in [key for key in repo.keys() if "_url" in key]:
                # repo.pop(key,None)
        repos += [repo for repo in json_data if repo.get('fork',False) == False]
    return owner,repos
