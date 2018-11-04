import hashlib
import time

from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import (filters, generics, mixins, permissions, status,
                            viewsets)
from rest_framework.decorators import action, api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from usermanager import models, serializers


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'register': reverse('register', request=request, format=format),
        'login': reverse('login', request=request, format=format),
        'users': reverse('userinfo-list', request=request, format=format),
    })


KEY_MISS = {
    "code": "0100",
    "success": False,
    "msg": "请求数据非法"
}

REGISTER_USERNAME_EXIST = {
    "code": "0101",
    "success": False,
    "msg": "用户名已被注册"
}

REGISTER_EMAIL_EXIST = {
    "code": "0101",
    "success": False,
    "msg": "邮箱已被注册"
}

SYSTEM_ERROR = {
    "code": "9999",
    "success": False,
    "msg": "System Error"
}

REGISTER_SUCCESS = {
    "code": "0001",
    "success": True,
    "msg": "register success"
}

LOGIN_FAILED = {
    "code": "0103",
    "success": False,
    "msg": "用户名或密码错误"
}

USER_NOT_EXISTS = {
    "code": "0104",
    "success": False,
    "msg": "该用户未注册"
}

LOGIN_SUCCESS = {
    "code": "0001",
    "success": True,
    "msg": "login success"
}


class RegisterView(APIView):

    authentication_classes = ()
    permission_classes = ()

    """
    注册:{
        "user": "demo"
        "password": "1321"
        "email": "1@1.com"
    }
    """

    def post(self, request):

        try:
            username = request.data["username"]
            password = request.data["password"]
            email = request.data["email"]
        except KeyError:
            return Response(KEY_MISS)

        if models.UserInfo.objects.filter(username=username).first():
            return Response(REGISTER_USERNAME_EXIST)

        if models.UserInfo.objects.filter(email=email).first():
            return Response(REGISTER_EMAIL_EXIST)

        request.data["password"] = make_password(password)

        serializer = serializers.UserInfoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(REGISTER_SUCCESS)
        else:
            return Response(SYSTEM_ERROR)


class LoginView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        try:
            username = request.data["username"]
            password = request.data["password"]
        except KeyError:
            return Response(KEY_MISS)

        user = models.UserInfo.objects.filter(username=username).first()

        if not user:
            return Response(USER_NOT_EXISTS)

        if not check_password(password, user.password):
            return Response(LOGIN_FAILED)

        token = generate_token(username)

        try:
            models.UserToken.objects.update_or_create(user=user, defaults={"token": token})
        except ObjectDoesNotExist:
            return Response(SYSTEM_ERROR)
        else:
            LOGIN_SUCCESS["token"] = token
            LOGIN_SUCCESS["user"] = username
            LOGIN_SUCCESS["url"] = reverse('userinfo-detail', args=[user.pk], request=request)
            return Response(LOGIN_SUCCESS)


def generate_token(username):
    timestamp = str(time.time())

    token = hashlib.md5(bytes(username, encoding='utf-8'))
    token.update(bytes(timestamp, encoding='utf-8'))

    return token.hexdigest()


class UserList(generics.ListAPIView):
    queryset = models.UserInfo.objects.all()
    serializer_class = serializers.UserInfoSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = models.UserInfo.objects.all()
    serializer_class = serializers.UserInfoSerializer
