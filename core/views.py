
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout
from django.views.generic import CreateView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserSignUpForm
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile, Question
from .forms import QuestionForm
from .decorators import check_recaptcha

def index(request):
    return render(request=request, template_name='index.html')

def signup(request):
    if request.method == 'POST':
        userform = UserSignUpForm(request.POST, prefix='userform')
        if userform.is_valid():
            user = userform.save()
            user.save()
            profile = Profile(user=user)
            profile.save()
            username = userform.cleaned_data.get('username')
            raw_password = userform.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        userform = UserSignUpForm(prefix='userform')
    return render(request=request, template_name='signup/signup.html',context={'userform': userform})

@login_required
@check_recaptcha
def question_detail(request, id):
    question = get_object_or_404(Question, pk=id)
    if request.method == 'POST':
        questionform = QuestionForm(request.POST)
        if questionform.is_valid():
            if request.recaptcha_is_valid:
                answer_response = questionform.cleaned_data.get('answer_input')
                if answer_response == question.answer:
                    current_progress = user.profile.progress
                    current_progress += 1
                    user.profile.progress = current_progress
                    user.profile.save()
                    user.save()
                # messages.success(request, 'User registered successfully')
                return redirect(reverse('index'))
            else:
                questionform.add_error(None, 'Invalid reCAPTCHA. Please try again.')
    else:
        questionform = QuestionForm()
    return render(request=request, template_name='question.html', context={'question':question, 'questionform':questionform})


def leaderboard(request):
    u=Profile.objects.order_by('-progress')
    return render(request=request,template_name='leaderboard.html',context={'profiles':u})
