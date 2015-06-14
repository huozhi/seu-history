from django import forms
from .models import Student
from captcha.fields import CaptchaField

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['username', 'password']


class CaptchaForm(forms.Form):
    captcha = CaptchaField()