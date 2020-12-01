
from django import forms
from app01 import models

class MyForm(forms.Form):
    username = forms.CharField(max_length=8,min_length=3,label='用户名',widget=forms.widgets.TextInput(attrs={'class':'form-control'}),
                               error_messages={
                                   'max_length':'用户名最长8位字符',
                                   'min_length':'用户名最短3位字符',
                                   'required':'用户名不能为空'
                               })
    password = forms.CharField(max_length=8,min_length=3,label='密码',widget=forms.widgets.PasswordInput(attrs={'class':'form-control'}),
                               error_messages={
                                   'max_length':'密码最长8位字符',
                                   'min_length':'密码最短3位字符',
                                   'required':'密码不能为空'
                               })
    confirm_password = forms.CharField(max_length=8, min_length=3, label='确认密码',
                               widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'}),
                               error_messages={
                                   'max_length': '密码最长8位字符',
                                   'min_length': '密码最短3位字符',
                                   'required': '密码不能为空'
                               })
    email = forms.EmailField(label='邮箱',error_messages={
        'invalid':'邮箱格式不正确',
        'required':'邮箱不能为空'
    },widget=forms.widgets.EmailInput(attrs={'class':'form-control'}))


    def clean_username(self):
        username = self.cleaned_data.get('username')
        user_obj = models.UserInfo.objects.filter(username=username).first()
        if user_obj:
            self.add_error('username','用户名已存在')
        return username

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if not password == confirm_password:
            self.add_error('confirm_password','两次密码不一致')

        return self.cleaned_data


