from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from blog_app.models import Article,Category,Tag
from user_app.models import User
from user_app.token import verify_token
from user_app.utils import login_url
from .serializers import ArticleAllListSerializer,ArticleListSerializer,ArticleDetailSerializer


# Create your views here.
class ArticleCreateView(APIView):
    '''
        发布个人文章
    '''
    def post(self,request):
        data = verify_token(request.META.get('HTTP_AUTHORIZATION'))
        if data:
            user = User.objects.get(phone=data.get('phone'))
            category = Category.objects.get(category=request.data.get('category'))
            
            article = Article.objects.create(
                title = request.data.get('title'),
                content = request.data.get('content'),
                status = request.data.get('status'),
                type = request.data.get('type'),
                is_featured = request.data.get('is_featured'),
                user=user,
                category = category,
                )
            
            # 处理多对多的tags
            tag_ids = request.data.get('tags',[])
            if tag_ids:
                tags = Tag.objects.filter(id__in=tag_ids)
                article.tags.set(tags) # 设置赋值给多对多字段
            
            return Response({
                'code' : status.HTTP_201_CREATED,
                'message' : '文章发布成功',
            })
        
        else:
            return Response({
                'code' : status.HTTP_401_UNAUTHORIZED ,
                'msg':'请先登录', 
                'redirect' : login_url(request)
                })


class ArticleDeleteView(APIView):
    '''
        删除个人文章
        权限：仅评论所有者或管理员可删除 （未实现）
    '''
    def delete(self,request,pk):
        data = verify_token(request.META.get('HTTP_AUTHORIZATION'))
        if data:
            try:
                article = Article.objects.get(pk=pk)
            except Article.DoesNotExist:
                return Response({
                    'code' : status.HTTP_404_NOT_FOUND,
                    'msg' : '文章不存在'
                })
            
            if article.delete():
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
                'code' : status.HTTP_401_UNAUTHORIZED,
                'msg' : '请先登录！',
                'redirect' : login_url(request) 
            })

class ArticleListView(APIView):
    '''
        搜索、获取个人文章列表 （搜索功能未实现）
    '''
    def get(self,request):
        data = verify_token(request.META.get('HTTP_AUTHORIZATION'))
        if data:
            user = User.objects.get(phone = data.get('phone'))
            articles = Article.objects.filter(user = user).order_by('-created_at')
        
            serializer = ArticleListSerializer(articles,many = True)

            return Response({
                'code' : status.HTTP_200_OK,
                'msg' : '获取个人文章列表成功',
                'data' : serializer.data,
            })
            
        else:
            return Response({
                'code' : status.HTTP_401_UNAUTHORIZED,
                'msg' : '请先登录',
                'redirect' : login_url(request)
            })

class ArticleDetailView(APIView):
    '''
        获取个人文章详情
    '''
    def get(self,request, pk):
        data = verify_token(request.META.get('HTTP_AUTHORIZATION'))
        if data:
            try:
                article = Article.objects.get(pk = pk)
                serializer = ArticleDetailSerializer(article)
            except Article.DoesNotExist:
                return Response({
                    'code' : status.HTTP_404_NOT_FOUND,
                    'msg' : '文章不存在'
                })
            
            return Response({
                'code' : status.HTTP_200_OK,
                'msg' : '获取文章成功',
                'data' : serializer.data
            })

        else:
            return Response({
                'code' : status.HTTP_401_UNAUTHORIZED,
                'msg' : '请先登录'
            })

class ArticleUpdateView(APIView):
    '''
        更新文章0 (留着)
    '''
    pass

class ArticleAllListPagination(PageNumberPagination):
    '''
        所有文章评论列表分页器
    '''
    page_size = 10
    max_page_size = 20 # 前端控制每页显示数据最多不能超过20
    page_query_param = 'page'
    page_size_query_param = 'page_size'


class ArticleAllListView(ListAPIView):
    '''
        获取所有文章列表
    '''
    pagination_class = ArticleAllListPagination
    serializer_class = ArticleAllListSerializer
    queryset = Article.objects.all()

