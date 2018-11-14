
from django.conf.urls import include, url
from django.urls import path
from usermanager import views

urlpatterns = [
    url(r'^$', views.api_root),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    url(r'^users/$', views.UserList.as_view(), name='userinfo-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='userinfo-detail'),
]
