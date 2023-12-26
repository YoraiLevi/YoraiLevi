# Creates README.md
import urllib.request
import json
from github_api import get_github_user_repositories
from svg import populate_svg_template

owner, repos = get_github_user_repositories("YoraiLevi")
repos = list(filter(lambda repo: not repo.get("archived", False), repos))
repos.sort(key=lambda repo: (repo.get("updated_at", None)), reverse=True)
repo_cards = ""
for index, repo in enumerate(repos[:6]):
    # Description
    name = repo.get("name") or "gist: " + repr(list(repo["files"].keys()))
    description = repo.get("description")
    language = repo.get("language")
    html_url = repo.get("html_url")
    homepage = repo.get("homepage")
    topics = repo.get("topics")

    # # Popularities and stats
    stargazers_count = repo.get("stargazers_count", 0)
    watchers_count = repo.get("watchers_count", 0)
    forks_count = repo.get("forks_count", 0)
    open_issues_count = repo.get("open_issues_count", 0)
    has_issues = repo.get("has_issues", False)
    has_projects = repo.get("has_projects", False)
    has_discussions = repo.get("has_discussions", False)

    # # Maintenence
    created_at = repo.get("created_at", None)
    pushed_at = repo.get("pushed_at", None)
    updated_at = repo.get("updated_at", None)

    has_downloads = repo.get("has_downloads", False)
    has_wiki = repo.get("has_wiki", False)
    has_pages = repo.get("has_pages", False)
    archived = repo.get("archived", False)

    with open(f"card-dark-{index}.svg", "w") as f:
        f.write(populate_svg_template(repo, dark_mode=True))
    with open(f"card-light-{index}.svg", "w") as f:
        f.write(populate_svg_template(repo, dark_mode=False))
    repo_card = f"""
<a href="{html_url}">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./card-dark-{index}.svg">
  <source media="(prefers-color-scheme: light)" srcset="./card-light-{index}.svg">
  <img align="center" src="./card-dark-{index}.svg" />
</picture>\
</a>"""
    repo_cards += repo_card
print("[repository list](REPOS.md)")
print('<p align="center">')
print(repo_cards)
print()
print("![](resources/README/header_image.jpg)")
print("</p>")