from django.urls import path    
from . import views

urlpatterns = [
    path('add/<int:article_id>/', views.CollectArticleAddView.as_view()),
    path('delete/<int:article_id>/', views.CollectArticleDeleteView.as_view()),
    path('list/', views.CollectArticleListView.as_view()),
]