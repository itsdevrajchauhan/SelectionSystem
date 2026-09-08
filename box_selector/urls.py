from django.urls import path

from .views import BoxRecommendationView


urlpatterns = [
    path("recommend-box/", BoxRecommendationView.as_view(), name="recommend-box"),
]