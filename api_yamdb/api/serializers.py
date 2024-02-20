from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db.models import Avg
from django.contrib.auth.tokens import default_token_generator

from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comment
from api_yamdb.settings import (
    MAX_LENGTH_OF_USERNAME,
    MAX_LENGTH_OF_EMAIL,
)
from users.models import User
from .validators import validate_username


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

        user, created = User.objects.get_or_create(
            email=email,
            defaults={'username': username},
        )

        if created:
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
        if User.objects.filter(
            username=data.get('username'),
            email=data.get('email'),
        ):
            return data
        elif User.objects.filter(
            username=data.get('username')
        ):
            raise serializers.ValidationError(
                'Никнейм уже занят'
            )
        elif User.objects.filter(
            email=data.get('email')
        ):
            raise serializers.ValidationError(
                'Эл. почта уже занята'
            )
        return data

    class Meta:
        model = User
        fields = (
            'email',
            'username',
        )


class ObtainJWTTokenSerializer(serializers.Serializer):
    """Сериалайзер для роута 'auth/token/'."""

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
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

    rating = serializers.IntegerField(read_only=True)

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
        reviews = instance.reviews.all()
        if reviews.exists():
            return reviews.aggregate(Avg('score'))['score__avg']
        return None

    def to_representation(self, instance):
        representation = {
            'id': instance.id,
            'name': instance.name,
            'year': instance.year,
            'rating': self.get_rating(instance),
            'description': instance.description,
            'genre': [],
            'category': None,
        }

        for genre in instance.genre.all():
            representation['genre'].append({
                'name': genre.name,
                'slug': genre.slug,
            })

        if instance.category:
            representation['category'] = {
                'name': instance.category.name,
                'slug': instance.category.slug,
            }

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
