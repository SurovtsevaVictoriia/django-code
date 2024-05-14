from django.shortcuts import render
from django.http import HttpResponse


def app_index(request):
    """Contains theme selector, rshould contain a link that redirects to either
      to "Пройти тест" page or "Добавить вопрос" form
    """

    return render(request, 'app_index.html')
    # return HttpResponse("Hello, world. You're at the polls index.")


def take_test(request):
    context = {
        'value1': 1,
        'value2': 2
    }
    return render(request, 'take_test.html', context=context)


def add_question(request):
    context = {
        'value1': 3,
        'value2': 4
    }
    return render(request, 'add_question.html', context=context)
