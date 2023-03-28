from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.validators import username_validation
from reviews.models import Title, Category, Genre, Review, Comment


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'bio',
            'role',
        )
        model = User

    def validate_username(self, value):
        return username_validation(value)


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        validators=[username_validation]
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
    )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
    )
    confirmation_code = serializers.CharField(
        required=True,
        max_length=10,
    )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CreateUpdateTitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field='slug', many=True,
                                         queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    title = serializers.SlugRelatedField(slug_field='name',
                                         read_only=True)

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        current_user = self.context.get('request').user
        request_method = self.context.get('request').method
        if request_method == 'POST':
            if Review.objects.filter(author=current_user,
                                     title=title).exists():
                raise serializers.ValidationError('Пользователь не может'
                                                  'оставить более одного'
                                                  'отзыва на произведение')
        return data

    class Meta:
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('id', 'review', 'text', 'author', 'pub_date')
        read_only_fields = ('review', )
        model = Comment
