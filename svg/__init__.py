import urllib.request
import json

url = "https://raw.githubusercontent.com/anuraghazra/github-readme-stats/master/src/common/languageColors.json"
webUrl  = urllib.request.urlopen(url)
data = webUrl.read()
github_languageColors_json = json.loads(data)

from string import Template
with open('./svg/template.svg','r') as f:
    card_svg_template = Template(f.read())

def populate_svg_template(repo):
    name = repo.get("name") or "gist: " + repr(list(repo["files"].keys()))
    description = repo.get("description") or ''
    language = repo.get("language") or ''
    archived = repo.get('archived',False)
    # # Popularities and stats
    stargazers_count = repo.get("stargazers_count", 0)
    forks_count = repo.get("forks_count", 0)

    repo = {
        "name": name,
        "description": description,
        "language": language,
        "language_color": github_languageColors_json.get(language),
        "stargazers_count": stargazers_count,
        "forks_count": forks_count,
        "archived" : '' if archived else 'hide',
        "not_archived" : 'hide' if archived else '',
    }
    return card_svg_template.substitute(repo)