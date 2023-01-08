from flask_restful import Resource, abort, request, reqparse
from mongoengine.queryset.visitor import Q

from ...models import Config

class ConfigInstance(Resource):
  def get(self, version_code):
    return Config.objects(Q(min_version_code__lte=version_code)).order_by('-min_version_code').first_or_404()
