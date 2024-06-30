import os

from flask import g
from supabase.client import Client, ClientOptions
from werkzeug.local import LocalProxy

from flask_storage import FlaskSessionStorage

url = os.environ.get("SUPABASE_URL", "")
key = os.environ.get("SUPABASE_KEY", "")


def get_supabase() -> Client:
    if "supabase" not in g:
        g.supabase = Client(
            url,
            key,
            options=ClientOptions(
                storage=FlaskSessionStorage(),
                flow_type="pkce"
            ),
        )
    return g.supabase


supabase: Client = LocalProxy(get_supabase)
