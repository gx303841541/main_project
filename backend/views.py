import os
import sys

import backend.task as task
import django_filters.rest_framework
from backend.httprunner.logger import logger
from backend.models import *
from backend.permissions import IsOwnerOrReadOnly
from backend.serializers import *
from backend.utils import formater, pagination, rsp_msg
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import (filters, generics, mixins, permissions, status,
                            viewsets)
from rest_framework.decorators import action, api_view, detail_route
from rest_framework.pagination import (CursorPagination, LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('users-list', request=request, format=format),
        'projects': reverse('projects-list', request=request, format=format),
        'apis': reverse('apis-list', request=request, format=format),
        'suites': reverse('suites-list', request=request, format=format),
        'cases': reverse('cases-list', request=request, format=format),
        'steps': reverse('steps-list', request=request, format=format),
        'caseresults': reverse('caseresults-list', request=request, format=format),
        'stepresults': reverse('stepresults-list', request=request, format=format),
        'suiteresults': reverse('suiteresults-list', request=request, format=format),
        'configs': reverse('configs-list', request=request, format=format),
    })


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


'''
@api_view(['GET', 'POST'])
def projects_list(request, format=None):
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProjectSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''

'''
class ProjectList(APIView):
    """
    列出所有的projects或者创建一个新的project。
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # if self.request.user:
        #    request.data['owner'] = User.objects.filter(username=self.request.user)[0]
        print(request.data)
        print(self.request.user)
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
'''

'''
@api_view(['GET', 'PUT', 'DELETE'])
def project_detail(request, pk, format=None):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''

'''
class ProjectDetail(APIView):
    """
    检索，更新或删除一个project示例。
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''


class ProjectViewSet(viewsets.ModelViewSet):
    """
    此视图自动提供`list`，`create`，`retrieve`，`update`和`destroy`操作。
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = pagination.MyPageNumberPagination
    authentication_classes = ()
    permission_classes = (IsOwnerOrReadOnly, )
    #filter_backends = (filters.OrderingFilter,)
    #search_fields = ('name',)
    #ordering_fields = ('create_time', 'name')

    # def perform_create(self, serializer):
    #    serializer.save(owner=self.request.user)

    def create(self, request, format=None):
        # print(self.request.query_params)
        return super().create(request, format)


class ApiViewSet(viewsets.ModelViewSet):
    """
    此视图自动提供`list`，`create`，`retrieve`，`update`和`destroy`操作。
    """
    queryset = Api.objects.all()
    serializer_class = ApiSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request, format=None):
        # print(dir(request.META))
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # now do not know frontend format, so just store it
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

            # format request.data(from frontend) to backend format
            data = formater.get_backend_api(request.data)
            if data:
                Api.objects.create(**data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        api = self.get_object()
        serializer = self.get_serializer(api, data=request.data)
        if serializer.is_valid():
            # now do not know frontend format, so just store it
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

            # format request.data(from frontend) to backend format
            data = formater.get_backend_api(request.data)
            if data:
                API.objects.filter(id=kwargs['pk']).update(**data)
                return Response(serializer.data, response.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SuiteViewSet(viewsets.ModelViewSet):
    """
    此视图自动提供`list`，`create`，`retrieve`，`update`和`destroy`操作。
    """
    queryset = Suite.objects.all()
    serializer_class = SuiteSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @action(detail=True, methods=['get', 'post'])
    def run(self, request, pk=None):
        return Response({'status': 'suite runing！'})


class CaseViewSet(viewsets.ModelViewSet):
    """
    此视图自动提供`list`，`create`，`retrieve`，`update`和`destroy`操作。
    """
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # now do not know frontend format, so just store it
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

            # format request.data(from frontend) to backend format
            data = formater.get_backend_case(request.data)
            if data:
                Case.objects.create(**data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        case = self.get_object()
        serializer = self.get_serializer(case, data=request.data)
        if serializer.is_valid():
            # now do not know frontend format, so just store it
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

            # format request.data(from frontend) to backend format
            data = formater.get_backend_case(request.data)
            if data:
                Case.objects.filter(id=kwargs['pk']).update(**data)
                return Response(serializer.data, response.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get', 'post'])
    def run(self, request, pk=None):
        case = self.get_object()
        print('To run case: %s' % (case.name))
        # format data to httprunner format
        data = formater.get_httprunner_case(case)
        if data:
            result = task.run_case.delay(data, callback=None)
            # CaseResult.objects.create(id=kwargs['pk'])
            print(result)
            return Response(rsp_msg.CASE_RUNNING)
        else:
            return Response(rsp_msg.CASE_NOT_EXIST)

    # @run.mapping.delete
    @action(detail=True, methods=['get', 'delete'])
    def cancel_run(self, request, pk=None):
        return Response(rsp_msg.CASE_CANCEL)


class StepViewSet(viewsets.ModelViewSet):
    """
    此视图自动提供`list`，`create`，`retrieve`，`update`和`destroy`操作。
    """
    queryset = Step.objects.all()
    serializer_class = StepSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # now do not know frontend format, so just store it
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

            # format request.data(from frontend) to backend format
            data = formater.get_backend_step(request.data)
            if data:
                Step.objects.create(**data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        step = self.get_object()
        serializer = self.get_serializer(step, data=request.data)
        if serializer.is_valid():
            # now do not know frontend format, so just store it
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

            # format request.data(from frontend) to backend format
            data = formater.get_backend_step(request.data)
            if data:
                Step.objects.filter(id=kwargs['pk']).update(**data)
                return Response(serializer.data, response.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CaseResultViewSet(viewsets.ModelViewSet):
    """
    此视图自动提供`list`，`create`，`retrieve`，`update`和`destroy`操作。
    """
    queryset = CaseResult.objects.all()
    serializer_class = CaseResultSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class StepResultViewSet(viewsets.ModelViewSet):
    """
    此视图自动提供`list`，`create`，`retrieve`，`update`和`destroy`操作。
    """
    queryset = StepResult.objects.all()
    serializer_class = StepResultSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination


class SuiteResultViewSet(viewsets.ModelViewSet):
    """
    此视图自动提供`list`，`create`，`retrieve`，`update`和`destroy`操作。
    """
    queryset = SuiteResult.objects.all()
    serializer_class = SuiteResultSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ConfigViewSet(viewsets.ModelViewSet):
    """
    此视图自动提供`list`，`create`，`retrieve`，`update`和`destroy`操作。
    """
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
