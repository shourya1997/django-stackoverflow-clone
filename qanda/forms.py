from django import forms
from django.contrib.auth import get_user_model

from qanda.models import Question

class QuestionForm(forms.ModelForm):
    user = forms.ModelChoiceField(widget=forms.HiddenInput,\
        queryset=get_user_model().objects.all(),\
        disabled=True)
    class Meta:
        model = Question
        fields = ['title','question','user']

        