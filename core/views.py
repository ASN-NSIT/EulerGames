from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile, Question
from .forms import QuestionForm
from .decorators import check_recaptcha


def index(request):
    return render(request=request, template_name='index.html')


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
