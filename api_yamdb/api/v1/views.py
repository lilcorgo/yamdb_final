from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.db.models import Avg
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import viewsets, mixins, filters, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .serializers import (
    CreateUpdateTitleSerializer, GenreSerializer, CategorySerializer,
    TitleSerializer, ReviewSerializer, CommentSerializer,
    UserSerializer, SignUpSerializer, TokenSerializer
)
from .permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsAdminOrAuthorOrModeratorOrReadOnly
)
from users.models import User
from reviews.models import Title, Genre, Category, Review


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class UsersViewSet(viewsets.ModelViewSet):
    """Получение информации о пользователе и редактирование ее."""
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me'
    )
    def me(self, request):
        """Информация о себе."""
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def SignupView(request):
    """Регистрация пользователя."""
    serializer = SignUpSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
    username = serializer.data['username']
    email = serializer.data['email']

    try:
        user, _ = User.objects.get_or_create(
            username=username,
            email=email,
        )
    except IntegrityError:
        return Response(
            'Логин и/или email уже зарегистрированы в системе.',
            status=status.HTTP_400_BAD_REQUEST,
        )
    confirmation_code = default_token_generator.make_token(user)
    message = f'Ваш код: {confirmation_code}'
    from_email = settings.EMAIL_FROM
    send_mail(
        settings.EMAIL_HEADER,
        message,
        from_email,
        [email],
        fail_silently=False
    )
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def TokenView(request):
    """Получение токена."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.data['username']
    confirmation_code = serializer.data['confirmation_code']
    user = get_object_or_404(User, username=username)

    if not default_token_generator.check_token(user, confirmation_code):
        return Response(
            'Код подтверждения неверен',
            status=status.HTTP_400_BAD_REQUEST
        )
    refresh = RefreshToken.for_user(user)
    return Response(
        {'token': str(refresh.access_token)},
        status=status.HTTP_200_OK
    )


class GenreViewSet(ListCreateDestroyViewSet):
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)


class CategoryViewSet(ListCreateDestroyViewSet):
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly, )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    filterset_class = TitleFilter
    filterset_fields = ('year', 'name', 'genre', 'category')
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return CreateUpdateTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для обработки запросов с отзывами."""
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrAuthorOrModeratorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для обработки запросов с комментариями к отзывам."""
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrAuthorOrModeratorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
            title=self.kwargs['title_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
            title=self.kwargs['title_id'])
        serializer.save(author=self.request.user,
                        review=review)
