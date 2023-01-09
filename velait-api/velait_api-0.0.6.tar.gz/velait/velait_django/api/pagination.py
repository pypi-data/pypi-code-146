from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param


class CustomPagination(PageNumberPagination):
    def get_last_page(self):
        return replace_query_param(
            url=self.request.build_absolute_uri(),
            key=self.page_query_param,
            val=self.page.paginator.num_pages,
        )

    def get_paginated_response(self, data):
        return Response({
            "Pagination": {
                'totalRecords': self.page.paginator.count,
                'totalPages': self.page.paginator.num_pages,
                'first': self.request.build_absolute_uri(),
                'last': self.get_last_page(),
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            "Results": data,
        })
