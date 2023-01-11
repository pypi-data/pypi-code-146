from typing import Type

from rest_framework.views import APIView
from rest_framework.serializers import ModelSerializer

from velait.velait_django.main.models import BaseModel
from velait.velait_django.main.api.responses import APIResponse
from velait.velait_django.main.services.search import search, SearchError


class SearchView(APIView):
    model: Type[BaseModel] = None
    serializer_class: Type[ModelSerializer] = None

    def __init__(self, *args, **kwargs):
        super(SearchView, self).__init__(*args, **kwargs)

        if self.model is None or self.serializer_class is None:
            raise NotImplementedError("Model or Serializer were not supplied to the SearchView")

    def get(self, request, *args, **kwargs):
        try:
            data = search(
                search_=request.GET.get('search'),
                query=request.GET.get('query'),
                ordering=request.GET.get('ordering'),
                page=request.GET.get('page'),
                model=self.model,
            )
        except SearchError as exc:
            return APIResponse(errors=[exc], status=400)

        return APIResponse(data=self.serializer_class(instance=data, many=True).data, status=200)
