import os

from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from flask import Flask, redirect, session

from rc_api import get_user_profile
from rc_oauth_utils import get_rc_oauth

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]


@app.route("/")
def index():
    return 'this is disco.recurse.com!!! <a href="/dashboard">login</a>'


@app.route("/dashboard")
def dashboard():
    if session.get("rc_user") is None:
        return get_rc_oauth(app).authorize_redirect(os.environ["RC_OAUTH_REDIRECT_URI"])
    return f"this is the disco recurse dashboard! hi {session['rc_user']['user']['first_name']}! <a href='/logout'>logout</a>"


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
    # redirect to /dashboard
    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session["rc_user"] = None
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
