from rest_framework import routers

from core.auth.viewsets.register import RegisterViewSet
from core.user.viewsets import UserViewSet

router = routers.SimpleRouter()

router.register(r'user', UserViewSet, basename='user')
router.register('auth/register', RegisterViewSet, basename='auth_register')

urlpatterns = [
    *router.urls,
]