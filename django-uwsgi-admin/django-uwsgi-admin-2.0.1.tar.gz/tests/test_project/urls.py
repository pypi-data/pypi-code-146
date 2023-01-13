import debug_toolbar
from django.contrib import admin
from django.urls import include
from django.urls import path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('wag/docs/', include(wagtaildocs_urls)),
    path('wag/', include(wagtailadmin_urls)),
    path('', include(wagtail_urls)),
]

# admin.site.
