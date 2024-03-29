from string import Template
from typing import TypedDict, Optional
from functools import partial
import urllib.request
import json
import os

"""
documentation of endpoints https://docs.github.com/en/rest/overview/endpoints-available-for-fine-grained-personal-access-tokens
"""


class Gist(TypedDict):
    # url: str
    # forks_url: str
    # commits_url: str
    # id: str
    # node_id: str
    # git_pull_url: str
    # git_push_url: str
    html_url: str
    files: dict
    public: bool
    created_at: str
    updated_at: str
    description: str
    # comments: int
    # comments_url: str
    owner: dict
    # truncated: bool
    stargazers_count: int  # populated by _populate_gist_stargazersCount_forks
    forks_count: int # populated by _populate_gist_stargazersCount_forks


class Repository(TypedDict):
    # id: int
    # node_id: str
    name: str
    full_name: str
    private: bool
    html_url: str
    description: Optional[str]
    fork: bool
    url: str
    # forks_url: str
    # keys_url: str
    # collaborators_url: str
    # teams_url: str
    # hooks_url: str
    # issue_events_url: str
    # events_url: str
    # assignees_url: str
    # branches_url: str
    # tags_url: str
    # blobs_url: str
    # git_tags_url: str
    # git_refs_url: str
    # trees_url: str
    # statuses_url: str
    # languages_url: str
    # stargazers_url: str
    # contributors_url: str
    # subscribers_url: str
    # subscription_url: str
    # commits_url: str
    # git_commits_url: str
    # comments_url: str
    # issue_comment_url: str
    # contents_url: str
    # compare_url: str
    # merges_url: str
    # archive_url: str
    # downloads_url: str
    # issues_url: str
    # pulls_url: str
    # milestones_url: str
    # notifications_url: str
    # labels_url: str
    # releases_url: str
    # deployments_url: str
    created_at: str
    updated_at: str
    pushed_at: str
    # git_url: str
    # ssh_url: str
    # clone_url: str
    # svn_url: str
    homepage: Optional[str]
    # size: int
    stargazers_count: int
    watchers_count: int
    language: str
    # has_issues: bool
    # has_projects: bool
    # has_downloads: bool
    # has_wiki: bool
    # has_pages: bool
    # has_discussions: bool
    forks_count: int
    # mirror_url: Optional[str]
    archived: bool
    disabled: bool
    open_issues_count: int
    license: Optional[str]
    allow_forking: bool
    is_template: bool
    # web_commit_signoff_required: bool
    # topics: list
    visibility: str
    # forks: int
    # open_issues: int
    # watchers: int
    default_branch: str
    # permissions: dict


class User(TypedDict):
    login: str
    # id: int
    # node_id: str
    avatar_url: str
    # gravatar_id: str
    # url: str
    html_url: str
    # followers_url: str
    # following_url: str
    # gists_url: str
    # starred_url: str
    # subscriptions_url: str
    # organizations_url: str
    # repos_url: str
    # events_url: str
    # received_events_url: str
    # type: str
    # site_admin: bool


def _fetch_json(url):
    api_token = os.getenv("USER_TOKEN")
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {api_token}")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    data = urllib.request.urlopen(req).read()
    json_data = json.loads(data)
    return json_data


def _query_graphql(graphql_query):
    url = "https://api.github.com/graphql"
    api_token = os.getenv("USER_TOKEN")
    query = {"query": graphql_query}
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    req = urllib.request.Request(url, json.dumps(query).encode("utf-8"), headers)
    req.add_header("Authorization", f"Bearer {api_token}")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    data = urllib.request.urlopen(req).read()
    json_data = json.loads(data)
    try:
        return json_data["data"]
    except KeyError:
        raise json_data


def _populate_gist_stargazersCount_forks(gists: list[Gist]):
    def _gists_stargzers_graphql_query(gists: list[Gist]):
        template_gist_query = Template(
            """gist_$id : gist(name : "$id"){
        stargazerCount
        forks {
            totalCount
        }
    }"""
        )
        template_query = Template(
            """query {
        viewer {
    $query
        }
    }"""
        )
        graphql_query = template_query.substitute(
            query="\n".join(template_gist_query.substitute(**gist) for gist in gists)
        )
        return graphql_query

    graphql_query = _gists_stargzers_graphql_query(gists)
    graphql_data = _query_graphql(graphql_query)
    for gist in gists:
        data = graphql_data["viewer"]["gist_" + gist["id"]]
        gist["stargazers_count"] = data["stargazerCount"]
        gist["forks_count"] = data["forks"]["totalCount"]
    return gists


def _filter_keys(annotated_type, d):
    return {key: d[key] for key in annotated_type.__annotations__.keys()}


def get_user_repositories(username) -> list[Repository]:
    """
    https://docs.github.com/en/rest/repos/repos#list-repositories-for-a-user
    """
    annotated_type = Repository
    url_template = Template(
        "https://api.github.com/users/$username/repos?sort=pushed&per_page=100&direction=desc"
    )
    url = url_template.substitute(username=username)
    json_data = _fetch_json(url)
    for repo in json_data:
        repo.pop("owner", None)
    return list(map(partial(_filter_keys, annotated_type), json_data))


