#!/usr/bin/env python
# encoding: utf-8
'''
@author: Limz
@mail: limz@yisa.com
@name: form.py
@Create time: 2018/5/8 11:41
@IDE: PyCharm
@Description:
'''

from django import forms
from django.contrib import auth



class LoginUserForm(forms.Form):
    username = forms.CharField(label=u'账 号', error_messages={'required': u'账号不能为空'},
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'User ID', 'autofocus': 'True'}))
    password = forms.CharField(label=u'密 码', error_messages={'required': u'密码不能为空'},
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Password'}))

    def __init__(self,*args, **kwargs):
        self.user_cache = ''
        super(LoginUserForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        print username
        password = self.cleaned_data.get('password')
        if username and password:
            self.user_cache = auth.authenticate(username=username,password=password)
            if self.user_cache is None:
                raise forms.ValidationError(u'账号密码不匹配！')
            elif not self.user_cache.is_active:
                raise forms.ValidationError(u'账号被禁用！')
        return self.cleaned_data

    def get_user(self):
        return self.user_cache

class registerForm(forms.Form):
    new_username = forms.CharField(label=u'账 号',
         widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'username', 'autocomplete': 'off', 'class': 'form-control placeholder-no-fix'}))
    new_password = forms.CharField(label=u'密 码',
         widget=forms.PasswordInput(attrs={'type': 'password', 'placeholder': 'Password', 'autocomplete': 'off', 'class': 'form-control placeholder-no-fix'}))
    new_email = forms.EmailField(label=u'电子邮件',
         widget=forms.EmailInput(attrs={'type': 'text', 'placeholder': 'Email', 'autocomplete': 'off', 'class': 'form-control placeholder-no-fix'}))
