from backend.models import (Api, Case, CaseResult, Config, Project, Step,
                            StepResult, Suite, SuiteResult)
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.utils import html, model_meta, representation


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    #owner = serializers.ReadOnlyField(source='owner.username')
    # my_apis = serializers.PrimaryKeyRelatedField(many=True, queryset=Api.objects.all())
    # my_apis = ApiSerializer(many=True, read_only=True)
    my_apis = serializers.HyperlinkedRelatedField(
        many=True, view_name='api-detail', queryset=Api.objects.all(), allow_null=True, required=False)
    my_suites = serializers.HyperlinkedRelatedField(
        many=True, view_name='suite-detail', queryset=Suite.objects.all(), allow_null=True, required=False)
    my_cases = serializers.HyperlinkedRelatedField(
        many=True, view_name='case-detail', queryset=Case.objects.all(), allow_null=True, required=False)
    my_configs = serializers.HyperlinkedRelatedField(
        many=True, view_name='config-detail', queryset=Config.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Project
        fields = '__all__'
        # fields = ('url', 'id', 'owner', 'my_apis', 'my_suites', 'my_cases', 'my_configs')

    def create(self, *args, **kwargs):
        print(kwargs)
        return super().create(*args, **kwargs)


class ApiSerializer(serializers.HyperlinkedModelSerializer):
    # my_cases = serializers.PrimaryKeyRelatedField(many=True, queryset=Case.objects.all())
    # my_cases = serializers.HyperlinkedRelatedField(
    #    many=True, view_name='case-detail', queryset=Case.objects.all(), allow_null=True, required=False)
    my_cases = serializers.SlugRelatedField(many=True, queryset=Case.objects.all(), slug_field='name', allow_null=True)
    # my_steps = serializers.PrimaryKeyRelatedField(many=True, queryset=Step.objects.all())

    #json = serializers.SerializerMethodField()

    # def get_json(self, obj):
    #    return 'Fuck you'

    class Meta:
        model = Api
        fields = '__all__'
        #fields = ('json', 'my_cases', 'name')
        # depth = 2


class SuiteSerializer(serializers.HyperlinkedModelSerializer):
    my_cases = serializers.SlugRelatedField(many=True, queryset=Case.objects.all(), slug_field='name', allow_null=True)

    class Meta:
        model = Suite
        fields = '__all__'


class SuiteWithResultSerializer(serializers.HyperlinkedModelSerializer):
    my_cases = serializers.SlugRelatedField(many=True, queryset=Case.objects.all(), slug_field='name', allow_null=True)

    my_suiteresults = serializers.SlugRelatedField(
        many=True, queryset=SuiteResult.objects.all(), slug_field='name', required=False)

    class Meta:
        model = Suite
        fields = '__all__'


class StepSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Step
        fields = '__all__'


class StepWithResultSerializer(serializers.HyperlinkedModelSerializer):
    # my_stepresults = serializers.HyperlinkedRelatedField(
    #    many=True, view_name='stepresult-detail', queryset=StepResult.objects.order_by('name'), allow_null=False, required=False)
    my_stepresults = serializers.SlugRelatedField(
        many=True, queryset=StepResult.objects.all(), slug_field='name', required=False)

    class Meta:
        model = Step
        fields = '__all__'


class CaseSerializer(serializers.HyperlinkedModelSerializer):
    my_steps = serializers.SlugRelatedField(many=True, queryset=Step.objects.all(), slug_field='name', allow_null=True)

    class Meta:
        model = Case
        fields = '__all__'
        #depth = 1


class CaseWithResultSerializer(serializers.HyperlinkedModelSerializer):
    my_steps = serializers.SlugRelatedField(many=True, queryset=Step.objects.all(), slug_field='name', allow_null=True)
    # my_steps = serializers.HyperlinkedRelatedField(
    #    many=True, view_name='step-detail', queryset=Step.objects.all().order_by('-order'), allow_null=True, required=False)
    #my_steps = StepWithResultSerializer(many=True, read_only=False)

    # my_caseresults = serializers.PrimaryKeyRelatedField(many=True, queryset=CaseResult.objects.all())
    # my_caseresults = serializers.HyperlinkedRelatedField(
    #    many=True, view_name='caseresult-detail', queryset=CaseResult.objects.all(), allow_null=True, required=False)
    my_caseresults = serializers.SlugRelatedField(
        many=True, queryset=CaseResult.objects.all(), slug_field='name', required=False)

    class Meta:
        model = Case
        fields = '__all__'
        #depth = 1

    def createx(self, validated_data):
        apis = validated_data.pop('apis')
        suites = validated_data.pop('suites')
        my_steps_datas = validated_data.pop('my_steps')

        case = Case.objects.create(**validated_data)
        for api in apis:
            api = Api.objects.get(name=api)
            api.my_cases.add(case)

        for suite in suites:
            suite = Suite.objects.get(name=suite)
            suite.my_cases.add(case)

        for my_steps_data in my_steps_datas:
            my_steps_data.pop('case')
            Step.objects.get_or_create(case=case, **my_steps_data)
        return case


class CaseResultSerializer(serializers.HyperlinkedModelSerializer):
    # my_stepresults = serializers.HyperlinkedRelatedField(
    #    many=True, view_name='stepresult-detail', queryset=StepResult.objects.all(), allow_null=False, required=False)

    my_stepresults = serializers.SlugRelatedField(
        many=True, queryset=StepResult.objects.all(), slug_field='name', required=False)

    class Meta:
        model = CaseResult
        fields = '__all__'


class StepResultSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = StepResult
        fields = '__all__'
        read_only_fieids = ('content',)


class SuiteResultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SuiteResult
        fields = '__all__'


class SuiteResultWithResultSerializer(serializers.HyperlinkedModelSerializer):
    # my_caseresults = serializers.HyperlinkedRelatedField(
    #   many=True, view_name='caseresult-detail', queryset=CaseResult.objects.all(), allow_null=True, required=False)

    my_caseresults = serializers.SlugRelatedField(
        many=True, queryset=CaseResult.objects.all(), slug_field='name', required=False)

    class Meta:
        model = SuiteResult
        fields = '__all__'


class ConfigSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Config
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # my_projects = serializers.PrimaryKeyRelatedField(many=True, queryset=Project.objects.all(), allow_null=True)
    my_projects = serializers.StringRelatedField(many=True, allow_null=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'my_projects')
