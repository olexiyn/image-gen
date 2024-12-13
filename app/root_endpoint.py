from sanic import Blueprint
from sanic import SanicException, json
from sanic_ext import render

blueprint = Blueprint('imgroot', url_prefix='/')

@blueprint.get('/')
async def main_root(request):
    return await render("index.html", context={}, status=200)


@blueprint.get('/image-gen')
async def image_gen_root(request):
    return await render("imggen.html", context={}, status=200)

@blueprint.get('/healthcheck')
async def healthcheck(request):
    return json({'status':'OK'})
