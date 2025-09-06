from django.urls import path

from question_app import views

urlpatterns = [
    path('comment/add/', views.ArticleCommentAddView.as_view()),
    path('comment/delete/<int:id>/', views.ArticleCommentDeleteView.as_view()),
    path('comment/list/<int:id>/', views.ArticleCommentListView.as_view()),
    path('comment/answer/', views.ArticleCommentAnswerView.as_view())
]