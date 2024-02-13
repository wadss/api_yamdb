import re

from django.shortcuts import get_object_or_404
from django.core.validators import RegexValidator

from rest_framework import serializers

from users.models import User
from reviews.models import Category, Genre, Title, Review, Comment


class UserSerializer(serializers.ModelSerializer):
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


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=(
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Никнейм должен быть '
                'буквенно-цифровым'
            )
        )
    )

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


class ObtainJWTTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):

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

    genre = GenreSerializer(
        read_only=True,
        many=True,
    )
    category = CategorySerializer(read_only=True)


class TitleWriteSerializer(TitleSerializer):

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

    author = serializers.StringRelatedField(read_only=True)
    title = serializers.SlugRelatedField(
        slug_field='id',
        many=False,
        read_only=True,
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )