from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserInfo(AbstractUser):
    avatar = models.FileField(upload_to='avatar/',default='static/default.jpg')
    phone = models.BigIntegerField(null=True)
    blog = models.OneToOneField(to='Blog',null=True)
    class Meta:
        verbose_name_plural = "用户表"

    def __str__(self):
        return self.username



class Blog(models.Model):
    name = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    site_theme = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=100)
    abstract = models.CharField(max_length=255,null=True)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

    #优化字段
    up_num = models.IntegerField(default=0)
    down_num = models.IntegerField(default=0)
    comment_num = models.IntegerField(default=0)

    # 外键
    tags = models.ManyToManyField(to='Tag',through='Article2Tag',through_fields=('article','tags'))
    classify = models.ForeignKey(to='Classify',null=True)
    blog = models.ForeignKey(to='Blog',null=True)
    def __str__(self):
        return self.title



class UpAndDown(models.Model):
    up_or_down = models.BooleanField()
    # create_time = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(to='Article')
    user = models.ForeignKey(to='UserInfo')

class Tag(models.Model):
    name = models.CharField(max_length=20)
    blog = models.ForeignKey(to='Blog')
    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(to='UserInfo')
    content = models.CharField(max_length=255)
    parent_id = models.ForeignKey(to='self',null=True)
    create_time = models.DateTimeField(auto_now_add=True)

    article = models.ForeignKey(to='Article')

class Article2Tag(models.Model):
    tags = models.ForeignKey(to='Tag')
    article = models.ForeignKey(to='Article')


class Classify(models.Model):
    name = models.CharField(max_length=20)
    blog = models.ForeignKey(to='Blog',null=True)
    def __str__(self):
        return self.name