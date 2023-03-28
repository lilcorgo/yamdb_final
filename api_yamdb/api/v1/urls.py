from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import (
    CategoryViewSet, GenreViewSet, TitleViewSet, ReviewViewSet, CommentViewSet,
    TokenView, SignupView, UsersViewSet
)

router_v1 = DefaultRouter()

router_v1.register('users', UsersViewSet, basename='users')
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

auth_patterns = [
    path('signup/', SignupView, name='signup'),
    path('token/', TokenView, name='token'),
]

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include(auth_patterns))
]
