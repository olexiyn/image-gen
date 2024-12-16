from vertexai.preview.vision_models import ImageGenerationModel
from vertexai.preview.generative_models import GenerationConfig, GenerativeModel
import json
import httpx
from sanic import Sanic
from io import BytesIO
import aioboto3
import random
import string

imagen_fast_model = ImageGenerationModel.from_pretrained(
    'imagen-3.0-fast-generate-001')
imagen_quality_model = ImageGenerationModel.from_pretrained(
    'imagen-3.0-generate-001')
gemini_pro_model = GenerativeModel('gemini-1.5-pro-002')

myapp = Sanic.get_app()

s3_endpoint = myapp.config.get('S3_ENDPOINT')
s3_access_key = myapp.config.get('S3_ACCESS_KEY')
s3_secret_key = myapp.config.get('S3_SECRET_KEY')
s3_bucket_name = myapp.config.get('S3_BUCKET_NAME')
s3_image_storage_url = myapp.config.get('S3_IMAGE_STORAGE_URL')



async def content_gen(topic):
    prompt_text = f"Create 4 High-Quality Image Prompts to generate photos on given topic: {
        topic}"
    response_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                },
            },
            "required": ["prompt"],
        },
    }

    content = await gemini_pro_model.generate_content_async(prompt_text,
                                                            generation_config=GenerationConfig(
                                                                response_mime_type="application/json",
                                                                response_schema=response_schema
                                                            ),
                                                            stream=False
                                                            )
    return json.loads(content.text)


async def image_gen(prompt, aspect_ratio='16:9', model='fast'):
    if model == 'quality':
        imagen_model = imagen_quality_model
    else:
        imagen_model = imagen_fast_model
    response = imagen_model.generate_images(
        prompt=prompt,
        language='en',
        guidance_scale=98.5,
        add_watermark=False,
        number_of_images=1,
        aspect_ratio=aspect_ratio
    )

    return response.images


async def upscale(image_url, scale):
    url = myapp.config.get('UPSCALE_URL')
    api_key = myapp.config.get('UPSCALE_API_KEY')
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-API-KEY': api_key,
               }
    data = {'image_url': image_url, 'scale': scale}
    async with httpx.AsyncClient() as client:
        result = await client.post(url, headers=headers, json=data, timeout=90.0)
    return result.json()


async def save_in_cloud(upload_data, image_type):
    if image_type == 'jpeg':
        content_type = 'image/jpeg'
    else:
        content_type = 'image/png'
    session = aioboto3.Session()
    async with session.client('s3',
                              aws_access_key_id=s3_access_key,
                              aws_secret_access_key=s3_secret_key,
                              endpoint_url=s3_endpoint,
                              region_name='auto') as s3:
        try:
            s3_file_name = ''.join(random.choices(
                string.ascii_lowercase + string.digits, k=8))+f".{image_type}"
            await s3.put_object(Body=upload_data, Bucket=s3_bucket_name,
                                    Key=s3_file_name, ContentType=content_type)
        except Exception as e:
            print(f"error: {e} ({type(e)})")
            return ''
    url = f"{s3_image_storage_url}/{s3_file_name}"
    return url


async def get_image_from_url(url):
    async with httpx.AsyncClient() as client:
        result = await client.get(url, timeout=90.0)
    return result.content