from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comment
from api_yamdb.settings import (
    MAX_LENGTH_OF_USERNAME,
    MAX_LENGTH_OF_EMAIL,
)
from users.models import User
from users.validators import validate_username


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для роута 'users'."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UserMeSerializer(UserSerializer):
    """Сериалайзер для роута 'users/me'."""

    role = serializers.CharField(read_only=True)


class SignUpSerializer(serializers.ModelSerializer):
    """Сериалайзер для роута 'auth/signup/'."""

    username = serializers.CharField(
        required=True,
        max_length=MAX_LENGTH_OF_USERNAME,
        validators=[
            UnicodeUsernameValidator(
                message='Никнейм должен быть '
                'буквенно-цифровым'
            ),
            validate_username,
        ],
    )
    email = serializers.EmailField(
        required=True,
        max_length=MAX_LENGTH_OF_EMAIL,
    )

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']

        user, _ = User.objects.get_or_create(
            email=email,
            defaults={'username': username}
        )

        if user:
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                subject='Регистрация на YaMDb',
                message=(
                    f'Здравствуйте, {user.username}. '
                    f'Ваш код подтверждения: {confirmation_code}'
                ),
                from_email=None,
                recipient_list=[user.email],
            )

        return user

    def validate(self, data):
        existing_user_with_email = User.objects.filter(
            email=data.get('email'),
        ).first()
        existing_user_with_username = User.objects.filter(
            username=data.get('username'),
        ).first()
        error_msg = {}

        if existing_user_with_email != existing_user_with_username:

            if existing_user_with_email:
                error_msg['email'] = ['Эл. почта уже занята']

            if existing_user_with_username:
                error_msg['username'] = ['Никнейм уже занят']

            raise serializers.ValidationError(error_msg)
        return data

    class Meta:
        model = User
        fields = (
            'email',
            'username',
        )


class ObtainJWTTokenSerializer(serializers.Serializer):
    """Сериалайзер для роута 'auth/token/'."""

    username = serializers.CharField(
        max_length=MAX_LENGTH_OF_USERNAME,
        validators=[
            UnicodeUsernameValidator(
                message='Никнейм должен быть '
                'буквенно-цифровым'
            ),
            validate_username,
        ],
    )
    confirmation_code = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для роута 'categories'."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер для роута 'genres'."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Миксин-сериалайзер для роута 'titles'."""

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )


class TitleReadSerializer(TitleSerializer):
    """Сериалайзер для роута 'titles' на чтение."""

    rating = serializers.IntegerField(read_only=True, default=None)

    genre = GenreSerializer(
        read_only=True,
        many=True,
    )
    category = CategorySerializer(read_only=True)


class TitleWriteSerializer(TitleSerializer):
    """Сериалайзер для роута 'titles' на запись."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False,
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )

    rating = serializers.SerializerMethodField()

    def get_rating(self, instance):
        return getattr(instance, 'rating', None)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['rating'] = self.get_rating(instance)
        return representation


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер для роута 'reviews'."""

    author = serializers.StringRelatedField(
        read_only=True,
    )

    def validate(self, data):
        if self.context.get('request').method != 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(
            author=author,
            title=title_id,
        ).exists():
            raise serializers.ValidationError(
                'Отзыв на это произведение уже оставлен'
            )
        return data

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для роута 'comments'."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
