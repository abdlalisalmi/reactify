from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url="/static/favicon.ico", permanent=True)

urlpatterns = [
    path("favicon.ico", favicon_view),
    path("admin/", admin.site.urls),
    path("", include("reactify.urls")),
]
