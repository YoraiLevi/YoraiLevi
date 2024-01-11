try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    pass

import github
from github import Gist, Repository


def pull_request2markdown(pull_request):
    # 2 files changed, 3 insertions(+), 11 deletions(-)
    return f"""{pull_request['changedFiles']} files changed, {pull_request['additions']} insertions(+), {pull_request['deletions']} deletions(-) [{pull_request['repository']['nameWithOwner']}]({pull_request['url']}) -- {pull_request['title']}"""


if __name__ == "__main__":
    pull_requests = github.get_authenticated_pullrequests("OPEN")
    if len(pull_requests) > 0:
        print("## TBD Contributions")
        print()
        markdown = list(map(pull_request2markdown, pull_requests))
        for m in markdown:
            print(m, end="  \n")
        print()

    pull_requests = github.get_authenticated_pullrequests("MERGED")
    if len(pull_requests) > 0:
        print("## My Contributions")
        print()
        markdown = list(map(pull_request2markdown, pull_requests))
        for m in markdown:
            print(m, end="  \n")
        print()

    pull_requests = github.get_authenticated_pullrequests("CLOSED")
    if len(pull_requests) > 0:
        print("### Things that didn't see the light of day")
        print()
        markdown = list(map(pull_request2markdown, pull_requests))
        for m in markdown:
            print(m, end="  \n")
        print()
