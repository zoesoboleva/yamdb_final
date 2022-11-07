from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True)

    def validate(self, data):
        username = data['username'].casefold()
        email = data['email']
        if username == 'me':
            raise serializers.ValidationError(
                {"username": "Нельзя использовать me как логин"})
        user_exist = User.objects.filter(username=username).exists()
        email_used = User.objects.filter(email=email).exists()
        dict_containing_errors: 'dict' = {}
        if user_exist:
            dict_containing_errors.update(
                {"username": "Имя пользователя уже занято"})
        if email_used:
            dict_containing_errors.update(
                {"email": "Почтовый адрес уже используется"})
        if dict_containing_errors:
            raise serializers.ValidationError(dict_containing_errors)
        return data

    class Meta:
        fields = ('username', 'email')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'confirmation_code')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        model = Review

    def validate(self, data):
        title_id = self.context['request'].parser_context['kwargs']['title_id']
        if self.context['request'].method == 'POST':
            if Review.objects.filter(
                    author=self.context['request'].user,
                    title__id=title_id).exists():
                raise (
                    serializers.ValidationError(
                        'Нелья написать обзор дважды.'))
            return data
        return data


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField()

    class Meta:
        fields = ('id', 'category', 'genre', 'name',
                  'rating', 'year', 'description')
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'bio',
            'role',
        )
