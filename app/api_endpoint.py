from sanic import Blueprint, json, raw
from sanic import SanicException
from app.utils import content_gen, image_gen
from io import BytesIO

blueprint = Blueprint('apiroot', url_prefix='/api')


@blueprint.get('/', name='apiroot_dogs')
async def main_root(request):
    if request.args.get('topic'):
        topic = request.args.get('topic')
    else:
        topic = 'Dogs'
    return json(content_gen(topic))


@blueprint.get('/imggen', name='img_gen')
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
async def img_gen_url(request):
    if request.args.get('prompt'):
        prompt = request.args.get('prompt')
        print(prompt)
    else:
        prompt = 'Cats'
    s3_endpoint = request.app.config.get('S3_ENDPOINT')
    s3_access_key = request.app.config.get('S3_ACCESS_KEY')
    s3_secret_key = request.app.config.get('S3_SECRET_KEY')
    img = image_gen(prompt)
    if not img:
        return json({'error': 'no images generated'})
    temp_png = BytesIO()
    img[0]._pil_image.save(temp_png, format='PNG')
    return raw(content_type='image/png', body=temp_png.getvalue())
    return json({'url': url})
