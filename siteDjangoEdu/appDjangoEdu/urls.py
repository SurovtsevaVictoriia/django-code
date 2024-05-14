from django.urls import path

from . import views

urlpatterns = [
    path("", views.app_index, name="index"),
    path("take_test", views.take_test),
    path("add_question", views.add_question)
]
