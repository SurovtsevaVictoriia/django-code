from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect,  Http404
from .models_work import *
from django.urls import reverse
import random


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
        sIdx = ''
        for idx in get_all_theme_ids():    
            try:
                if(request.POST['theme_'+str(idx)]):
                    if sIdx == '':
                        sIdx += str(idx)
                    else:
                        sIdx += '&' + str(idx)
            except Exception as e:
                print(e.args, idx, 'this id is not selected')
        print(sIdx)
        return redirect("appDjangoEdu:take_test", s = sIdx)
    
def take_test(request, s):
    try:
        print(s)
        theme_idxs = [int(x) for x in (s.split('&'))]
        test_questions = {'questions':[]}
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
        except Exception as e:
            print('lolll')
            sIdx = []
            for item in request.POST:
                print(item, request.POST[item])
                sIdx.append(item.split('_')[-1])
            sIdx = sIdx[1]
            print(sIdx)
            return redirect("appDjangoEdu:add_question", s = sIdx)
        else:
            newQuestion = request.POST['inputQuestion']
            newAnswer = request.POST['inputAnswer']
            theme_id = request.POST['theme_id']
            
            print(newQuestion, newAnswer)
            write_new_question(theme_id=theme_id, new_question= newQuestion, new_answer= newAnswer)
            # for item in request.POST:
            #     print(item, request.POST[item])
            # print('yoo')
            return redirect("appDjangoEdu:add_question", s = str(theme_id))
            

        

        # if request.POST['inputQuestion']:
        #     for item in request.POST:
        #         print(item, request.POST[item])
        #     print('yoo')
        #     theme_id = request.POST['theme_id']
        #     return redirect("appDjangoEdu:add_question", s = theme_id)
        # else:
        #     sIdx = []
        #     for item in request.POST:
        #         print(item, request.POST[item])
        #         sIdx.append(item.split('_')[-1])
        #     sIdx = sIdx[1]
        #     print(sIdx)
        #     return redirect("appDjangoEdu:add_question", s = sIdx)

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
            'theme' : theme, 
            'questions' : theme_questions
        }
        return render(request, 'appDjangoEdu/add_question.html', context=context)
