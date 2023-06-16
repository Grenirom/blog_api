from rest_framework import generics, permissions
from rest_framework.decorators import action
from comment.serializers import CommentSerializer
from like.models import Favorite
from like.serializers import LikeSerializer, LikeUserSerializer
from .models import Posts
from . import serializers
from .permissions import IsAuthor, IsAuthorOrAdmin
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class StandartResultPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'


class PostViewSet(ModelViewSet):
    queryset = Posts.objects.all()
    pagination_class = StandartResultPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('title', 'body')
    filterset_fields = ('owner', 'category')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PostListSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return serializers.PostCreateSerializer
        return serializers.PostDetailSerializer

    def get_permissions(self):
        # удалять может только автор поста или админы
        if self.action == 'destroy':
            return [IsAuthorOrAdmin(), ]
        # обновлять может только автор поста
        elif self.action in ('update', 'partial_update'):
            return [IsAuthor(), ]
        # просматривать могут все, но создавать может только аутентифицированный пользователь
        return [permissions.IsAuthenticatedOrReadOnly(), ]

    @action(['GET'], detail=True)
    def comments(self, request, pk):
        post = self.get_object()
        # print(post, '11111111111111')
        comments = post.comments.all()
        serializer = CommentSerializer(instance=comments, many=True)
        return Response(serializer.data, status=200)

    @action(['GET'], detail=True)
    def likes(self, request, pk):
        post = self.get_object()
        likes = post.likes.all()
        serializer = LikeUserSerializer(instance=likes, many=True)
        return Response(serializer.data, status=200)

    @action(['POST', 'DELETE'], detail=True)
    def favorites(self, request, pk):
        post = self.get_object() # Posts.objects.get(id=pk)
        user = request.user
        favorite = user.favorites.filter(post=post)

        if request.method == 'POST':
            if favorite.exists():
                return Response({'msg': 'Already in favorite'}, status=400)
            Favorite.objects.create(owner=user, post=post)
            return Response({'msg': 'Added to favorites'}, status=201)

        if favorite.exists():
            favorite.delete()
            return Response({'msg': 'Deleted from favorite'}, status=204)
        return Response({'msg': 'Post Not Found in Favorite'}, status=404)

# class PostListCreateView(generics.ListCreateAPIView):
#         queryset = Posts.objects.all()
#         permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
#
#         def get_serializer_class(self):
#             if self.request.method == 'GET':
#                 return serializers.PostListSerializer
#             return serializers.PostCreateSerializer
#
#         def perform_create(self, serializer):
#             serializer.save(owner=self.request.user)
#
#
# class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Posts.objects.all()
#
#     def get_serializer_class(self):
#         if self.request.method in ('PUT', 'PATCH'):
#             return serializers.PostCreateSerializer
#         return serializers.PostDetailSerializer
#
#     def get_permissions(self):
#         if self.request.method in ('PUT', 'PATCH'):
#             return [IsAuthor()]
#         elif self.request.method == 'DELETE':
#             return [IsAuthorOrAdmin()]
#         return [permissions.AllowAny()]


