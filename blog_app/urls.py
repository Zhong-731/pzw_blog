from django.urls import path

from .views import *

urlpatterns = [
    path('article/create/', ArticleCreateView.as_view()),
    path('article/delete/<int:pk>/', ArticleDeleteView.as_view()),
    path('article/detail/<int:pk>/', ArticleDetailView.as_view()),
    path('article/list/', ArticleListView.as_view()),
    path('article/all_list/', ArticleAllListView.as_view()),
]   