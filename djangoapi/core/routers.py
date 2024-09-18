from rest_framework import routers

from core.auth.viewsets import LoginViewSet, RefreshViewSet
from core.auth.viewsets.register import RegisterViewSet
from core.post.viewsets import PostViewSet
from core.user.viewsets import UserViewSet

router = routers.SimpleRouter()

router.register(r'user', UserViewSet, basename='user')
router.register(r'auth/register', RegisterViewSet, basename='auth_register')
router.register(r'auth/login', LoginViewSet, basename='auth_login')
router.register(r'auth/refresh', RefreshViewSet, basename='auth_refresh')
router.register(r'post', PostViewSet, basename='post')

urlpatterns = [
    *router.urls,
]