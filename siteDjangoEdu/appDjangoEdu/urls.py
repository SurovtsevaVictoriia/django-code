from django.urls import path

from . import views
app_name = "appDjangoEdu"
urlpatterns = [
    path("", views.app_index, name="index"),
    path("take_test/<str:s>", views.take_test, name = "take_test"),
    path("take_test_submit/", views.take_test_submit, name = "take_test_submit"),
    path("add_question/<str:s>", views.add_question, name = "add_question"), 
    path("add_question_submit/", views.add_question_submit, name = "add_question_submit")
]
