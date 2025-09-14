from django.urls import path

from . import views

urlpatterns = [
    # 短信验证码
    path('sms_code/', views.SendSMSView.as_view(), name='sms_code'),
    # 手机号登录路由
    path('phone_login/', views.PhoneLoginView.as_view(), name='phone_login'),
    # Google登录路由
    path('google_login/', views.GoogleLoginView.as_view(), name='google_login'),
    # 手机号注册路由
    path('phone_register/', views.PhoneRegisterView.as_view(),name='phone_register'),
    path('password_change/', views.PasswordChangeView.as_view(),name='password_change'),
    
    # 用户路由模块
    path('user_list/', views.UserListView.as_view(),name='user_list'),
    path('user_detail/<int:pk>/', views.UserDetailView.as_view(),name='user_detail'),
    # 第三方/手机认证接口（与你前端保持一致）

]