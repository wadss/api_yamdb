from django.urls import include, path
from rest_framework import routers

from api.views import (
    UserViewSet,
    ObtainJWTTokenViewSet,
    SignUpView,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
)


router_v1 = routers.DefaultRouter()

router_v1.register(
    'users',
    UserViewSet,
    basename='user,'
)
router_v1.register(
    'categories',
    CategoryViewSet,
    basename='category',
)
router_v1.register(
    'genres',
    GenreViewSet,
    basename='genre',
)
router_v1.register(
    'titles',
    TitleViewSet,
    basename='title'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review',
)
router_v1.register(
    r'titles/(?P<title_id>\d+)'
    r'/reviews/(?P<review_id>\d+)'
    r'/comments',
    CommentViewSet,
    basename='comment',
)

auth_urls = [
    path(
        'token/',
        ObtainJWTTokenViewSet.as_view(),
        name='obtain_token'
    ),
    path(
        'signup/',
        SignUpView.as_view(),
        name='sign_up'
    ),
]

urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path('v1/', include(router_v1.urls)),
]
