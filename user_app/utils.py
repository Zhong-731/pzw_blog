from django.urls import reverse

import time
import json
import random
import requests
from django.conf import settings
from django.core.cache import cache

# Apple 验证需要 pyjwt 和 cryptography
import jwt
from jwt import PyJWKClient
def login_url(request):
    '''
        反向查找域名 : 获取登录的URL
    '''
    full_url = request.build_absolute_uri(reverse('login'))  # 'url-name'是登录的URL名称
    return full_url


GOOGLE_TOKENINFO_URL = 'https://oauth2.googleapis.com/tokeninfo'
APPLE_KEYS_URL = 'https://appleid.apple.com/auth/keys'

def verify_google_id_token(id_token):
    """
    使用 Google 的 tokeninfo 校验 id_token 并返回 payload dict
    """
    r = requests.get(GOOGLE_TOKENINFO_URL, params={'id_token': id_token}, timeout=5)
    if r.status_code != 200:
        return None
    data = r.json()
    # 可选检查 aud
    aud = data.get('aud')
    if getattr(settings, 'GOOGLE_CLIENT_ID', None) and aud and settings.GOOGLE_CLIENT_ID != aud:
        return None
    # 返回包含 sub,email,name,picture
    return data

def verify_apple_id_token(id_token):
    """
    使用 Apple 公钥 验证 id_token（JWT），返回 payload 或 None
    需要 PyJWT >=2.x
    """
    try:
        jwks_client = PyJWKClient(APPLE_KEYS_URL)
        signing_key = jwks_client.get_signing_key_from_jwt(id_token)
        payload = jwt.decode(
            id_token,
            signing_key.key,
            algorithms=["RS256"],
            audience=getattr(settings, 'APPLE_CLIENT_ID', None),
            options={"verify_exp": True}
        )
        return payload
    except Exception:
        return None

def _make_otp():
    return f"{random.randint(100000, 999999)}"

def send_sms_via_provider(phone, text):
    """
    SMS 发送占位。请替换为你实际的短信服务（如 Twilio、Aliyun、腾讯云等）。
    这里只做日志或简单 requests 支持。
    """
    # 示例（伪代码）
    # requests.post(SMS_PROVIDER_URL, data={'to': phone, 'text': text, ...})
    # 目前只是返回 True 表示发送成功
    print(f"SMS to {phone}: {text}")
    return True

def send_otp(phone, ttl=300):
    """
    生成 OTP, 存入 cache 与返回。cache key 使用 phone。
    也会创建 PhoneOTP 记录（视情况可从视图中创建）。
    """
    code = _make_otp()
    cache_key = f"phone_otp_{phone}"
    cache.set(cache_key, code, ttl)
    text = f"您的验证码是 {code}，{ttl//60}分钟内有效。"
    ok = send_sms_via_provider(phone, text)
    if ok:
        return code
    return None

def verify_otp(phone, code):
    cache_key = f"phone_otp_{phone}"
    saved = cache.get(cache_key)
    if not saved:
        return False
    if str(saved) == str(code):
        cache.delete(cache_key)
        return True
    return False