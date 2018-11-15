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
from celery.task.control import revoke
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
        name = request.query_params.get('name', None)

        if name:
            projects = projects.filter(name=name)

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
        apis = self.get_queryset()
        project_id = request.query_params.get('project_id', None)
        apisuite_id = request.query_params.get('apisuite_id', None)
        name = request.query_params.get('name', None)

        if name:
            api = apis.get(name=name)
            serializer = self.get_serializer(api, many=False)
            return Response(serializer.data)

        if project_id:
            apis = apis.filter(project__id=project_id)

        if apisuite_id:
            apis = apis.filter(apisuite__id=apisuite_id)


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
        tmp = serializer.data
        tmp_list = []
        for step_name in tmp['my_steps']:
            step = api.my_steps.get(name=step_name)
            case_name = step.case.name
            tmp_list.append(case_name + ' : ' + step_name)

        tmp['my_steps'] = tmp_list
        return Response(tmp)

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


class ApiSuiteViewSet(viewsets.GenericViewSet):
    """
    此视图自动提供`list`，`create`，`retrieve`，`update`和`destroy`操作。
    """
    queryset = ApiSuite.objects.all()
    serializer_class = ApiSuiteSerializer
    pagination_class = pagination.MyPageNumberPagination
    authentication_classes = ()
    permission_classes = (IsOwnerOrReadOnly, )

    # def get_serializer_class(self):
    #    if self.action == 'retrieve':
    #        return ApiSuiteWithResultSerializer

    #    return ApiSuiteSerializer

    def list(self, request, format=None):
        apisuites = self.get_queryset()
        name = request.query_params.get('name', None)
        project_id = request.query_params.get('project_id', None)

        if name:
            apisuites = apisuites.filter(name=name)

        if project_id:
            apisuites = apisuites.filter(project__id=project_id)

        page_apisuites = self.paginate_queryset(apisuites)
        serializer = self.get_serializer(page_apisuites, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # now do not know frontend format, so just store it
            serializer.save()
            return Response(rsp_msg.APISUITE_CREATE_SUCCESS)

        rsp_msg.APISUITE_FAIL['msg'] = serializer.errors
        return Response(rsp_msg.APISUITE_FAIL)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, many=False)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            # now do not know frontend format, so just store it
            serializer.save()
            return Response(rsp_msg.APISUITE_UPDATE_SUCCESS)
        rsp_msg.APISUITE_FAIL['msg'] = serializer.errors
        return Response(rsp_msg.APISUITE_FAIL)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(rsp_msg.APISUITE_DELETE_SUCCESS)


class SuiteViewSet(viewsets.GenericViewSet):
    """
    此视图自动提供`list`，`create`，`retrieve`，`update`和`destroy`操作。
    """
    queryset = Suite.objects.all()
    serializer_class = SuiteSerializer
    pagination_class = pagination.MyPageNumberPagination
    authentication_classes = ()
    permission_classes = (IsOwnerOrReadOnly, )
    task_ids = {}

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SuiteWithResultSerializer

        return SuiteSerializer

    def list(self, request, format=None):
        suites = self.get_queryset()
        name = request.query_params.get('name', None)
        project_id = request.query_params.get('project_id', None)

        if name:
            suites = suites.filter(name=name)

        if project_id:
            suites = suites.filter(project__id=project_id)

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
        result_count = int(request.query_params.get('result_count', 5))
        tmp = serializer.data
        tmp['my_suiteresults'] = tmp['my_suiteresults'][:result_count]
        return Response(tmp)

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
            task_result = task.run_suite.delay(suite=suite)

            if task_result.status in ('SUCCESS', 'FAILURE'):
                rsp_msg.SUITE_RUN_SUCCESS['task'], suite_result = task_result.get()
                rsp_msg.SUITE_RUN_SUCCESS['task'].update({
                    'id': task_result.id,
                    'status': task_result.status
                })
                rsp_msg.SUITE_RUN_SUCCESS['result'] = reverse(
                    'suiteresult-detail', args=[suite_result.pk], request=request)
                return Response(rsp_msg.SUITE_RUN_SUCCESS)

            else:
                rsp_msg.SUITE_RUNNING['task'] = {
                    'id': task_result.id,
                    'status': task_result.status
                }
                self.task_ids[task_result.id] = task_result
                rsp_msg.SUITE_RUNNING['msg'] = 'case status: %s' % (task_result.status)
                return Response(rsp_msg.SUITE_RUNNING)

        else:
            return Response(rsp_msg.SUITE_NOT_EXIST)

    @action(detail=True, methods=['get'])
    def check_run(self, request, pk=None):
        suite = self.get_object()
        if suite:
            id = request.query_params.get('id', None)
            if id:
                print('views to check run suite: %s, id: %s' % (suite.name, id))

                if id in self.task_ids:
                    task_result = self.task_ids[id]
                else:
                    task_result = None

            else:
                rsp_msg.SUITE_FAIL['msg'] = 'Not result ID!'
                return Response(rsp_msg.SUITE_FAIL)

            if task_result and task_result.status in ('SUCCESS', 'FAILURE'):
                rsp_msg.SUITE_RUN_SUCCESS['task'], suite_result = task_result.get()
                rsp_msg.SUITE_RUN_SUCCESS['task'].update({
                    'id': task_result.id,
                    'status': task_result.status
                })
                rsp_msg.SUITE_RUN_SUCCESS['result'] = reverse(
                    'suiteresult-detail', args=[suite_result.pk], request=request)
                self.task_ids.pop(id)
                return Response(rsp_msg.SUITE_RUN_SUCCESS)

            elif task_result:
                rsp_msg.SUITE_RUNNING['task'] = {
                    'id': task_result.id,
                    'status': task_result.status
                }
                rsp_msg.SUITE_RUNNING['msg'] = 'case status: %s' % (task_result.status)
                return Response(rsp_msg.SUITE_RUNNING)

            else:
                rsp_msg.SUITE_FAIL['msg'] = 'result has checked or not exist!'
                return Response(rsp_msg.SUITE_FAIL)

        else:
            return Response(rsp_msg.SUITE_NOT_EXIST)

    # @run.mapping.delete
    @action(detail=True, methods=['get', 'delete'])
    def cancel_run(self, request, pk=None):
        suite = self.get_object()
        id = request.query_params.get('id', None)
        if id:
            print('views to cancel run suite: %s, id: %s' % (suite.name, id))

            if id in self.task_ids:
                revoke(id, terminate=True)
                self.task_ids.pop(id)
                return Response(rsp_msg.CASE_CANCEL)

        rsp_msg.SUITE_FAIL['msg'] = 'Invalid task ID!'
        return Response(rsp_msg.SUITE_FAIL)


