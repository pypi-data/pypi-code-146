from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required

from rest_framework.authtoken.models import Token


@login_required
def member_index(request):
    t = loader.get_template('member/member-index.html')
    token = Token.objects.get_or_create(user=request.user)
    c = {'token': token[0]}
    return HttpResponse(t.render(c, request), content_type='text/html')
