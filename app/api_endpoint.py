from sanic import Blueprint, json
from sanic import SanicException
#from vertexai.preview.vision_models import ImageGenerationModel
from vertexai.preview.generative_models import GenerationConfig, GenerativeModel

blueprint = Blueprint('apiroot', url_prefix='/api')

@blueprint.get('/')
async def main_root(request):
    return json({'testkey': 'testvalue'})
