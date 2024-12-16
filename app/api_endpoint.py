from sanic import Blueprint, Sanic, json, raw
from sanic import SanicException
from app.utils import content_gen, image_gen, upscale, save_in_cloud
import random
import string
from io import BytesIO
import boto3

my_app = Sanic.get_app()
my_auth = my_app.config.BASIC_AUTH
blueprint = Blueprint('apiroot', url_prefix='/api')


@blueprint.get('/', name='apiroot_dogs')
@my_auth.login_required
async def main_root(request):
    if request.args.get('topic'):
        topic = request.args.get('topic')
    else:
        topic = 'Dogs'
    json_prompts = await content_gen(topic)
    return json(json_prompts)


@blueprint.get('/imggen', name='img_gen')
@my_auth.login_required
async def img_gen(request):
    if request.args.get('prompt'):
        prompt = request.args.get('prompt')
        print(prompt)
    else:
        prompt = 'Cats'
    img = image_gen(prompt)
    if not img:
        return json({'error': 'no images generated'})
    temp_png = BytesIO()
    img[0]._pil_image.save(temp_png, format='PNG')
    return raw(content_type='image/png', body=temp_png.getvalue())


@blueprint.get('/imggen-url', name='img_gen_url')
@my_auth.login_required
async def img_gen_url(request):
    if request.args.get('prompt'):
        prompt = request.args.get('prompt')
        print(prompt)
    else:
        prompt = 'Cats'
        
    img = image_gen(prompt)
    if not img:
        return json({'error': 'no images generated'})
    temp_png = BytesIO()
    img[0]._pil_image.save(temp_png, format='PNG')
    url = await save_in_cloud(temp_png.getvalue(), 'png')
    return json({'url': url})

@blueprint.get('/upscale', name='img_upscale')
@my_auth.login_required
async def img_upscale(request):
    imaage_url = request.args.get('url')
    scale = request.args.get('scale')
    result = await upscale(image_url=imaage_url, scale=scale)
    return json(result)