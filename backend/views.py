import json
import os
import sys
import time
from datetime import datetime

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


class ProjectViewSet(viewsets.GenericViewSet):
    """
    此视图自动提供`list`，`create`，`retrieve`，`update`和`destroy`操作。
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = pagination.MyPageNumberPagination
    authentication_classes = ()
    permission_classes = (IsOwnerOrReadOnly, )
    # filter_backends = (filters.OrderingFilter,)
    # search_fields = ('name',)
    # ordering_fields = ('create_time', 'name')

    # def perform_create(self, serializer):
    #    serializer.save(owner=self.request.user)

    def list(self, request, format=None):
        projects = self.get_queryset()
        page_projects = self.paginate_queryset(projects)
        serializer = self.get_serializer(page_projects, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, format=None):
        print(dir(request.META))
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # now do not know frontend format, so just store it
            serializer.save()
            return Response(rsp_msg.PROJECT_CREATE_SUCCESS)

            # format request.data(from frontend) to backend format
            data = formater.get_backend_api(request.data)
            if data:
                Project.objects.create(**data)
                return Response(rsp_msg.PROJECT_CREATE_SUCCESS)
        rsp_msg.PROJECT_FAIL['msg'] = serializer.errors
        return Response(rsp_msg.PROJECT_FAIL)

    def retrieve(self, request, *args, **kwargs):
        project = self.get_object()
        serializer = self.get_serializer(project, many=False)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        project = self.get_object()
        serializer = self.get_serializer(project, data=request.data)
        if serializer.is_valid():
            # now do not know frontend format, so just store it
            serializer.save()
            return Response(rsp_msg.PROJECT_UPDATE_SUCCESS)

            # format request.data(from frontend) to backend format
            data = formater.get_backend_api(request.data)
            if data:
                Project.objects.filter(id=kwargs['pk']).update(**data)
                return Response(rsp_msg.PROJECT_UPDATE_SUCCESS)
        rsp_msg.PROJECT_FAIL['msg'] = serializer.errors
        return Response(rsp_msg.PROJECT_FAIL)

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        project.delete()
        return Response(rsp_msg.PROJECT_DELETE_SUCCESS)


class ApiViewSet(viewsets.ModelViewSet):
    """
    此视图自动提供`list`，`create`，`retrieve`，`update`和`destroy`操作。
    """
    queryset = Api.objects.all()
    serializer_class = ApiSerializer
    pagination_class = pagination.MyPageNumberPagination
    authentication_classes = ()
    permission_classes = (IsOwnerOrReadOnly, )

    def list(self, request, format=None):
        project_id = request.query_params.get('project_id', None)
        name = request.query_params.get('name', None)
        if name:
            api = self.get_queryset().get(name=name)
            serializer = self.get_serializer(api, many=False)
            return Response(serializer.data)
        elif project_id:
            apis = self.get_queryset().filter(project__id=project_id)
        else:
            apis = self.get_queryset()

        page_apis = self.paginate_queryset(apis)
        serializer = self.get_serializer(page_apis, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # now do not know frontend format, so just store it
            serializer.save()
            return Response(rsp_msg.API_CREATE_SUCCESS)

            # format request.data(from frontend) to backend format
            data = formater.get_backend_api(request.data)
            if data:
                Api.objects.create(**data)
                return Response(rsp_msg.API_CREATE_SUCCESS)
        rsp_msg.API_FAIL['msg'] = serializer.errors
        return Response(rsp_msg.API_FAIL)

    def retrieve(self, request, *args, **kwargs):
        api = self.get_object()
        serializer = self.get_serializer(api, many=False)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        api = self.get_object()
        serializer = self.get_serializer(api, data=request.data)
        if serializer.is_valid():
            # now do not know frontend format, so just store it
            serializer.save()
            return Response(rsp_msg.API_UPDATE_SUCCESS)

            # format request.data(from frontend) to backend format
            data = formater.get_backend_api(request.data)
            if data:
                API.objects.filter(id=kwargs['pk']).update(**data)
                return Response(rsp_msg.API_UPDATE_SUCCESS)
        rsp_msg.API_FAIL['msg'] = serializer.errors
        return Response(rsp_msg.API_FAIL)

    def destroy(self, request, *args, **kwargs):
        api = self.get_object()
        api.delete()
        return Response(rsp_msg.API_DELETE_SUCCESS)


class SuiteViewSet(viewsets.GenericViewSet):
    """
    此视图自动提供`list`，`create`，`retrieve`，`update`和`destroy`操作。
    """
    queryset = Suite.objects.all()
    serializer_class = SuiteSerializer
    pagination_class = pagination.MyPageNumberPagination
    authentication_classes = ()
    permission_classes = (IsOwnerOrReadOnly, )

    def list(self, request, format=None):
        project_id = request.query_params.get('project_id', None)
        if project_id:
            suites = self.get_queryset().filter(project__id=project_id)
        else:
            suites = self.get_queryset()
        page_suites = self.paginate_queryset(suites)
        serializer = self.get_serializer(page_suites, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # now do not know frontend format, so just store it
            serializer.save()
            return Response(rsp_msg.SUITE_CREATE_SUCCESS)

            # format request.data(from frontend) to backend format
            data = formater.get_backend_api(request.data)
            if data:
                Suite.objects.create(**data)
                return Response(rsp_msg.SUITE_CREATE_SUCCESS)
        rsp_msg.SUITE_FAIL['msg'] = serializer.errors
        return Response(rsp_msg.SUITE_FAIL)

    def retrieve(self, request, *args, **kwargs):
        suite = self.get_object()
        serializer = self.get_serializer(suite, many=False)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        suite = self.get_object()
        serializer = self.get_serializer(suite, data=request.data)
        if serializer.is_valid():
            # now do not know frontend format, so just store it
            serializer.save()
            return Response(rsp_msg.SUITE_UPDATE_SUCCESS)

            # format request.data(from frontend) to backend format
            data = formater.get_backend_api(request.data)
            if data:
                Suite.objects.filter(id=kwargs['pk']).update(**data)
                return Response(rsp_msg.SUITE_UPDATE_SUCCESS)
        rsp_msg.SUITE_FAIL['msg'] = serializer.errors
        return Response(rsp_msg.SUITE_FAIL)

    def destroy(self, request, *args, **kwargs):
        suite = self.get_object()
        suite.delete()
        return Response(rsp_msg.SUITE_DELETE_SUCCESS)

    @action(detail=True, methods=['get', 'post'])
    def run(self, request, pk=None):
        suite = self.get_object()
        print('views to run suite: %s' % (suite.name))
        if suite:
            task_id = task.run_suite.delay(suite=suite, request=request)
            print(var(task_id))
            rsp_msg.SUITE_RUNNING['task'] = {
                'id': task_id,
                'status': task_id.status
            }
            return Response(rsp_msg.SUITE_RUNNING)

        else:
            return Response(rsp_msg.SUITE_NOT_EXIST)

    # @run.mapping.delete
    @action(detail=True, methods=['get', 'delete'])
    def cancel_run(self, request, pk=None):
        return Response(rsp_msg.CASE_CANCEL)


class CaseViewSet(viewsets.ModelViewSet):
    """
    此视图自动提供`list`，`create`，`retrieve`，`update`和`destroy`操作。
    """
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    pagination_class = pagination.MyPageNumberPagination
    authentication_classes = ()
    permission_classes = (IsOwnerOrReadOnly, )

    def list(self, request, format=None):
        project_id = request.query_params.get('project_id', None)
        name = request.query_params.get('name', None)
        if name:
            case = self.get_queryset().get(name=name)
            serializer = self.get_serializer(case, many=False)
            return Response(serializer.data)
        elif project_id:
            cases = self.get_queryset().filter(project__id=project_id)
        else:
            cases = self.get_queryset()

        page_cases = self.paginate_queryset(cases)
        serializer = self.get_serializer(page_cases, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # now do not know frontend format, so just store it
            serializer.save()
            return Response(rsp_msg.CASE_CREATE_SUCCESS)

            # format request.data(from frontend) to backend format
            data = formater.get_backend_case(request.data)
            if data:
                Case.objects.create(**data)
                return Response(rsp_msg.CASE_CREATE_SUCCESS)
        rsp_msg.CASE_FAIL['msg'] = serializer.errors
        return Response(rsp_msg.CASE_FAIL)

    def retrieve(self, request, *args, **kwargs):
        case = self.get_object()
        serializer = self.get_serializer(case, many=False)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        case = self.get_object()
        serializer = self.get_serializer(case, data=request.data)
        if serializer.is_valid():
            # now do not know frontend format, so just store it
            serializer.save()
            return Response(rsp_msg.CASE_UPDATE_SUCCESS)

            # format request.data(from frontend) to backend format
            data = formater.get_backend_case(request.data)
            if data:
                Case.objects.filter(id=kwargs['pk']).update(**data)
                return Response(rsp_msg.CASE_UPDATE_SUCCESS)
        rsp_msg.CASE_FAIL['msg'] = serializer.errors
        return Response(rsp_msg.CASE_FAIL)

    def destroy(self, request, *args, **kwargs):
        case = self.get_object()
        case.delete()
        return Response(rsp_msg.CASE_DELETE_SUCCESS)

    @action(detail=True, methods=['get', 'post'])
    def run(self, request, pk=None):
        case = self.get_object()
        print('views to run case: %s' % (case.name))
        return Response(task.run_case(case=case, request=request, return_caseresult_url=True, statistics=False))

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


class StepResultViewSet(viewsets.ModelViewSet):
    """
    此视图自动提供`list`，`create`，`retrieve`，`update`和`destroy`操作。
    """
    queryset = StepResult.objects.all()
    serializer_class = StepResultSerializer
    pagination_class = PageNumberPagination


class SuiteResultViewSet(viewsets.ModelViewSet):
    """
    此视图自动提供`list`，`create`，`retrieve`，`update`和`destroy`操作。
    """
    queryset = SuiteResult.objects.all()
    serializer_class = SuiteResultSerializer


class ConfigViewSet(viewsets.ModelViewSet):
    """
    此视图自动提供`list`，`create`，`retrieve`，`update`和`destroy`操作。
    """
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer
