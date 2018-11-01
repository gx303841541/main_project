from django.db import models


class UserInfo(models.Model):
    create_time = models.DateTimeField('create time', auto_now_add=True)
    update_time = models.DateTimeField('update time', auto_now=True)
    username = models.CharField('user name', max_length=20, unique=True, null=False)
    password = models.CharField('password', max_length=100, null=False)
    email = models.EmailField('email', unique=True, null=False)

    class Meta:
        verbose_name = "owner"

    def __str__(self):
        return str(self.username)


class UserToken(models.Model):
    create_time = models.DateTimeField('create time', auto_now_add=True)
    update_time = models.DateTimeField('update time', auto_now=True)
    user = models.OneToOneField(to=UserInfo, on_delete=models.CASCADE)
    token = models.CharField('token', max_length=50)

    class Meta:
        verbose_name = "token"

    def __str__(self):
        return str(self.user.username + ' : ' + self.token)
