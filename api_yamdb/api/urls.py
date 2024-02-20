from django.urls import include, path
from rest_framework import routers

from api.views import (
    UserMeView,
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

urlpatterns = [
    path(
        'auth/token/',
        ObtainJWTTokenViewSet.as_view(),
        name='obtain_token'
    ),
    path(
        'auth/signup/',
        SignUpView.as_view(),
        name='sign_up'
    ),
    path(
        'users/me/',
        UserMeView.as_view(),
        name='me'
    ),
    path('', include(router_v1.urls)),
]
