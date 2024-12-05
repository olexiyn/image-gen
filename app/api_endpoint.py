from sanic import Blueprint, json
from sanic import SanicException

blueprint = Blueprint('apiroot', url_prefix='/api')

@blueprint.get('/')
async def main_root(request):
    return json({'testkey': 'testvalue'})
