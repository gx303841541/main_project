from django.contrib import admin
from django.contrib.auth.models import User

from .models import (Api, Case, CaseResult, Config, Project, Step, StepResult,
                     Suite, SuiteResult)


class ProjectAdmin(admin.ModelAdmin):
    #fields = ['name', 'owner']
    list_display = ('name', 'owner')


class ApiAdmin(admin.ModelAdmin):
    #fields = ['name', 'url']
    list_display = ('name', 'variables', 'api_url', 'method', 'header', 'body', 'validators')


class SuiteAdmin(admin.ModelAdmin):
    #fields = ['name', 'url']
    list_display = ('name',)


class CaseAdmin(admin.ModelAdmin):
    #fields = ['name', 'url']
    list_display = ('name', 'parameters', 'variables', 'base_url', 'header', 'validators')


class StepAdmin(admin.ModelAdmin):
    #fields = ['name', 'url']
    list_display = ('name', 'extractors', 'variables', 'base_url', 'header', 'validators')


class CaseResultAdmin(admin.ModelAdmin):
    #fields = ['name', 'url']
    list_display = ('name', )


class StepResultAdmin(admin.ModelAdmin):
    #fields = ['name', 'url']
    list_display = ('name', )


class SuiteResultAdmin(admin.ModelAdmin):
    #fields = ['name', 'url']
    list_display = ('name', )


class ConfigAdmin(admin.ModelAdmin):
    #fields = ['name', 'url']
    list_display = ('name', 'hostname')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Api, ApiAdmin)
admin.site.register(Suite, SuiteAdmin)
admin.site.register(Case, CaseAdmin)
admin.site.register(Step, StepAdmin)
admin.site.register(CaseResult, CaseResultAdmin)
admin.site.register(StepResult, StepResultAdmin)
admin.site.register(SuiteResult, SuiteResultAdmin)
admin.site.register(Config, ConfigAdmin)
