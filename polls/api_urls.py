from django.urls import include, path
from rest_framework import routers

from polls import views

router = routers.DefaultRouter()
router.register(r"questions", views.QuestionViewSet)
router.register(r"choices", views.ChoiceViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
