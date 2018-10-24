from .forms import UserSignUpForm
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, reverse
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Question
from .forms import QuestionForm
from .decorators import check_recaptcha
from django.utils import timezone


def index(request):
    return render(request=request, template_name='index.html')


@login_required
def start(request):
    progress = request.user.profile.progress
    return render(request=request, template_name='start.html', context={'progress_num': progress + 1})


@login_required
def finish(request):
    if request.user.profile.progress < int(settings.NUMBER_OF_QUESTIONS):
        messages.warning(request, 'There are no shortcuts!')
        return redirect(reverse('question_detail', args=[request.user.profile.progress + 1]))
    else:
        return render(request=request, template_name='finish.html')


def register(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already registered as a valid user')
        return redirect(reverse('start'))
    if request.method == 'POST':
        userform = UserSignUpForm(request.POST)
        if userform.is_valid():
            user = userform.save()
            user.save()
            profile = Profile(user=user)
            profile.save()
            username = userform.cleaned_data.get('username')
            raw_password = userform.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'User registered successfully!')
            return redirect('start')
    else:
        userform = UserSignUpForm()
    return render(request=request, template_name='registration/register.html', context={'userform': userform})


@login_required
@check_recaptcha
def question_detail(request, num):
    user = request.user
    num = int(num)
    if num > int(settings.NUMBER_OF_QUESTIONS):
        return redirect(reverse('finish'))
    elif num > user.profile.progress + 1:
        messages.warning(request, 'There are no shortcuts!')
        return redirect(reverse('question_detail', args=[user.profile.progress + 1]))
    else:
        question = get_object_or_404(Question, number=num)
        if request.method == 'POST':
            questionform = QuestionForm(request.POST)
            if questionform.is_valid():
                if request.recaptcha_is_valid:
                    answer_response = questionform.cleaned_data.get('answer_input')
                    if answer_response == question.answer:
                        progress = user.profile.progress
                        progress = max(progress, num)
                        user.profile.progress = progress
                        user.profile.save()
                        user.save()
                        if num + 1 > int(settings.NUMBER_OF_QUESTIONS):
                            return redirect(reverse('finish'))
                        else:
                            return redirect(reverse('question_detail', args=[num + 1]))
                    else:
                        questionform.add_error(None, 'Wrong Answer, keep trying!')
                else:
                    questionform.add_error(None, 'Invalid reCAPTCHA. Please try again.')
        else:
            questionform = QuestionForm()
        return render(request=request, template_name='question.html',
                      context={'question': question, 'questionform': questionform})


@login_required
def leaderboard(request):
    profiles = Profile.objects.order_by('-progress', 'progress_time')
    durations = []
    for profile in profiles:
        d = profile.progress_time - profile.progress_start
        total_seconds = int(d.total_seconds())
        hrs = total_seconds // 3600
        min = (total_seconds % 3600) // 60
        if hrs:
            td = '{} hrs {} mins'.format(hrs, min)
        elif min:
            td = '{} mins'.format(min)
        else:
            td = '{} sec'.format(d.seconds)
        durations.append(td)
    leaderboard_data = zip(profiles, durations)
    return render(request=request, template_name='leaderboard.html', context={'leaderboard_data': leaderboard_data})
