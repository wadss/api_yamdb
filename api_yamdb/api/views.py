from django.db.models import Avg
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import mixins, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (
    SAFE_METHODS,
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
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
from users.models import User


class UserMeView(APIView):

    permission_classes = (
        IsAuthenticated,
    )
    
    def get(self, request):
        user = get_object_or_404(
            User,
            username=request.user.username
        )
        serializer = UserSerializer(user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    
    def patch(self, request):
        user = get_object_or_404(
            User,
            username=request.user.username
        )
        serializer = UserMeSerializer(
            user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class UserViewSet(ModelViewSet):

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


class ObtainJWTTokenViewSet(CreateAPIView):

    serializer_class = ObtainJWTTokenSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return get_object_or_404(
            User,
            username=self.kwargs.get('username')
        )
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data.get('username')
        )
        token = serializer.validated_data.get('confirmation_code')
        if default_token_generator.check_token(user, token):
            token = AccessToken.for_user(user)
            return Response(
                {'token':f'{token}'},
                status=status.HTTP_200_OK,
            )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST,
        )


class SignUpView(APIView):

    permission_classes = (AllowAny,)
    
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        username = request.data.get('username')
        email = request.data.get('email')
        user = User.objects.filter(
            username=username,
            email=email,
        ).first()
        
        if user:
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                subject='Регистрация на YaMDb',
                message=(
                    f'Здравствуйте, {user.username}.'
                    f'Ваш код потверждения: {confirmation_code}'
                ),
                from_email=None,
                recipient_list=[user.email],
            )
            message = (
                'Пользователь с такими данными уже зарегистрирован.'
                'Код подтверждения отправлен на почту.'
            )
            return Response(
                message, 
                status=status.HTTP_200_OK
            )
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            user = get_object_or_404(User, username=username)
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                subject='Регистрация на YaMDb',
                message=(
                    f'Здравствуйте, {user.username}.'
                    f'Ваш код потверждения: {confirmation_code}'
                ),
                from_email=None,
                recipient_list=[user.email],
            )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateListDestroyMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    )
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(CreateListDestroyMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):

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
        'patch'
    )

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthorModeratorOrAdmin,
    )
    http_method_names = (
        'get',
        'post',
        'delete',
        'patch'
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
            title = self._get_title(),
        )
    
    def get_queryset(self):
        return self._get_title().reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    
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
        'patch'
    )

    def _get_review(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(
            Title,
            id = title_id
        )
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(
            Review,
            id=review_id,
            title=title,
        )
    
    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self._get_review()
        )
    
    def get_queryset(self):
        return Comment.objects.filter(
            review=self._get_review(),
        )
