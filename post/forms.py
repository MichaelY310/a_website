from captcha.fields import CaptchaField
from django import forms
from django.core.exceptions import ValidationError


class registerform(forms.Form):
    title = forms.CharField(min_length=3,required=True,error_messages={
        'min_length': '标题长度不能小于3',
        'required': '标题必须填写',
    })
    description = forms.CharField(error_messages={})
    detailtext = forms.CharField(error_messages={})
    pictures = forms.FileField(error_messages={})
