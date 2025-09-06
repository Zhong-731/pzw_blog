from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from user_app.models import User
from user_app.token import verify_token
from blog_app.models import Article
from question_app.models import ArticleComment
from .models import LikeArticle,LikeComment
from .serializers import LikeArticleListSerializer

# Create your views here.
'''
    文章点赞模型功能
'''

class LikeArticleAddView(APIView):
    def post(self,request,article_id):
        '''
            点赞文章
        '''
        data = verify_token(request.META.get('HTTP_AUTHORIZATION'))
        if data:
            user = User.objects.get(phone=data.get('phone'))
            article = Article.objects.get(id=article_id)
            LikeArticle.objects.create(article=article, user=user)
            return Response({
                'status':status.HTTP_200_OK,
                'message':'点赞成功'
            })
        else:
            return Response({
                'status':status.HTTP_401_UNAUTHORIZED,
                'message':'请先登录'
            })
        

class LikeArticleDeleteView(APIView):
    def delete(self,request,article_id):
        '''
            取消点赞文章
        '''
        data = verify_token(request.META.get('HTTP_AUTHORIZATION'))
        if data:
            user = User.objects.get(phone = data.get('phone'))
            article = Article.objects.get(id = article_id)
            if LikeArticle.objects.get(user=user, article=article).delete():
                return Response({
                    'status':status.HTTP_200_OK,
                    'msg':'删除成功'
                })
            else:
                return Response({
                    'status':status.HTTP_400_BAD_REQUEST,
                    'msg':'删除失败'
                })
        else:
            return Response({
                'status':status.HTTP_401_UNAUTHORIZED,
                'msg':'请先登录'
            })

class LikeArticleListView(APIView):
    def get(self, request):
        '''
            获取点赞文章列表
        '''
        data = verify_token(request.META.get('HTTP_AUTHORIZATION'))
        if data:
            user = User.objects.get(phone = data.get('phone'))
            like_articles = LikeArticle.objects.filter(user = user).all()
            serializer = LikeArticleListSerializer(like_articles,many = True)

            return Response({
                'status':status.HTTP_200_OK,
                'msg':'获取成功',
                'data':serializer.data
            })
        else:
            return Response({
                'code' : status.HTTP_401_UNAUTHORIZED,
                'msg' : '请先登录'
            })
        

'''
    评论点赞模型功能
'''

class LikeCommentAddView(APIView):
    def post(self,request,comment_id):
        '''
            点赞评论
        '''
        data = verify_token(request.META.get('HTTP_AUTHORIZATION'))
        if data:
            user = User.objects.get(phone=data.get('phone'))
            comment = ArticleComment.objects.get(id = comment_id)
            LikeComment.objects.create(comment = comment,user = user)
            return Response({
                'status':status.HTTP_200_OK,
                'message':'点赞成功'
            })
        else:
            return Response({
                'status':status.HTTP_401_UNAUTHORIZED,
                'message':'请先登录'
            })
        

class LikeCommentDeteleteView(APIView):
    def delete(self,request,comment_id):
        '''
            取消点赞评论
        '''
        data = verify_token(request.META.get('HTTP_AUTHORIZATION'))
        if data:
            user = User.objects.get(phone = data.get('phone'))
            comment = ArticleComment.objects.get(id = comment_id)
            LikeComment.objects.filter(comment = comment,user = user).delete()
            return Response(data = {
                'code':200,
                'message':'取消点赞成功'
            })
        else:
            return Response({
                'status':status.HTTP_401_UNAUTHORIZED,
                'message':'请先登录'
            })
        
