from django.core.exceptions import ObjectDoesNotExist
from djangoldp.views import LDPViewSet, JSONLDParser, NoCSRFAuthentication
from rest_framework import status
import requests as requestsLib

from ..models import AnnotationTarget, NeedleActivity
from ..models.needle_activity import ACTIVITY_TYPE_FIRST_ANNOTATION_WITHOUT_CONNECTIONS
from rest_framework.views import APIView, Response

from ..request_parser import RequestParser


class AnnotationTargetViewset(LDPViewSet):
    def create(self, request, *args, **kwargs):
        self.check_model_permissions(request)
        target = request.data['target']
        try:
            targets_in_db = AnnotationTarget.objects.get(target=target)
        except ObjectDoesNotExist:
            try:
                new_annotation = self.parse_target(target)
                return self.save_annotation_target(request, new_annotation)

            except Exception as e:
                return self.generate_invalide_response()

        return self.generate_success_response(status.HTTP_200_OK, targets_in_db)

    def parse_target(self, target):
        targetRequestResponse = requestsLib.get(target)

        if targetRequestResponse.status_code != 200:
            raise Exception

        parser = RequestParser()
        (result, annotation_target) = parser.parse(target, targetRequestResponse.content)
        if not result:
            raise Exception

        return annotation_target

    def generate_success_response(self, status, target):
        response_serializer = self.get_serializer()
        data = response_serializer.to_representation(target)
        headers = self.get_success_headers(data)
        return Response(data, status=status, headers=headers)

    def generate_invalide_response(self):
        return Response({'URL': ['Le lien est invalide']}, status=status.HTTP_400_BAD_REQUEST)

    def save_annotation_target(self, request, annotation_target):
        annotation_target.save()
        response_serializer = self.get_serializer()
        data = response_serializer.to_representation(annotation_target)
        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


