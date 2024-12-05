from sanic import Sanic, Blueprint
from app.endpoint import blueprint as root_bp

app = Sanic('image-gen', env_prefix="IMGEN_")

def init_app(app):
    app.config.FALLBACK_ERROR_FORMAT = "text"
    app_bp = Blueprint.group([root_bp,], version_prefix='/')
    app.blueprint(app_bp)
