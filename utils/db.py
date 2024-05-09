import os
import sqlite3

from flask import g

SQLITE_DB_PATH = os.environ["DB_PATH"]


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(SQLITE_DB_PATH)
        g.db.row_factory = sqlite3.Row

    # create table if not exists
    # we want a table with invite_url and recurse_user_id
    g.db.execute(
        "CREATE TABLE IF NOT EXISTS invites (invite_url TEXT PRIMARY KEY, recurse_user_id TEXT)"
    )

    return g.db


def get_invite_for_recurse_user_id(recurse_user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT invite_url FROM invites WHERE recurse_user_id = ?", (recurse_user_id,)
    )
    return cursor.fetchone()


def insert_invite_for_recurse_user_id(recurse_user_id, invite_url):
    db = get_db()
    db.execute(
        "INSERT INTO invites (invite_url, recurse_user_id) VALUES (?, ?)",
        (invite_url, recurse_user_id),
    )
    db.commit()


def remove_invite_for_recurse_user_id(recurse_user_id):
    db = get_db()
    db.execute("DELETE FROM invites WHERE recurse_user_id = ?", (recurse_user_id,))
    db.commit()
