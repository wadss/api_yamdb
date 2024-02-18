from django.core.validators import RegexValidator

from rest_framework import serializers

from users.models import User
from reviews.models import Category, Genre, Title, Review, Comment


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для роута 'users'."""

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
    )

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
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Никнейм должен быть '
                'буквенно-цифровым'
            )
        ],
    )

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

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве '
                'никнейма запрещено'
            )
        return username

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
        max_length=150,
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


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер для роута 'reviews'."""

    author = serializers.StringRelatedField(
        read_only=True,
    )
    title = serializers.SlugRelatedField(
        slug_field='id',
        many=False,
        read_only=True,
    )

    def validate(self, data):
        if not self.context.get('request').method == 'POST':
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
            'title',
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
