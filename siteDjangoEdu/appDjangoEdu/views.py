"""views module
"""
import random
from django.shortcuts import render, redirect
from django.http import Http404
from .models_work import *


def app_index(request):
    """Contains theme selector, rshould contain a link that redirects to either
      to "Пройти тест" page or "Добавить вопрос" form
    """
    try:
        context = {
            'theme_tree': get_theme_dicts_as_json_string()
        }
    except Exception:
        raise Http404("Oops")

    return render(request, 'appDjangoEdu/app_index.html', context=context)
    # return HttpResponse("Hello, world. You're at the polls index.")


def take_test_submit(request):

    if request.method == 'POST':
        s_idx = ''
        try:
            a_idx = []
            for item in request.POST:
                theme_a = item.split('_')
                if theme_a[0] == 'theme':
                    a_idx.append(item.split('_')[-1])
        except Exception as e:
            print(e.args)

        s_idx = '&'.join(a_idx)
        print(s_idx)
        return redirect("appDjangoEdu:take_test", s=s_idx)


def take_test(request, s):
    try:
        print(s)
        theme_idxs = [int(x) for x in (s.split('&'))]
        test_questions = {'questions': []}
        for theme_idx in theme_idxs:
            theme_questions = get_questions(theme_idx)
            test_questions['questions'].extend(theme_questions)
        random.shuffle(test_questions['questions'])
    except Exception as e:
        print(e.args)
    return render(request, 'appDjangoEdu/take_test.html', context=test_questions)


def add_question_submit(request):
    if request.method == 'POST':
        try:
            (request.POST['inputQuestion'])
        except Exception:
            s_idx = []
            for item in request.POST:
                print(item, request.POST[item])
                s_idx.append(item.split('_')[-1])
            s_idx = s_idx[1]
            print(s_idx)
            return redirect("appDjangoEdu:add_question", s=s_idx)
        else:
            new_question = request.POST['inputQuestion']
            new_answer = request.POST['inputAnswer']
            theme_id = request.POST['theme_id']

            print(new_question, new_answer)
            write_new_question(theme_id=theme_id, new_question=new_question,
                               new_answer=new_answer)

            return redirect("appDjangoEdu:add_question", s=str(theme_id))


def add_question(request, s):
    if s == 'inputQuestion':
        context = {
            'questions': []
        }
        return render(request, 'appDjangoEdu/add_question.html', context=context)
    else:
        theme_idx = int(s)
        theme = get_theme_by_id(theme_idx)
        theme_questions = get_questions(theme_idx)

        context = {
            'theme': theme,
            'questions': theme_questions
        }
        return render(request, 'appDjangoEdu/add_question.html', context=context)
