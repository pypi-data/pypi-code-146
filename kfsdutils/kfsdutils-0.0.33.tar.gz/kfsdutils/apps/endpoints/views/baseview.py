from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, filters
from rest_framework.renderers import JSONRenderer
from rest_framework import generics, status
from rest_framework.views import Response

class ModelPagination(PageNumberPagination):
    page_size = 20

class BaseModelViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    renderer_classes = [JSONRenderer]
    pagination_class = ModelPagination
    filter_backends = [filters.OrderingFilter]
    ordering = ['created']

class CustomModelViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    renderer_classes = [JSONRenderer]
    pagination_class = ModelPagination
    filter_backends = [filters.OrderingFilter]
    ordering = ['created']
    lookup_field = "identifier"
    lookup_value_regex = '[^/]+'


class CustomGetView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class CustomListView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class CustomViewSet(generics.GenericAPIView):
    renderer_classes = [JSONRenderer]
    pagination_class = ModelPagination

    def processRequest(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return serializer.eval(serializer.validated_data)
        else:
           return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        return self.processRequest(request)