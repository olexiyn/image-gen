from sanic import Blueprint, Sanic
from sanic import SanicException, json
from sanic_ext import render

my_app = Sanic.get_app()
my_auth = my_app.config.BASIC_AUTH
blueprint = Blueprint('imgroot', url_prefix='/')

@blueprint.get('/')
@my_auth.login_required
async def main_root(request):
    return await render("index.html", context={}, status=200)

@blueprint.get('/image-gen')
@my_auth.login_required
async def image_gen_root(request):
    return await render("imggen.html", context={}, status=200)

@blueprint.get('/healthcheck')
async def healthcheck(request):
    return json({'status':'OK'})
