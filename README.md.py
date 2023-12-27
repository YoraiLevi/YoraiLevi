try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    pass

import github
from svg import populate_svg_template


def repolike_card(repolike, card_name_suffix):
    html_url = repo.get("html_url")
    dark_svg = populate_svg_template(repolike, dark_mode=True)
    dark_svg_name = f"card-dark-{card_name_suffix}.svg"
    light_svg = populate_svg_template(repolike, dark_mode=False)
    light_svg_name = f"card-light-{card_name_suffix}.svg"

    markdown_display_string = f"""
<a href="{html_url}">
<picture>
<source media="(prefers-color-scheme: dark)" srcset="./{dark_svg_name}/">
<source media="(prefers-color-scheme: light)" srcset="./{light_svg_name}/">
<img align="center" src="./{dark_svg_name}" />
</picture>\
</a>"""
    return (
        dark_svg,
        dark_svg_name,
        light_svg,
        light_svg_name,
        markdown_display_string,
    )


if __name__ == "__main__":
    repos = github.get_authenticated_repositories()
    gists = github.get_authenticated_gists()

    for gist in gists:
        file = next(iter(gist["files"].items()))
        gist["name"] = file[0]
        gist["language"] = file[1]["language"]

    user_items = repos + gists
    user_items = list(filter(lambda repo: not repo.get("fork", False), user_items))
    # user_items = list(filter(lambda repo: not repo.get("archived", False), user_items))
    user_items.sort(key=lambda repo: (repo.get("updated_at", None)), reverse=True)
    recently_updated_repo_cards = ""
    for index, repo in enumerate(user_items[:6]):
        (
            dark_svg,
            dark_svg_name,
            light_svg,
            light_svg_name,
            markdown_display_string,
        ) = repolike_card(repo, card_name_suffix=index)

        with open(dark_svg_name, "w") as f:
            f.write(dark_svg)
        with open(light_svg_name, "w") as f:
            f.write(light_svg)
        recently_updated_repo_cards += markdown_display_string
    # gists don't show stars :(
    user_items.sort(key=lambda repo: (repo.get("stargazers_count", 0)), reverse=True)
    most_starred_repo_cards = ""
    for index, repo in enumerate(user_items[:4]):
        (
            dark_svg,
            dark_svg_name,
            light_svg,
            light_svg_name,
            markdown_display_string,
        ) = repolike_card(repo, card_name_suffix=f"starred-{index}")

        with open(dark_svg_name, "w") as f:
            f.write(dark_svg)
        with open(light_svg_name, "w") as f:
            f.write(light_svg)
        most_starred_repo_cards += markdown_display_string
    links = {
        "📘repositories": "./REPOS.md#repositories-and-gists",
        "⭐starred": "./STARRED.md#starred",
    }
    links_menu = "    ".join([f"[{key}]({value})" for key, value in links.items()])
    print(links_menu)
    ###
    print()
    print('<p align="center">')
    print(recently_updated_repo_cards)
    print()
    print("</p>")
    print()
    ###
    print("# My Most Starred")
    print()
    print('<p align="center">')
    print(most_starred_repo_cards)
    print()
    print("</p>")
    print()
    ###
    print('<p align="center">')
    print()
    print("![](resources/README/header_image.jpg)")
    print()
    print("</p>")
    print()
    ###
