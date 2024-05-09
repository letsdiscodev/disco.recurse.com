import os

import requests

# set in .env on dev, and automatically by the environment on prod
# does NOT include the protocol i.e. is just "example.com", not "https://example.com"
DISCO_HOST = os.environ["DISCO_HOST"]
DISCO_API_KEY = os.environ["DISCO_API_KEY"]


class DiscoApiError(Exception):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code


class InviteAlreadyExistsForUser(DiscoApiError):
    pass


def _query(api_url, method, json_post_body=None):
    url = f"https://{DISCO_HOST}{api_url}"
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
    return _query("/api/api-keys", "GET")


def generate_invite_get_id(recurse_user_id):
    body = {"name": f"recurse-user-{recurse_user_id}"}
    try:
        return _query("/api/api-key-invites", "POST", json_post_body=body)
    except DiscoApiError as e:
        if (
            e.status_code == 422
            and str(e) == "API Key name already used in other invite"
        ):
            raise InviteAlreadyExistsForUser(
                "API Key name already used in other invite"
            )
        raise e
