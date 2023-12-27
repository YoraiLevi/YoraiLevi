try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    pass

import github
from github import Gist, Repository


def repolike2str(repo: Repository):
    # print(  + "+ +"  ")

    archived = repo.get("archived", False)
    description = repo.get("description")
    name = repo.get("name")
    html_url = repo.get("html_url")

    string_archived = "Archived: " if archived else ""
    string_name = f"[{name}]({html_url})"
    string_description = f" - {description}" if description else ""

    s = f"{string_archived}{string_name}{string_description}"
    return s


if __name__ == "__main__":
    starred_gists: list[Gist] = github.get_authenticated_starred_gists()
    starred_repos: list[Repository] = github.get_authenticated_starred_repositories()

    for gist in starred_gists:
        gist["name"] = next(iter(gist["files"].keys()))

    user_starred = starred_repos + starred_gists

    # user_starred.sort(key=lambda item: (item.get("forks_count", None)), reverse=True)
    print("## Starred")
    for repo in user_starred:
        print(f"- {repolike2str(repo)}  ")
