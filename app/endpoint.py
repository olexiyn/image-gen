from sanic import Blueprint
from sanic import SanicException
from sanic_ext import render

blueprint = Blueprint('imgroot', url_prefix='/')

@blueprint.get('/')
async def main_root(request):
    return await render("index.html", context={}, status=200)
