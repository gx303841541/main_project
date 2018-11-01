from backend.models import Project
from rest_framework import serializers
from usermanager import models


class UserInfoSerializer(serializers.HyperlinkedModelSerializer):
    my_projects = serializers.HyperlinkedRelatedField(
        many=True, view_name='project-detail', queryset=Project.objects.all(), allow_null=True, required=False)

    class Meta:
        model = models.UserInfo
        fields = '__all__'
