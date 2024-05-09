import os

import requests

DISCO_HOST = os.environ["DISCO_HOST"]
DISCO_API_KEY = os.environ["DISCO_API_KEY"]


class DiscoApiError(Exception):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code


class InviteAlreadyExistsForUser(DiscoApiError):
    pass


def _query(url, method, json_post_body=None):
    if method == "GET":
        r = requests.get(
            url,
            auth=(DISCO_API_KEY, ""),
            headers={"Accept": "application/json"},
        )
    elif method == "POST":
        r = requests.post(
            url,
            json=json_post_body,
            auth=(DISCO_API_KEY, ""),
            headers={"Accept": "application/json"},
        )
    else:
        raise Exception("method not supported")

    if not r.ok:
        try:
            raise DiscoApiError(r.json()["detail"][0]["msg"], status_code=r.status_code)
        except:
            raise DiscoApiError(r.text, status_code=r.status_code)

    return r.json()


def get_api_keys():
    query_url = "/api/api-keys"
    return _query(f"{DISCO_HOST}{query_url}", "GET")


def generate_invite_get_id(recurse_user_id):
    query_url = "/api/api-key-invites"
    body = {"name": f"recurse-user-{recurse_user_id}"}
    try:
        return _query(f"{DISCO_HOST}{query_url}", "POST", json_post_body=body)
    except DiscoApiError as e:
        if (
            e.status_code == 422
            and str(e) == "API Key name already used in other invite"
        ):
            raise InviteAlreadyExistsForUser(
                "API Key name already used in other invite"
            )
        raise e
