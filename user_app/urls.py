from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(),name='login'),
    path('register/', views.RegisterView.as_view(),name='register'),
    path('password_change/', views.PasswordChangeView.as_view(),name='password_change'),
    path('user_list/', views.UserListView.as_view(),name='user_list'),
    path('user_detail/<int:pk>/', views.UserDetailView.as_view(),name='user_detail')  
]