# Creates README.md
import urllib.request
import json

def get_github_user_repositories(username):
    repos = []
    urls = [
        'https://api.github.com/users/{}/repos'.format(username),
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
owner,repos = get_github_user_repositories("YoraiLevi")
repos.sort(key=lambda repo: (repo.get('updated_at',None)),reverse=True)
repo_cards = ""
for repo in repos[:6]:
    # Description
    name = repo.get('name') or "gist: "+repr(list(repo['files'].keys()))
    description = repo.get('description')
    language = repo.get('language')
    html_url = repo.get('html_url')
    homepage = repo.get('homepage')
    topics = repo.get('topics')
    
    # # Popularities and stats
    stargazers_count = repo.get('stargazers_count',0)
    watchers_count = repo.get('watchers_count',0)
    forks_count = repo.get('forks_count',0)
    open_issues_count = repo.get('open_issues_count',0)
    has_issues = repo.get('has_issues',False)
    has_projects = repo.get('has_projects',False)
    has_discussions = repo.get('has_discussions',False)
    
    
    # # Maintenence
    created_at = repo.get('created_at',None)
    pushed_at = repo.get('pushed_at',None)
    updated_at = repo.get('updated_at',None)

    has_downloads = repo.get('has_downloads',False)
    has_wiki = repo.get('has_wiki',False)
    has_pages = repo.get('has_pages',False)
    archived = repo.get('archived',False)
    repo_card = f'''
<a href="{html_url}">
<img align="center" src="https://github-readme-stats-one-theta-17.vercel.app/api/pin/?username={owner['login']}&repo={name}&theme=github_dark&max_lines=2" />\
</a>'''
    repo_cards+=repo_card

print('<p align="center">')
print(repo_cards)
print()
print("![](resources/README/header_image.jpg)")
print("</p>")
