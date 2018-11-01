from django.contrib import admin

from .models import UserInfo, UserToken


class UserInfoAdmin(admin.ModelAdmin):
    #fields = ['name', 'owner']
    list_display = ('username',)


class UserTokenAdmin(admin.ModelAdmin):
    #fields = ['name', 'url']
    list_display = ('token',)


admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(UserToken, UserTokenAdmin)
