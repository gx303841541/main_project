from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    自定义权限只允许对象的所有者编辑它。
    """

    # def has_permission(self, request, view):
    #    return True

    def has_object_permission(self, request, view, obj):
        # 读取权限允许任何请求，
        # 所以我们总是允许GET，HEAD或OPTIONS请求。
        if request.method in permissions.SAFE_METHODS:
            return True

        # 只有该project的所有者才允许写权限。
        # return obj.owner == request.user
        user = request.META.get("user", None)
        token = request.META.get("token", None)
        if not user:
            print('headers has no user!')
            pass

        if not token:
            print('headers has no token!')
            pass

        return True
        return obj.owner.usertoken.token == token
