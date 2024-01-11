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

    print("## My Contributions")
    pull_requests = github.get_authenticated_pullrequests("MERGED")
    def pull_request2markdown(pull_request):
        # 2 files changed, 3 insertions(+), 11 deletions(-)
        return f"""[{pull_request['repository']['nameWithOwner']}]({pull_request['url']}) {pull_request['changedFiles']} files changed, {pull_request['additions']} insertions(+), {pull_request['deletions']} deletions(-)"""
    markdown = list(map(pull_request2markdown, pull_requests))
    for m in markdown:
        print(m, end='  \n')
    pull_requests = github.get_authenticated_pullrequests("OPEN")
    if(len(pull_requests) > 0):
        print("### TBD Contributions")
        markdown = list(map(pull_request2markdown, pull_requests))
        for m in markdown:
            print(m, end='  \n')