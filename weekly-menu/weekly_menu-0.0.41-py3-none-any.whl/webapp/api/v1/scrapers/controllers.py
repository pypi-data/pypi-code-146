from uuid import uuid4
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask_jwt_extended.config import config
from marshmallow_mongoengine import schema

from . import scrape_recipe_from_url
from .. import BASE_PATH
from ... import QueryArgs, parse_query_args, validate_payload
from ...models import User, ShoppingList, UserPreferences
from ...exceptions import BadRequest, InvalidCredentials, NotFound

scraper_blueprint = Blueprint(
    'scrapers',
    __name__,
    url_prefix=BASE_PATH + '/scrapers'
)


@scraper_blueprint.route('/recipe')
@jwt_required
@parse_query_args
def scrape_recipe(query_args):
    if (QueryArgs.URL not in query_args or query_args[QueryArgs.URL] == None):
        raise BadRequest('url not provided')

    url = query_args[QueryArgs.URL]

    try:
        return jsonify(scrape_recipe_from_url(url)), 200
    except:
        raise NotFound('no recipe found on supplied URL')
