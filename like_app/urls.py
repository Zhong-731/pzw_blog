from django.urls import path

from . import views

urlpatterns = [
    path('like_article/add/<int:article_id>/', views.LikeArticleAddView.as_view()),
    path('like_article/delete/<int:article_id>/', views.LikeArticleDeleteView.as_view()),
    path('like_article/list/', views.LikeArticleListView.as_view()),
    path('like_comment/add/<int:comment_id>/', views.LikeCommentAddView.as_view()),
    path('like_comment/delete/<int:comment_id>/', views.LikeCommentDeteleteView.as_view()),
]