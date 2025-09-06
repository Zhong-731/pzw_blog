from django.urls import reverse

def login_url(request):
    '''
        反向查找域名 : 获取登录的URL
    '''
    full_url = request.build_absolute_uri(reverse('login'))  # 'url-name'是登录的URL名称
    return full_url