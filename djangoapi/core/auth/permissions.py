from rest_framework.permissions import BasePermission, SAFE_METHODS

class UserPermission(BasePermission):
    # NÍVEL GERAL
    def has_permission(self, request, view, obj):
        # Se o usuário for anônimo só terá permissão para métodos seguros - GET, HEAD, OPTIONS
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS

        # Se tentar fazer um post só será permitido se ele for authenticado
        if view.basename in ["post"]:
            return bool(request.user and request.user.is_authenticated)

        #  Permissão negada por padrão
        return False

    # NÍVEL DE OBJETO
    def has_object_permission(self, request, view, obj):
        # Se tentar fazer um post
        if view.basename in ["post"]:
            # Verifica se é anônimo;  se for só será permitido GET, HEAD e OPTIONS
            if request.user.is_anonymous:
                return request.method in SAFE_METHODS

            # Libera POST se o usuário for autenticado
            return bool(request.user and request.user.is_authenticated)

        #  Permissão negada por padrão
        return False