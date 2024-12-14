from sanic import Blueprint, Sanic, json, raw
from sanic import SanicException
from app.utils import content_gen, image_gen
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
    s3_endpoint = request.app.config.get('S3_ENDPOINT')
    s3_access_key = request.app.config.get('S3_ACCESS_KEY')
    s3_secret_key = request.app.config.get('S3_SECRET_KEY')
    s3_bucket_name = request.app.config.get('S3_BUCKET_NAME')
    s3_image_storage_url = request.app.config.get('S3_IMAGE_STORAGE_URL')
    img = image_gen(prompt)
    if not img:
        return json({'error': 'no images generated'})
    temp_png = BytesIO()
    img[0]._pil_image.save(temp_png, format='PNG')
    s3 = boto3.client(
        's3',
        aws_access_key_id=s3_access_key,
        aws_secret_access_key=s3_secret_key,
        endpoint_url=s3_endpoint,
        region_name='auto'
    )
    s3_file_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))+".png"
    s3.put_object(Body=temp_png.getvalue(), Bucket=s3_bucket_name, Key=s3_file_name, ContentType='image/png')
    url = f"{s3_image_storage_url}/{s3_file_name}"
    return json({'url': url})
