from backend.models import (Api, Case, CaseResult, Config, Project, Step,
                            StepResult, Suite, SuiteResult)
from django.contrib.auth.models import User
from rest_framework import serializers


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    #my_apis = serializers.PrimaryKeyRelatedField(many=True, queryset=Api.objects.all())
    #my_apis = ApiSerializer(many=True, read_only=True)
    my_apis = serializers.HyperlinkedRelatedField(
        many=True, view_name='api-detail', queryset=Api.objects.all(), allow_null=True, required=False)
    my_suites = serializers.HyperlinkedRelatedField(
        many=True, view_name='suite-detail', queryset=Suite.objects.all(), allow_null=True, required=False)
    my_cases = serializers.HyperlinkedRelatedField(
        many=True, view_name='case-detail', queryset=Case.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Project
        fields = '__all__'

    def create(self, *args, **kwargs):
        print(kwargs)
        return super().create(*args, **kwargs)


class ApiSerializer(serializers.HyperlinkedModelSerializer):
    #my_cases = serializers.PrimaryKeyRelatedField(many=True, queryset=Case.objects.all())
    my_cases = serializers.HyperlinkedRelatedField(
        many=True, view_name='case-detail', queryset=Case.objects.all(), allow_null=True, required=False)
    #my_steps = serializers.PrimaryKeyRelatedField(many=True, queryset=Step.objects.all())

    class Meta:
        model = Api
        fields = '__all__'


class SuiteSerializer(serializers.HyperlinkedModelSerializer):
    #my_cases = serializers.PrimaryKeyRelatedField(many=True, queryset=Case.objects.all(), allow_null=True)
    my_cases = serializers.HyperlinkedRelatedField(
        many=True, view_name='case-detail', queryset=Case.objects.all(), allow_null=True, required=False)
    #my_suiteresults = serializers.PrimaryKeyRelatedField(many=True, queryset=SuiteResult.objects.all())
    my_suiteresults = serializers.HyperlinkedRelatedField(
        many=True, view_name='suiteresult-detail', queryset=SuiteResult.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Suite
        fields = '__all__'


class CaseSerializer(serializers.HyperlinkedModelSerializer):
    #my_steps = serializers.PrimaryKeyRelatedField(many=True, queryset=Step.objects.all())
    my_steps = serializers.HyperlinkedRelatedField(
        many=True, view_name='step-detail', queryset=Step.objects.all(), allow_null=True, required=False)
    #my_caseresults = serializers.PrimaryKeyRelatedField(many=True, queryset=CaseResult.objects.all())
    my_caseresults = serializers.HyperlinkedRelatedField(
        many=True, view_name='caseresult-detail', queryset=CaseResult.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Case
        fields = '__all__'


class StepSerializer(serializers.HyperlinkedModelSerializer):
    #my_stepresults = serializers.PrimaryKeyRelatedField(many=True, queryset=StepResult.objects.all())
    my_stepresults = serializers.HyperlinkedRelatedField(
        many=True, view_name='stepresult-detail', queryset=StepResult.objects.all(), allow_null=False, required=False)

    class Meta:
        model = Step
        fields = '__all__'


class CaseResultSerializer(serializers.HyperlinkedModelSerializer):
    my_stepresults = serializers.HyperlinkedRelatedField(
        many=True, view_name='stepresult-detail', queryset=StepResult.objects.all(), allow_null=False, required=False)

    class Meta:
        model = CaseResult
        fields = '__all__'


class StepResultSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = StepResult
        fields = '__all__'


class SuiteResultSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = SuiteResult
        fields = '__all__'


class ConfigSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Config
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    #my_projects = serializers.PrimaryKeyRelatedField(many=True, queryset=Project.objects.all(), allow_null=True)
    my_projects = serializers.StringRelatedField(many=True, allow_null=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'my_projects')
