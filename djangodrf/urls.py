from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("polls/", include("polls.web_urls")),
    path("api/v1/users/", include("users.api_urls")),
    path("admin/", admin.site.urls),
] + debug_toolbar_urls()
