from django.conf import settings
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from enough.api.permissions import IsEnoughGroupMember
from enough.common import bind


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated, IsEnoughGroupMember))
def delegate_test_dns(request):
    return JsonResponse(bind.delegate_dns(
        f'test.{settings.ENOUGH_DOMAIN}',
        request.data['name'],
        request.data['ip'],
    ), safe=False, status=201)


@api_view(['POST'])
def delegate_dns(request):
    return JsonResponse(bind.delegate_dns(
        f'd.{settings.ENOUGH_DOMAIN}',
        request.data['name'],
        request.data['ip'],
    ), safe=False, status=201)


@api_view(['GET'])
def ping(request):
    return HttpResponse('pong')
