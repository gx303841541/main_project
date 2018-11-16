from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from usermanager.models import UserInfo

from .my_fields import ListField


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


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
    #owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_projects')
    owner = models.ForeignKey(
        UserInfo,
        on_delete=models.SET_NULL,
        related_name='my_projects',
        null=True)
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

    name = models.CharField("name", unique=True, null=False, max_length=100)
    variables = models.TextField("variables", null=True, blank=True)
    api_url = models.CharField("api_url", null=False, max_length=50)
    method = models.CharField("method", choices=method_map, default=1, max_length=50)
    headers = models.TextField("headers", null=True)
    data = models.TextField("data", null=True, blank=True)
    json = models.TextField("json", null=True, blank=True)
    params = models.TextField("params", null=True, blank=True)
    validate = models.TextField("validate", null=True, blank=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='my_apis')
    apisuite = models.ForeignKey('Apisuite', on_delete=models.SET_NULL, related_name='my_apis', null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "api"
        ordering = ('-create_time', 'name', )


# Suite model
class ApiSuite(BaseTable):
    name = models.CharField("name", unique=True, null=False, max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='my_apisuites')
    father_apisuite = models.ForeignKey('self', on_delete=models.CASCADE, null=True,
                                        blank=True, related_name='my_apisuites')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "apisuite"
        ordering = ('-create_time', 'name', )


# Suite model
class Suite(BaseTable):
    name = models.CharField("name", unique=True, null=False, max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='my_suites')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "suite"
        ordering = ('-create_time', 'name', )


# Case model
class Case(BaseTable):
    name = models.CharField("name", unique=True, null=False, max_length=100)
    parameters = models.TextField("parameters", null=True, blank=True)
    variables = models.TextField("variables", null=True, blank=True)
    base_url = models.CharField("base_url", null=False, max_length=50)
    headers = models.TextField("headers", null=True, blank=True)
    order = models.IntegerField("order", default=99)

    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name='my_cases', null=True)
    suites = models.ManyToManyField(Suite, related_name='my_cases')
    # Does apis needed?
    #apis = models.ManyToManyField(Api, related_name='my_cases')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "case"
        ordering = ('-create_time', 'name', )
        #unique_together = (("name", "suites"),)


# Step model
class Step(BaseTable):
    name = models.CharField("name", unique=True, null=False, max_length=100)
    variables = models.TextField("variables", null=True, blank=True)
    extract = models.TextField("extract", null=True, blank=True)
    base_url = models.CharField("base_url", null=True, blank=True, max_length=50)
    header = models.TextField("header", null=True, blank=True)
    validate = models.TextField("validate", null=True, blank=True)
    order = models.IntegerField("order", default=99)

    api = models.ForeignKey(Api, on_delete=models.CASCADE, related_name='my_steps')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='my_steps', null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "step"
        ordering = ('-create_time', 'name', )


# SuiteResult model
class SuiteResult(BaseTable):
    name = models.CharField("name", unique=True, null=False, max_length=100)
    content = models.TextField("content", null=True, blank=True)
    total = models.IntegerField("total cases", default=0)
    successes = models.IntegerField("pass cases", default=0)
    failures = models.IntegerField("fail cases", default=0)
    skipped = models.IntegerField("skiped cases", default=0)
    errors = models.IntegerField("error cases", default=0)
    unknow = models.IntegerField("unknow cases", default=0)
    end_time = models.DateTimeField('end time', auto_now=True)

    suite = models.ForeignKey(Suite, on_delete=models.CASCADE, related_name='my_suiteresults')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "suite result"
        ordering = ('-create_time', 'name', )


# CaseResult model
result_map = (
    ("pass", "pass"),
    ("fail", "fail"),
    ("skip", "skip"),
    ("error", "error"),
)


class CaseResult(BaseTable):
    name = models.CharField("name", unique=True, null=False, max_length=100)
    content = models.TextField("content", null=True, blank=True)
    result = models.CharField("result", choices=result_map, default=1, max_length=10)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='my_caseresults', null=True)
    suiteresult = models.ForeignKey(SuiteResult, on_delete=models.CASCADE, related_name='my_caseresults', null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "case result"
        ordering = ('-create_time', 'name', )


# CaseResult model
class StepResult(BaseTable):
    name = models.CharField("name", unique=True, null=False, max_length=100)
    content = models.TextField("content", null=True, blank=True)
    result = models.CharField("result", choices=result_map, default=1, max_length=10)
    caseresult = models.ForeignKey(CaseResult, on_delete=models.CASCADE, related_name='my_stepresults')
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name='my_stepresults')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "step result"
        ordering = ('-create_time', 'name', )


# env model
class Config(BaseTable):
    name = models.CharField("name", unique=True, null=False, max_length=100)
    ip = models.GenericIPAddressField("ip")
    port = models.IntegerField("port", default=8888)
    hostname = models.URLField("hostname", max_length=100, default='http://127.0.0.1:5000')

    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name='my_configs', null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "env variables"
        ordering = ('-create_time', 'name', )
