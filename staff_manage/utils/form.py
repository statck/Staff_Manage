# -*- coding=utf-8 -*-
# 
# GK
from staff_manage.utils.bootstrap import BootStrapModelForm
from django import forms
from staff_manage import models
from django.core.exceptions import ValidationError

class UserModelForm(BootStrapModelForm):
    name = forms.CharField(min_length=3 , label="用户名")
    password = forms.CharField(label="密码" )
    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "create_time","gender", "depart"]
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),
        # }

class PrettyModelForm(BootStrapModelForm):
    # 验证方式一：
    # mobile = forms.CharField(label="手机号",validators=[RegexValidator(r'^1[3-9]\d{9}$','手机号格式错误，必须以1开头，且为11位数字')])
    class Meta:
        model = models.PrettyNum
        fields = ["mobile","price","level","status"]
        fields = "__all__"
    # 验证方式二：
    def clean_mobile(self):  # 钩子函数
        txt_mobile = self.cleaned_data["mobile"]
        exits_flag = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exits_flag:
            raise ValidationError("号码已存在！")
        if len(txt_mobile) != 11:
            raise ValidationError("格式错误")
        return txt_mobile

class PrettyEditModelForm(BootStrapModelForm):
    mobile = forms.CharField(disabled=True, label="手机号")
    class Meta:
        model = models.PrettyNum
        fields = "__all__"