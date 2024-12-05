from sanic import Blueprint, json
from sanic import SanicException
from app.utils import content_gen

blueprint = Blueprint('apiroot', url_prefix='/api')

@blueprint.get('/')
async def main_root(request):
    if request.args.get('topic'):
        topic = request.args.get('topic')
    else:
        topic = 'Dogs'
    return json(content_gen(topic))
