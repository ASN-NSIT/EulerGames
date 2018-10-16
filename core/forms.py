from django import forms
from .models import Question


class QuestionForm(forms.ModelForm):
    answer_input = forms.IntegerField()
    class Meta:
        model = Question
        fields = ('answer_input',)
