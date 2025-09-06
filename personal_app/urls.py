from django.urls import path

from .views import *

urlpatterns = [
    path("add/", PersonalAddView.as_view()),
    path("update/", PersonalUpdateView.as_view()),
    path("detail/", PersonalDetailView.as_view()),
]