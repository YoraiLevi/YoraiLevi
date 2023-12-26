import urllib.request
import json
from github import Repository
url = "https://raw.githubusercontent.com/anuraghazra/github-readme-stats/master/src/common/languageColors.json"
webUrl = urllib.request.urlopen(url)
data = webUrl.read()
github_languageColors_json = json.loads(data)

from string import Template

with open("./svg/template.svg", "r") as f:
    card_svg_template = Template(f.read())
with open("./svg/dark_mode.css", "r") as f:
    dark_mode_css = f.read()
with open("./svg/light_mode.css", "r") as f:
    light_mode_css = f.read()


def populate_svg_template(repo : Repository, dark_mode=True):
    name = repo.get("name")
    description = repo.get("description") or ""
    language = repo.get("language") or ""
    archived = repo.get("archived", False)
    stargazers_count = repo.get("stargazers_count", 0)
    forks_count = repo.get("forks_count", 0)

    _repo = {
        "name": name,
        "description": description,
        "language": language,
        "language_color": github_languageColors_json.get(language),
        "stargazers_count": stargazers_count,
        "forks_count": forks_count,
        "archived": "" if archived else "hide",
        "not_archived": "hide" if archived else "",
        "color_scheme": dark_mode_css if dark_mode else light_mode_css,
    }
    return card_svg_template.substitute(_repo)
