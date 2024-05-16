from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,  Http404
from .models_work import *
from django.urls import reverse


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
    print(request.body)
    if request.method == 'POST':
        return HttpResponseRedirect("take_test")
    
def take_test(request):
    return render(request, 'appDjangoEdu/add_question.html')

def add_question(request):
    context = {
        'value1': 3,
        'value2': 4
    }
    return render(request, 'appDjangoEdu/add_question.html', context=context)
