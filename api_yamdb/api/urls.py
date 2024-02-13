from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
)

app_name = 'api'

v1_router = DefaultRouter()

v1_router.register('titles', TitleViewSet, basename='title')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
