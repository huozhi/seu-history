from django import forms
from .models import ChoiceProblem, ToFProblem

class ChoiceProblemForm(forms.ModelForm):
    class Meta:
        model = ChoiceProblem
        fields = ['id', 'correct']


class ToFProblemForm(forms.ModelForm):
    class Meta:
        model = ToFProblem
        fields = ['id', 'correct']

