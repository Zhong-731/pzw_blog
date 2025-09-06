import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination

from blog_app.models import Article
from user_app.models import User
from user_app.token import verify_token 
from question_app.models import ArticleComment,Question
from .serializers import *

# Create your views here.
logger = logging.getLogger(__name__)


class ArticleCommentAddView(APIView):
    def post(self,request):
        '''
            个人文章评论增加
        '''
        data = verify_token(request.META.get("HTTP_AUTHORIZATION"))
        if data:
            user = User.objects.get(phone = data.get('phone'))
            article = Article.objects.get(id = request.data.get('article'))
            ArticleComment.objects.create(
                comment=request.data.get("comment"),
                user=user,
                article = article,
            )
            return Response({
                'code' : status.HTTP_201_CREATED,
                'msg' : '评论发布成功'
            })
        else:
            return Response({
                'code' : status.HTTP_401_UNAUTHORIZED,
                'msg' : '请先登录',
            })


class ArticleCommentDeleteView(APIView):
    def delete(self,request,id):
        '''
            个人文章评论删除
            权限：仅评论所有者或管理员可删除
        '''
        data = verify_token(request.META.get("HTTP_AUTHORIZATION"))
        if data:
            user = User.objects.get(phone=data.get('phone'))
            article_comment = ArticleComment.objects.get(id = id)
            # 权限验证
            if article_comment.user.id == user.id or user.id == 1: # 1 是超级管理员
                try:
                    article_comment.delete()
                except Exception as e:
                    return Response({
                        'code ':  status.HTTP_500_INTERNAL_SERVER_ERROR,
                        'msg' : '删除失败'
                    })
                return Response({
                    'code' : status.HTTP_204_NO_CONTENT,
                    'msg' : '删除成功'
                })
            else:
                return Response({
                    'code' : status.HTTP_403_FORBIDDEN,
                    'msg' : "无法删除其他用户的评论"
                })
        else:
            return Response({
                'code' : status.HTTP_401_UNAUTHORIZED,
                'msg' : '请先登录',
            })
    
# class ArticleCommentListPagination(PageNumberPagination):
#     '''
#         个人文章评论列表分页器
#     '''
#     page_size = 10
#     max_page_size = 20 # 前端控制每页显示数据最多不能超过20

class ArticleCommentListView(ListAPIView):
    '''
        个人文章评论列表获取
        功能：
            分页
    '''
    serializer_class = ArticleCommentListSerializer
    queryset = ArticleComment.objects.filter(answer=None).all()


class ArticleCommentAnswerView(APIView):
    def post(self,request):
        '''
            个人文章评论回复
        '''
        data = verify_token(request.META.get("HTTP_AUTHORIZATION"))
        if data:
            user = User.objects.get(phone=data.get('phone'))
            article = Article.objects.get(id = request.data.get('article'))
            answer = ArticleComment.objects.get(id = request.data.get('answer'))
            ArticleComment.objects.create(
                comment=request.data.get("comment"),
                user=user,
                article = article,
                answer = answer
            )
            return Response({
                'code' : status.HTTP_201_CREATED,
                'msg' : '评论发布成功'
            })
        else:
            return Response({
                'code' : status.HTTP_401_UNAUTHORIZED,
                'msg' : '请先登录',
            })




class QuestionAddView(APIView):
    def post(self,request):
        '''
            个人意见反馈增加
        '''
        data = verify_token(request.META.get("hTTP_AUTHORIZATION"))
        if data:
            user = User.objects.get(phone=data.get('phone'))
            serializer = QuestionDetailSerializer(data=request.data,user=user)
            if serializer.is_valid():
                pass


