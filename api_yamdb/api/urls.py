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


router = routers.DefaultRouter()

router.register(
    r'users',
    UserViewSet,
    basename='user,'
)
router.register(
    r'categories',
    CategoryViewSet,
    basename='category',
)
router.register(
    r'genres',
    GenreViewSet,
    basename='genre',
)
router.register(
    r'titles',
    TitleViewSet,
    basename='title'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review',
)
router.register(
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
    path('', include(router.urls)),
]