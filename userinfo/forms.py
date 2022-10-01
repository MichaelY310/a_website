from captcha.fields import CaptchaField
from django import forms
from django.core.exceptions import ValidationError


class registerform(forms.Form):
    username = forms.CharField(min_length=3,required=True,error_messages={
        'min_length': '用户名长度不能小于3',
        'required': '用户名必须填写',
    })
    password = forms.CharField(min_length=3, required=True, error_messages={
        'min_length': '密码长度不能小于3',
        'required': '密码必须填写',
    })
    confirm = forms.CharField(required=True, error_messages={
        'required': '请确认密码',
    })

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password.isdigit():
            raise ValidationError('密码不能是纯数字')
        return password

    def clean(self):
        confirm = self.cleaned_data.get('confirm')
        password = self.cleaned_data.get('password')
        if confirm != password:
            raise ValidationError({'confirm': '两次密码输入不一致'})
        return self.cleaned_data