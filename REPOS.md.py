try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    pass

import datetime
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
    user_gists: list[Gist] = github.get_authenticated_gists()
    repos: list[Repository] = github.get_authenticated_repositories()

    user_repos = list(filter(lambda repo: not repo.get("fork", False), repos))
    user_forks = list(filter(lambda repo: repo.get("fork", False), repos))
    for gist in user_gists:
        gist["name"] = next(iter(gist["files"].keys()))

    user_items = user_repos + user_gists

    user_items.sort(key=lambda item: (item.get("updated_at", None)), reverse=True)
    print("## Repositories and Gists")
    for repo in user_items:
        print(f"- {repolike2str(repo)}  ")
    print("## Forks")
    for repo in user_forks:
        print(f"- {repolike2str(repo)}  ")
    
    print("  ")
    print(datetime.datetime.now(datetime.timezone.utc).isoformat())
