from django.shortcuts import render
# from . import data


def index(request):
    return render(request, 'index.html')


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