class CaseViewSet(viewsets.GenericViewSet):
    """
    此视图自动提供`list`，`create`，`retrieve`，`update`和`destroy`操作。
    """
    queryset = Case.objects.all()
    # serializer_class = CaseSerializer
    pagination_class = pagination.MyPageNumberPagination
    authentication_classes = ()
    permission_classes = (IsOwnerOrReadOnly, )

    def get_serializer_class(self):
        if self.action in ('retrieve', 'update'):
            return CaseWithResultSerializer

        return CaseSerializer

    def list(self, request, format=None):
        cases = self.get_queryset()
        project_id = request.query_params.get('project_id', None)
        suite_id = request.query_params.get('suite_id', None)
        name = request.query_params.get('name', None)
        api_id = request.query_params.get('api_id', None)

        if name:
            case = cases.get(name=name)
            serializer = self.get_serializer(case, many=False)
            return Response(serializer.data)

        if project_id:
            cases = cases.filter(project__id=project_id)

        if suite_id:
            cases = cases.filter(suites__id=suite_id)

        if api_id:
            tmp_cases = []
            try:
                api = Api.objects.get(pk=api_id)
            except Api.DoesNotExist:
                return Response("Api with ID %s doesn't exist!" % (api_id))
            my_steps = api.my_steps.all()
            for step in my_steps:
                if step.case and step.case in cases:
                    tmp_cases.append(step.case)
            cases = tmp_cases

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
        result_count = int(request.query_params.get('result_count', 5))
        tmp = serializer.data
        tmp['my_caseresults'] = tmp['my_caseresults'][:result_count]
        tmp_dict = {}
        for step_name in tmp['my_steps']:
            step = case.my_steps.get(name=step_name)
            order = step.order
            tmp_dict[order] = step_name

        tmp['my_steps'] = []
        for item in sorted(tmp_dict.keys()):
            tmp['my_steps'].append(tmp_dict[item])
        return Response(tmp)

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
        return Response(task.run_case(case=case, request=request, return_caseresult_url=True, statistics=False)[0])

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
    pagination_class = pagination.MyPageNumberPagination

    def get_serializer_class(self):
        if self.action in ('retrieve', 'update'):
            return StepWithResultSerializer

        return StepSerializer

    def list(self, request, format=None):
        steps = self.get_queryset()
        case_name = request.query_params.get('case_name', None)
        name = request.query_params.get('name', None)

        if name:
            steps = steps.filter(name=name)

        if case_name:
            steps = steps.filter(case__name=case_name)

        page_steps = self.paginate_queryset(steps)
        serializer = self.get_serializer(page_steps, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # now do not know frontend format, so just store it
            serializer.save()
            return Response(rsp_msg.STEP_CREATE_SUCCESS)

            # format request.data(from frontend) to backend format
            data = formater.get_backend_step(request.data)
            if data:
                Step.objects.create(**data)
                return Response(rsp_msg.STEP_CREATE_SUCCESS)
        rsp_msg.STEP_FAIL['msg'] = serializer.errors
        return Response(rsp_msg.STEP_FAIL)

    def retrieve(self, request, *args, **kwargs):
        step = self.get_object()
        serializer = self.get_serializer(step, many=False)
        result_count = int(request.query_params.get('result_count', 5))
        tmp = serializer.data
        tmp['my_stepresults'] = tmp['my_stepresults'][:result_count]
        return Response(tmp)

    def update(self, request, *args, **kwargs):
        step = self.get_object()
        serializer = self.get_serializer(step, data=request.data)
        if serializer.is_valid():
            # now do not know frontend format, so just store it
            serializer.save()
            return Response(rsp_msg.STEP_UPDATE_SUCCESS)

            # format request.data(from frontend) to backend format
            data = formater.get_backend_step(request.data)
            if data:
                Step.objects.filter(id=kwargs['pk']).update(**data)
                return Response(rsp_msg.STEP_UPDATE_SUCCESS)
        rsp_msg.STEP_FAIL['msg'] = serializer.errors
        return Response(rsp_msg.STEP_FAIL)

    def destroy(self, request, *args, **kwargs):
        step = self.get_object()
        my_order = step.order
        step.delete()
        for step in step.case.my_steps.order_by('order'):
            if step.order > my_order:
                step.order -= 1
                step.save()
        return Response(rsp_msg.STEP_DELETE_SUCCESS)


class CaseResultViewSet(viewsets.ModelViewSet):
    """
    此视图自动提供`list`，`create`，`retrieve`，`update`和`destroy`操作。
    """
    queryset = CaseResult.objects.all()
    serializer_class = CaseResultSerializer
    pagination_class = pagination.MyPageNumberPagination

    def list(self, request, format=None):
        results = self.get_queryset()
        name = request.query_params.get('name', None)

        if name:
            results = results.filter(name=name)

        page_results = self.paginate_queryset(results)
        serializer = self.get_serializer(page_results, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        step_results = self.get_object()
        serializer = self.get_serializer(step_results, many=False)
        tmp = serializer.data
        tmp_dict = {}
        for id, step_result_name in enumerate(tmp['my_stepresults']):
            step_result = StepResult.objects.get(name=step_result_name)
            step_name = step_result.step.name
            order = step_result.step.order
            result = step_result.result
            tmp_dict[order] = {
                'step name': step_name,
                'result': result,
                'step log': step_result_name
            }
        tmp['my_stepresults'] = []
        for item in sorted(tmp_dict.keys()):
            tmp['my_stepresults'].append(tmp_dict[item])
        return Response(tmp)


class StepResultViewSet(viewsets.ModelViewSet):
    """
    此视图自动提供`list`，`create`，`retrieve`，`update`和`destroy`操作。
    """
    queryset = StepResult.objects.all()
    serializer_class = StepResultSerializer
    pagination_class = pagination.MyPageNumberPagination

    def list(self, request, format=None):
        results = self.get_queryset()
        name = request.query_params.get('name', None)

        if name:
            results = results.filter(name=name)

        page_results = self.paginate_queryset(results)
        serializer = self.get_serializer(page_results, many=True)
        return self.get_paginated_response(serializer.data)


class SuiteResultViewSet(viewsets.ModelViewSet):
    """
    此视图自动提供`list`，`create`，`retrieve`，`update`和`destroy`操作。
    """
    queryset = SuiteResult.objects.all()
    serializer_class = SuiteResultSerializer
    pagination_class = pagination.MyPageNumberPagination

    def get_serializer_class(self):
        if self.action in ('retrieve', 'update'):
            return SuiteResultWithResultSerializer

        return SuiteResultSerializer

    def list(self, request, format=None):
        results = self.get_queryset()
        name = request.query_params.get('name', None)

        if name:
            results = results.filter(name=name)

        page_results = self.paginate_queryset(results)
        serializer = self.get_serializer(page_results, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        results = self.get_object()
        serializer = self.get_serializer(results, many=False)
        tmp = serializer.data
        for id, case_result_name in enumerate(tmp['my_caseresults']):
            case_result = CaseResult.objects.get(name=case_result_name)
            case_name = case_result.case.name
            result = case_result.result

            tmp['my_caseresults'][id] = {
                'case name': case_name,
                'result': result,
                'case log': case_result_name
            }
        return Response(tmp)


class ConfigViewSet(viewsets.ModelViewSet):
    """
    此视图自动提供`list`，`create`，`retrieve`，`update`和`destroy`操作。
    """
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer
    pagination_class = pagination.MyPageNumberPagination
    authentication_classes = ()
    permission_classes = (IsOwnerOrReadOnly, )

    def list(self, request, format=None):
        configs = self.get_queryset()
        name = request.query_params.get('name', None)

        if name:
            configs = configs.filter(name=name)

        page_configs = self.paginate_queryset(configs)
        serializer = self.get_serializer(page_configs, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(rsp_msg.CONFIG_CREATE_SUCCESS)
        rsp_msg.CONFIG_FAIL['msg'] = serializer.errors
        return Response(rsp_msg.CONFIG_FAIL)

    def retrieve(self, request, *args, **kwargs):
        config = self.get_object()
        serializer = self.get_serializer(config, many=False)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        config = self.get_object()
        serializer = self.get_serializer(config, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(rsp_msg.CONFIG_UPDATE_SUCCESS)

        rsp_msg.CONFIG_FAIL['msg'] = serializer.errors
        return Response(rsp_msg.CONFIG_FAIL)

    def destroy(self, request, *args, **kwargs):
        config = self.get_object()
        config.delete()
        return Response(rsp_msg.CONFIG_DELETE_SUCCESS)
