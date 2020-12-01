from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from django.contrib import auth
from app01 import MyFormdata
from app01 import models
import random
from PIL import Image,ImageDraw,ImageFont
from io import BytesIO
from django.db.models import Count
from django.db.models.functions import TruncMonth
#BytesIO实现了在内存中读写bytes，我们创建一个BytesIO，然后写入一些bytes：
# Create your views here.

def register(request):
    form_obj = MyFormdata.MyForm()
    if request.method == 'POST':
        back_dic = {}
        form_obj = MyFormdata.MyForm(request.POST)
        if form_obj.is_valid():
            cleaned_data = form_obj.cleaned_data
            cleaned_data.pop('confirm_password')#这里是为了下面的打散字典做准备
            file_obj = request.FILES.get('avatar')
            if file_obj:
                cleaned_data['avatar'] = file_obj
            models.UserInfo.objects.create(**cleaned_data)
            back_dic = {'code':1000,'msg':'注册成功','url':'/login/'}
        else:
            back_dic = {'code':2000,'msg':form_obj.errors}
        return JsonResponse(back_dic)
    return render(request,'register.html',locals())


#生成随机RGB
def get_random():
    a = random.randint(0,255)
    b = random.randint(0,255)
    c = random.randint(0,255)
    return a,b,c

# 生成随机验证码与图片
def get_code(request):
    img_obj = Image.new('RGB',(360,35),get_random())
    img_draw = ImageDraw.Draw(img_obj)
    img_font = ImageFont.truetype('static/font/kraash.woff.ttf',17)
    code = ''
    for i in range(5):
        upper_str = chr(random.randint(65,90))
        lower_str = chr(random.randint(97,122))
        random_int = str(random.randint(0,9))
        tmp = random.choice([upper_str,lower_str,random_int])
        img_draw.text((i*60+60,0),tmp,get_random(),img_font)
        #这里的get_random()是为了控制字体颜色text(坐标，文本内容，文本颜色，字体)
        code += tmp
    print(code)
    request.session['code'] = code
    io_obj = BytesIO()
    img_obj.save(io_obj,'png')#图片的格式生成
    return HttpResponse(io_obj.getvalue())


def login(request):
    if request.method == 'POST':
        back_dic = {}
        username = request.POST.get('username')
        password = request.POST.get('password')
        code = request.POST.get('code')
        if code.upper() == request.session.get('code').upper():
            user_obj = models.UserInfo.objects.filter(username=username,password=password).first()
            if user_obj:
                auth.login(request,user_obj)
                back_dic = {'code':1000,'url':'/home/'}
            else:
                back_dic = {'code':2000,'msg':'用户名或密码错误'}
        else:
            back_dic = {'code':3000,'msg':'验证码错误'}
        return JsonResponse(back_dic)
    return render(request,'login.html',locals())



def home(request):
    article_list = models.Article.objects.all()
    return render(request,'home.html',locals())

def blog(request,username,**kwargs):
    user_obj = models.UserInfo.objects.filter(username=request.user).first()
    blog_obj = models.Blog.objects.filter(id=user_obj.blog.id)
    article_list = models.Article.objects.filter(blog=blog_obj)
    tag_list = models.Tag.objects.filter(blog=blog_obj).annotate(num=Count('article')).values_list('name','num','pk')


    classify_list = models.Classify.objects.filter(blog=blog_obj).annotate(num=Count('article')).values_list('name','num','pk')
    # month_list = models.Article.objects.filter(blog=blog).annotate(month=TruncMonth('create_time')).values('month').annotate(num=Count('pk')).values_list('month','num')
    # print(month_list)
    if kwargs:
        condition = kwargs.get('condition')
        param = kwargs.get('param')
        if condition == 'classify':
            article_list = models.Article.objects.filter(classify_id=param)
        elif condition == 'tag':
            article_list = models.Article.objects.filter(tags__id = param)
        # else:
        #     year,month = param.split('-')
        #     article_list = article_list.filter(create_time__year=year,create_time__month=month)

    return render(request,'blog.html',locals())


def article(request,username,article_id):
    user_obj = models.UserInfo.objects.filter(username=request.user).first()
    blog_obj = models.Blog.objects.filter(id=user_obj.blog.id)

    tag_list = models.Tag.objects.filter(blog=blog_obj).annotate(num=Count('article')).values_list('name','num','pk')


    classify_list = models.Classify.objects.filter(blog=blog_obj).annotate(num=Count('article')).values_list('name','num','pk')
    article_obj = models.Article.objects.filter(pk=article_id).first()


    return render(request,'article.html',locals())

import json
from django.db.models import F
from django.utils.safestring import mark_safe
def up_down(request):
    #request.user是一个对象
    if request.is_ajax():
        if request.method == 'POST':
            is_up = request.POST.get('is_up')
            is_up = json.loads(is_up)
            article_id = request.POST.get('article_id')
            back_dic = {}

            if request.user.is_authenticated():
                article_obj = models.Article.objects.filter(pk=article_id).first()
                # article_user = models.UserInfo.objects.filter(blog__article=article_obj)
                if not request.user == article_obj.blog.userinfo:
                    up_down_obj = models.UpAndDown.objects.filter(article=article_obj,user=request.user)
                    if not up_down_obj:
                        if is_up:
                            models.Article.objects.filter(pk=article_id).update(up_num=F('up_num') + 1)

                            back_dic = {'code':1000,'msg':'点赞成功'}
                        else:
                            models.Article.objects.filter(pk=article_id).update(down_num=F('down_num') + 1)
                            back_dic = {'code': 1000, 'msg': '点踩成功'}
                        models.UpAndDown.objects.create(article=article_obj, user=request.user, up_or_down=is_up)
                    else:
                        back_dic = {'code':2000,'msg':'您已点过'}
                else:
                    back_dic = {'code':3000,'msg':'自己不能给自己点赞'}
            else:
                back_dic = {'code':4000,'msg':'请先登录'}

            return JsonResponse(back_dic)
    return render(request,'article.html',locals())


from django.db import transaction

def comment(request):
    if request.is_ajax():
        if request.POST:
            back_dic = {}
            article_id = request.POST.get('article_id')
            comment = request.POST.get('comment')
            parent_id = request.POST.get('parent_id')
            with transaction.atomic():
                models.Comment.objects.create(
                    user=request.user,article_id=article_id,
                    content=comment,parent_id=parent_id
                )
                models.Article.objects.filter(pk=article_id).update(comment_num = F('comment_num') + 1)
                back_dic['msg'] = '评论成功'
            return JsonResponse(back_dic)
            # user_obj =
            # article_obj =


