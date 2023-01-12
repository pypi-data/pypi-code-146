from django.http import HttpResponse
from django.urls import path


def index(request):
    return HttpResponse("""
<div align="center">
  <h1>light-django</h1>
  <p>✨ A lighter and easier <a href="https://www.djangoproject.com/">django</a> frame. ✨</p>
  <p>
    <a href="https://www.wtfpl.net/"><img src="https://img.shields.io/github/license/montmorillonite-CN/light-django" alt="license"></a>
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="Python"></a>
    <a href="https://www.djangoproject.com/"><img src="https://img.shields.io/badge/django-4.1.5-red.svg" alt="django"></a>
    <a href="https://pypi.org/project/light-django"><img src="https://badgen.net/pypi/v/light-django" alt="pypi"></a>
  </p>
</div>
""")


urlpatterns = [
    path("", index, name="index")
]
