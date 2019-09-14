from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()

try:
    urlpatterns = [
        url(r'^admin/', include(admin.site.urls)),
    ]
except:
    urlpatterns = [
        url(r'^admin/', admin.site.urls),
    ]
