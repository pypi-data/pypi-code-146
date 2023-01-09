import json
from typing import Type

from rest_framework.views import APIView
from rest_framework.serializers import ModelSerializer

from velait.velait_django.models import BaseModel
from velait.velait_django.api.responses import APIResponse
from velait.velait_django.search import search_objects, SearchError


class SearchView(APIView):
    model: Type[BaseModel] = None
    serializer_class: Type[ModelSerializer] = None

    def __init__(self, *args, **kwargs):
        super(SearchView, self).__init__(*args, **kwargs)

        if self.model is None or self.serializer_class is None:
            raise NotImplementedError("Model or Serializer were not supplied to the SearchView")

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query')
        ordering = request.GET.get('ordering')
        page = request.GET.get('page')

        try:
            data = search_objects(model=self.model, ordering=ordering, search_data=json.loads(query))
        except SearchError as exc:
            return APIResponse(data=exc.message, status=400)
        except json.JSONDecodeError as exc:
            return APIResponse(data=str(exc), status=400)

        return APIResponse(data=self.serializer_class(instance=data, many=True).data, status=200)
