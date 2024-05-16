from django.urls import path

from . import views
app_name = "appDjangoEdu"
urlpatterns = [
    path("", views.app_index, name="index"),
    path("take_test", views.take_test, name = "take_test"),
    path("take_test_submit", views.take_test_submit, name = "take_test_submit"),
    path("add_question", views.add_question, name = "add_question")
]
