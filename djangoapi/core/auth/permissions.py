from rest_framework.permissions import BasePermission, SAFE_METHODS

class UserPermission(BasePermission):
    # NÍVEL GERAL
    def has_permission(self, request, view):
        # Se tentar fazer um post só será permitido se ele for authenticado
        if view.basename in ["post", "post-comment"]:
        # Se o usuário for anônimo só terá permissão para métodos seguros - GET, HEAD, OPTIONS
            if request.user.is_anonymous:
                return request.method in SAFE_METHODS

            return bool(request.user and request.user.is_authenticated)

        #  Permissão negada por padrão
        return False

    # NÍVEL DE OBJETO
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS

        if view.basename in ["post"]:
            return bool(request.user and request.user.is_authenticated)

        if view.basename in ["post-comment"]:
            if request.method in ["DELETE"]:
                return bool(request.user.is_superuser or request.user in [obj.author, obj.post.author])

            return bool(request.user and request.user.is_authenticated)

        #  Permissão negada por padrão
        return False