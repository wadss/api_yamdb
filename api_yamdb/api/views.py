from django.db.models import Avg
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .filters import TitleFilter
from .permissions import (
    IsAdminUser,
    IsAdminOrReadOnly,
    IsAuthorModeratorOrAdmin,
)
from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    Comment,
)
from .serializers import (
    UserSerializer,
    UserMeSerializer,
    SignUpSerializer,
    ObtainJWTTokenSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    ReviewSerializer,
    CommentSerializer
)
from .mixins import CreateListDestroyMixin
from users.models import User


class UserViewSet(ModelViewSet):
    """Viewset для роута 'users'."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdminUser,
    )
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    ordering = ('username',)

    @action(
            url_path='me',
            url_name='me',
            methods=['get', 'patch'],
            detail=False,
            permission_classes=(IsAuthenticated,)
    )
    def user_me_route(self, request):
        if request.method == 'GET':
            serializer = UserMeSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = UserMeSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class ObtainJWTTokenViewSet(APIView):
    """View-класс для роута 'auth/token/'."""

    serializer_class = ObtainJWTTokenSerializer

    def get_queryset(self):
        return get_object_or_404(
            User,
            username=self.kwargs.get('username')
        )

    def post(self, request, *args, **kwargs):
        serializer = ObtainJWTTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data.get('username')
        )
        token = serializer.validated_data.get('confirmation_code')
        if not default_token_generator.check_token(user, token):
            return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
        token = AccessToken.for_user(user)
        return Response(
            {'token': f'{token}'},
            status=status.HTTP_200_OK,
        )


class SignUpView(APIView):
    """View-класс для роута 'auth/signup/'."""

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(CreateListDestroyMixin):
    """Viewset для роута 'categories'."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyMixin):
    """Viewset для роута 'genres'."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Viewset для роута 'titles'."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score'),
    ).order_by('name')
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = (
        'get',
        'post',
        'delete',
        'patch',
    )

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Viewset для роута 'reviews'."""

    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorModeratorOrAdmin,
    )
    http_method_names = (
        'get',
        'post',
        'delete',
        'patch',
    )

    def _get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(
            Title,
            id=title_id
        )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self._get_title(),
        )

    def get_queryset(self):
        return self._get_title().reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    """Viewset для роута 'comments'."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorModeratorOrAdmin,
    )
    http_method_names = (
        'get',
        'post',
        'delete',
        'patch',
    )

    def _get_review(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(
            Review,
            id=review_id,
            title=title_id,
        )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self._get_review()
        )

    def get_queryset(self):
        return self._get_review().comments.all()
