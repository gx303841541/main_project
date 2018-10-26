from django.contrib.auth.models import User
from django.db import models

from .my_fields import ListField


class BaseTable(models.Model):
    create_time = models.DateTimeField('create time', auto_now_add=True)
    update_time = models.DateTimeField('update time', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        verbose_name = "common field"


# project model
class Project(BaseTable):
    name = models.CharField("project name", unique=True, null=False, max_length=40)
    owner = models.ForeignKey(User, related_name='my_projects', on_delete=models.CASCADE)
    #owner = models.ForeignKey(User, on_delete=models.CASCADE)
    desc = models.CharField("project description", null=False, max_length=200)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        """
        传进来的是user的name。
        """
        #self.owner = User.objects.filter(username='kobe')[0]
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "project"
        ordering = ('-create_time', 'name', )


# Api model
class Api(BaseTable):

    method_map = (
        ("GET", "GET"),
        ("POST", "POST"),
        ("PUT", "PUT"),
        ("DELETE", "DELETE"),
    )

    name = models.CharField("name", null=False, max_length=100, unique=True)
    variables = models.TextField("variables", null=True, blank=True)
    api_url = models.CharField("api_url", null=False, max_length=50)
    method = models.CharField("method", choices=method_map, default=1, max_length=50)
    header = models.TextField("header", null=True)
    body = models.TextField("body", null=False)
    validators = models.TextField("validators", null=True, blank=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='my_apis')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "api"
        ordering = ('-create_time', 'name', )


# Suite model
class Suite(BaseTable):
    name = models.CharField("name", null=False, max_length=100, unique=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='my_suites')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "suite"
        ordering = ('-create_time', 'name', )


# Case model
class Case(BaseTable):
    name = models.CharField("name", null=False, max_length=100, unique=True)
    parameters = models.TextField("parameters", null=True, blank=True)
    variables = models.TextField("variables", null=True, blank=True)
    base_url = models.CharField("base_url", null=False, max_length=50)
    header = models.TextField("header", null=True, blank=True)
    validators = models.TextField("validators", null=True, blank=True)

    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name='my_cases', null=True)
    suites = models.ManyToManyField(Suite, related_name='my_cases')
    # Does apis needed?
    apis = models.ManyToManyField(Api, related_name='my_cases')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "case"
        ordering = ('-create_time', 'name', )


# Step model
class Step(BaseTable):
    name = models.CharField("name", null=False, max_length=100, unique=True)
    variables = models.TextField("variables", null=True, blank=True)
    extractors = models.TextField("extractors", null=True, blank=True)
    base_url = models.CharField("base_url", null=True, blank=True, max_length=50)
    header = models.TextField("header", null=True)
    validators = models.TextField("validators", null=True, blank=True)
    order = models.IntegerField("order", default=99)

    api = models.ForeignKey(Api, on_delete=models.CASCADE, related_name='my_steps')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='my_steps')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "step"
        ordering = ('-create_time', 'name', )


# CaseResult model
class CaseResult(BaseTable):
    name = models.CharField("name", null=False, max_length=100, unique=True)
    content = models.TextField("content", null=True, blank=True)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='my_caseresults')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "case result"
        ordering = ('-create_time', 'name', )


# CaseResult model
class StepResult(BaseTable):
    name = models.CharField("name", null=False, max_length=100, unique=True)
    content = models.TextField("content", null=True, blank=True)
    caseresult = models.ForeignKey(CaseResult, on_delete=models.CASCADE, related_name='my_stepresults')
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name='my_stepresults')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "step result"
        ordering = ('-create_time', 'name', )


# SuiteResult model
class SuiteResult(BaseTable):
    name = models.CharField("name", null=False, max_length=100, unique=True)
    content = models.TextField("content", null=True, blank=True)
    total = models.IntegerField("total cases", default=0)
    pass_nu = models.IntegerField("pass cases", default=0)
    fail_nu = models.IntegerField("fail cases", default=0)
    skip_nu = models.IntegerField("skiped cases", default=0)
    end_time = models.DateTimeField('end time', auto_now=True)

    suite = models.ForeignKey(Suite, on_delete=models.CASCADE, related_name='my_suiteresults')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "suite result"
        ordering = ('-create_time', 'name', )


# env model
class Config(BaseTable):
    name = models.CharField("name", null=False, max_length=100, unique=True)
    ip = models.GenericIPAddressField("ip")
    port = models.IntegerField("port", default=8888)
    hostname = models.URLField("hostname", max_length=100, default='http://')

    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name='my_configs', null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "env variables"
        ordering = ('-create_time', 'name', )
