from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from user_app.token import verify_token
from user_app.models import User
from blog_app.models import Article
from .serializers import CollectArticleListSerializer
from .models import CollectArticle

# Create your views here.
class CollectArticleAddView(APIView):
    def post(self,request, article_id):
        '''
            增加文章收藏
        '''
        data = verify_token(request.META.get("HTTP_AUTHORIZATION"))
        if data:
            user = User.objects.get(phone=data.get('phone'))
            article = Article.objects.get(id=article_id)
            try:
                CollectArticle.objects.create(article=article, user=user)
                return Response({
                    "code" : status.HTTP_201_CREATED,
                    'msg' : '文章收藏成功'
                })
            except Exception as e:
                return Response({
                    'code' : status.HTTP_400_BAD_REQUEST,
                    'msg' : '文章收藏失败'
                })
        else:
            return Response({
                "code" : status.HTTP_401_UNAUTHORIZED,
                'msg' : '请先登录'
            })
        
class CollectArticleDeleteView(APIView):
    def delete(self,request,article_id):
        '''
            取消文章收藏
        '''
        # 获取用户
        data = verify_token(request.META.get('HTTP_AUTHORIZATION'))
        if data:
            user = User.objects.get(phone = data.get('phone'))
            article = Article.objects.get(id = article_id)
            try:
                CollectArticle.objects.filter(article = article,user = user).delete()
                return Response({
                    'code' : status.HTTP_200_OK,
                    'msg' : '取消收藏成功'
                })
            except Exception as e:
                return Response({
                    'code' : status.HTTP_400_BAD_REQUEST,
                    'msg' : '取消收藏失败'
                })
        else:
            return Response({
                "code" : status.HTTP_401_UNAUTHORIZED,
                'msg' : '请先登录'
            })

class CollectArticleListView(APIView):
    def get(self,request):
        '''
            获取文章收藏列表
        '''
        data = verify_token(request.META.get('HTTP_AUTHORIZATION'))
        if data:
            user = User.objects.get(phone = data.get('phone'))
            articles = CollectArticle.objects.filter(user = user).all()
        
            serializer = CollectArticleListSerializer(articles,many = True)

            return Response({
                'code' : status.HTTP_200_OK,
                'msg' : '获取文章收藏列表成功',
                'data' : serializer.data
            })
        else :
            return Response({
                'code' : status.HTTP_401_UNAUTHORIZED,
                'msg' : '请先登录'
            })
        
