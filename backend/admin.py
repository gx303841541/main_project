from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework.authtoken.admin import TokenAdmin

from .models import (Api, Case, CaseResult, Config, Project, Step, StepResult,
                     Suite, SuiteResult)

TokenAdmin.raw_id_fields = ('user',)


class ProjectAdmin(admin.ModelAdmin):
    #fields = ['name', 'owner']
    list_display = ('name', 'owner')


class ApiAdmin(admin.ModelAdmin):
    #fields = ['name', 'url']
    list_display = ('name', 'variables', 'api_url', 'method', 'data', 'validate')


class SuiteAdmin(admin.ModelAdmin):
    #fields = ['name', 'url']
    list_display = ('name',)


class CaseAdmin(admin.ModelAdmin):
    #fields = ['name', 'url']
    list_display = ('name', 'parameters', 'variables', 'base_url')


class StepAdmin(admin.ModelAdmin):
    #fields = ['name', 'url']
    list_display = ('name', 'extract', 'variables', 'base_url', 'header', 'validate')


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