def get_user_gists(username) -> list[Gist]:
    """
    https://docs.github.com/en/rest/gists/gists#list-gists-for-a-user
    """
    annotated_type = Gist
    url_template = Template("https://api.github.com/users/$username/gists?per_page=100")
    url = url_template.substitute(username=username)
    json_data = _fetch_json(url)
    json_data = _populate_gist_stargazersCount_forks(json_data)
    json_data = list(filter(lambda gist: gist.get("public", False), json_data))
    return list(map(partial(_filter_keys, annotated_type), json_data))


def get_user_starred_repositories(username) -> list[Repository]:
    """
    https://docs.github.com/en/rest/activity/starring#list-repositories-starred-by-a-user
    """
    annotated_type = Repository
    url_template = Template(
        "https://api.github.com/users/$username/starred?per_page=100&sort=created&direction=desc"
    )
    url = url_template.substitute(username=username)
    json_data = _fetch_json(url)
    return list(map(partial(_filter_keys, annotated_type), json_data))


def get_user_followers(username) -> list[User]:
    """
    https://docs.github.com/en/rest/users/followers#list-followers-of-a-user
    """
    annotated_type = User
    url_template = Template(
        "https://api.github.com/users/$username/followers?per_page=100"
    )
    url = url_template.substitute(username=username)
    json_data = _fetch_json(url)
    return list(map(partial(_filter_keys, annotated_type), json_data))


def get_user_following(username) -> list[User]:
    """
    https://docs.github.com/en/rest/users/followers#list-the-people-a-user-follows
    """
    url_template = Template(
        "https://api.github.com/users/$username/following?per_page=100"
    )
    annotated_type = User
    url = url_template.substitute(username=username)
    json_data = _fetch_json(url)
    return list(map(partial(_filter_keys, annotated_type), json_data))


def get_user_social_accounts(username):
    """
    https://docs.github.com/en/rest/users/social-accounts#list-social-accounts-for-a-user
    """
    annotated_type = User
    url_template = Template(
        "https://api.github.com/users/$username/social_accounts?per_page=100"
    )
    url = url_template.substitute(username=username)
    json_data = _fetch_json(url)
    return list(map(partial(_filter_keys, annotated_type), json_data))


def get_authenticated_gists() -> list[Gist]:
    """
    https://docs.github.com/en/rest/gists/gists#list-gists-for-the-authenticated-user
    """
    annotated_type = Gist
    url_template = Template("https://api.github.com/gists?per_page=100")
    url = url_template.substitute()
    json_data = _fetch_json(url)
    json_data = _populate_gist_stargazersCount_forks(json_data)
    json_data = list(filter(lambda gist: gist.get("public", False), json_data))
    return list(map(partial(_filter_keys, annotated_type), json_data))


def get_authenticated_starred_gists() -> list[Gist]:
    """
    https://docs.github.com/en/rest/gists/gists#list-starred-gists
    """
    annotated_type = Gist
    url_template = Template("https://api.github.com/gists/starred?per_page=100")
    url = url_template.substitute()
    json_data = _fetch_json(url)
    json_data = _populate_gist_stargazersCount_forks(json_data)
    json_data = list(filter(lambda gist: gist.get("public", False), json_data))
    return list(map(partial(_filter_keys, annotated_type), json_data))


def get_authenticated_repositories() -> list[Repository]:
    """
    https://docs.github.com/en/rest/repos/repos#list-repositories-for-the-authenticated-user
    """
    annotated_type = Repository
    url_template = Template(
        "https://api.github.com/user/repos?per_page=100&visibility=public&sort=pushed&direction=desc"
    )
    url = url_template.substitute()
    json_data = _fetch_json(url)
    return list(map(partial(_filter_keys, annotated_type), json_data))


def get_authenticated_starred_repositories() -> list[Repository]:
    """
    https://docs.github.com/en/rest/activity/starring#list-repositories-starred-by-the-authenticated-user
    """
    annotated_type = Repository
    url_template = Template(
        "https://api.github.com/user/starred?sort=created&per_page=100&direction=desc"
    )
    url = url_template.substitute()
    json_data = _fetch_json(url)
    json_data = list(filter(lambda gist: not gist.get("private", False), json_data))
    return list(map(partial(_filter_keys, annotated_type), json_data))

def get_authenticated_pullrequests(status: str):
    # MERGED, OPEN, CLOSED
    graphql_query_template = Template("""
query {
  viewer {
    login
    pullRequests (last :100, states: $status) {
      nodes {
        url
        title
        changedFiles
        additions
        deletions
        repository {
          isPrivate
          nameWithOwner
          name
          owner {
            login
          }
        }
      }
    }
  }
}""")
    graphql_query = graphql_query_template.substitute(status=status)
    data = _query_graphql(graphql_query)
    authenticated_login = data['viewer']['login']
    pull_requests = data['viewer']['pullRequests']['nodes']
    pull_requests = list(filter(lambda x: x['repository']['owner']['login'] != authenticated_login, pull_requests))
    pull_requests = list(filter(lambda x: x['repository']['isPrivate'] == False, pull_requests))
    return pull_requests