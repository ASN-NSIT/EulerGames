from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Question


class UserSignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'validate'
            })
        # for fieldname in ['username', 'password1', 'password2']:
        #     self.fields[fieldname].help_text = None
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Retype Password'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'A user with that email address already exists.')
        return email


class QuestionForm(forms.ModelForm):
    answer_input = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Enter Answer', 'class': 'validate'}))

    class Meta:
        model = Question
        fields = ('answer_input',)
