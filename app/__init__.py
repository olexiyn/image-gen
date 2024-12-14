from sanic import Sanic, Blueprint
import hashlib
from sanic_httpauth import HTTPBasicAuth
import os

app = Sanic('image-gen', env_prefix="IMGGEN_")
auth = HTTPBasicAuth()
app.config.BASIC_AUTH = auth

from app.root_endpoint import blueprint as root_bp
from app.api_endpoint import blueprint as api_bp

def hash_password(salt, password):
    salted = password + salt
    return hashlib.sha512(salted.encode("utf8")).hexdigest()

app_salt = os.getenv('APP_SALT')
if not app_salt:
    print("error: no salt")
    exit(1)

users = {
    os.getenv('ADMIN_LOGIN'): hash_password(app_salt, os.getenv('ADMIN_PASSWORD')),
    os.getenv('CLIENT_LOGIN'): hash_password(app_salt, os.getenv('CLIENT_PASSWORD')),
}

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return users.get(username) == hash_password(app_salt, password)
    return False

def init_app(app):
    app.config.FALLBACK_ERROR_FORMAT = "text"  
    app_bp = Blueprint.group([root_bp, api_bp,], version_prefix='/')
    app.blueprint(app_bp)
