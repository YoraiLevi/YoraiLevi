# Creates README.md
import urllib.request
import json
import github
from svg import populate_svg_template

username = 'YoraiLevi'
repos = github.get_authenticated_repositories()
repos = list(filter(lambda repo: not repo.get("fork", False), repos))
repos = list(filter(lambda repo: not repo.get("archived", False), repos))
repos.sort(key=lambda repo: (repo.get("updated_at", None)), reverse=True)
repo_cards = ""
for index, repo in enumerate(repos[:6]):
    html_url = repo.get("html_url")
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
