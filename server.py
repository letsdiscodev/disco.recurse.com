from dotenv import load_dotenv

# call before any imports
load_dotenv()

import os
import random
import sqlite3

from flask import Flask, redirect, render_template, session

from utils.db import (
    get_invite_for_recurse_user_id,
    insert_invite_for_recurse_user_id,
    remove_invite_for_recurse_user_id,
)
from utils.disco_api import (
    InviteAlreadyExistsForUser,
    generate_invite_get_id,
    get_api_keys,
)
from utils.rc_api import get_user_profile
from utils.rc_oauth_utils import get_rc_oauth

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    if session.get("rc_user") is None:
        return get_rc_oauth(app).authorize_redirect(os.environ["RC_OAUTH_REDIRECT_URI"])

    disco_api_keys = get_api_keys()["apiKeys"]

    print("disco_api_keys", disco_api_keys)
    # try to find the user in the existing api keys
    looking_for_api_key_name = f"recurse-user-{session['rc_user']['user']['id']}"
    disco_api_keys = [
        key for key in disco_api_keys if key["name"] == looking_for_api_key_name
    ]

    found_api_key = None
    if disco_api_keys:
        found_api_key = disco_api_keys[0]
        remove_invite_for_recurse_user_id(session["rc_user"]["user"]["id"])

    found_invite_url = None
    if not found_api_key:
        # is there an existing invite in the db?
        found_invite = get_invite_for_recurse_user_id(session["rc_user"]["user"]["id"])
        if found_invite:
            found_invite_url = found_invite["invite_url"]

    # if no api key found and no invite in the db, generate new invite and store it
    if not found_api_key and not found_invite_url:
        found_invite = generate_invite_get_id(session["rc_user"]["user"]["id"])
        found_invite_url = found_invite["apiKeyInvite"]["url"]
        insert_invite_for_recurse_user_id(
            session["rc_user"]["user"]["id"], found_invite_url
        )

    return render_template(
        "dashboard.html",
        user=session["rc_user"]["user"],
        found_api_key=found_api_key,
        found_invite_url=found_invite_url,
    )


@app.route("/oauth_redirect")
def oauth_redirect():
    rc_oauth = get_rc_oauth(app)
    try:
        token = rc_oauth.authorize_access_token()
    except:
        return 'could not log you in. <a href="/dashboard">try again?</a>'
    user = get_user_profile(token["access_token"])
    session["rc_user"] = {
        "token": token,
        "user": user,
    }
    return redirect("/dashboard")


# @app.route("/generate_invite")
# def generate_invite_view():
#     if session.get("rc_user") is None:
#         return get_rc_oauth(app).authorize_redirect(os.environ["RC_OAUTH_REDIRECT_URI"])

#     generate_invite(session["rc_user"]["user"]["id"])
#     return redirect("/dashboard")


@app.route("/logout")
def logout():
    session["rc_user"] = None
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
