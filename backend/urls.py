from django.conf.urls import include, url
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

# urlpatterns = [
#    path('', views.index, name='index'),
# ]

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet)
router.register(r'apis', views.ApiViewSet)
router.register(r'suites', views.SuiteViewSet)
router.register(r'cases', views.CaseViewSet)
router.register(r'steps', views.StepViewSet)
router.register(r'caseresults', views.CaseResultViewSet)
router.register(r'stepresults', views.StepResultViewSet)
router.register(r'suiteresults', views.SuiteResultViewSet)
router.register(r'envs', views.ConfigViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),

    # users
    #url(r'^users/$', views.UserList.as_view(), name='users-list'),
    #url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),
]


#app_name = 'backend'
urlpatterns2 = format_suffix_patterns([
    url(r'^$', views.api_root),
    #url(r'^', include(router.urls)),

    # users
    url(r'^users/$', views.UserList.as_view(), name='users-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),

    # project
    #url(r'^projects/$', views.projects_list, name='projects-list'),
    #url(r'^projects/(?P<pk>[0-9]+)/$', views.project_detail, name='project-detail'),
    url(r'^projects/$', views.ProjectViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='projects-list'),
    url(r'^projects/(?P<pk>[0-9]+)/$', views.ProjectViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='project-detail'),

    # api
    url(r'^apis/$', views.ApiViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='apis-list'),
    url(r'^apis/(?P<pk>[0-9]+)/$', views.ApiViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='api-detail'),

    # suite
    url(r'^suites/$', views.SuiteViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='suites-list'),
    url(r'^suites/(?P<pk>[0-9]+)/$', views.SuiteViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='suite-detail'),

    # case
    url(r'^cases/$', views.CaseViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='cases-list'),
    url(r'^cases/(?P<pk>[0-9]+)/$', views.CaseViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='case-detail'),


    # case
    url(r'^steps/$', views.StepViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='steps-list'),
    url(r'^steps/(?P<pk>[0-9]+)/$', views.StepViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='step-detail'),

    # caseresults
    url(r'^caseresults/$', views.CaseResultViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='caseresults-list'),
    url(r'^caseresults/(?P<pk>[0-9]+)/$', views.CaseResultViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='caseresult-detail'),


    # suiteresults
    url(r'^suiteresults/$', views.SuiteResultViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='suiteresults-list'),
    url(r'^suiteresults/(?P<pk>[0-9]+)/$', views.SuiteResultViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='suiteresult-detail'),

    # configs
    url(r'^configs/$', views.ConfigViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='configs-list'),
    url(r'^configs/(?P<pk>[0-9]+)/$', views.ConfigViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='config-detail'),
])
