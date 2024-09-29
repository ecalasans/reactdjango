from rest_framework_nested import routers


from core.auth.viewsets import LoginViewSet, RefreshViewSet
from core.auth.viewsets.register import RegisterViewSet
from core.comment.viewsets import CommentViewSet
from core.post.viewsets import PostViewSet
from core.user.viewsets import UserViewSet

router = routers.SimpleRouter()

####  DRF ROUTER

router.register(r'user', UserViewSet, basename='user')
router.register(r'auth/register', RegisterViewSet, basename='auth_register')
router.register(r'auth/login', LoginViewSet, basename='auth_login')
router.register(r'auth/refresh', RefreshViewSet, basename='auth_refresh')
router.register(r'post', PostViewSet, basename='post')

#### NESTED ROUTERS
posts_router = routers.NestedSimpleRouter(
    parent_router=router,
    parent_prefix='post',
    lookup='post',
)

posts_router.register(r'comment', CommentViewSet, basename='post-comment')

urlpatterns = [
    *router.urls,
    *posts_router.urls,
]