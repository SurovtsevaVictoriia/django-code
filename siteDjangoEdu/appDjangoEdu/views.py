from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'app_index.html')
    # return HttpResponse("Hello, world. You're at the polls index.")

def page1(request):
    context = {
        'value1': 1,
        'value2': 2
    }
    return render(request, 'page1.html', context=context)


def page2(request):
    context = {
        'value1': 3,
        'value2': 4
    }
    return render(request, 'page2.html', context=context)
