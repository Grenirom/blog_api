import action as action
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import generics, permissions
from account import serializers
from dj_rest_auth.views import LogoutView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.decorators import action

from account.serializers import UserListSerializer, UserDetailSerializer
from like.serializers import FavoriteSerializer


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.RegisterSerializer


class CustomLogoutView(LogoutView):
    permission_classes = (permissions.IsAuthenticated,)


class UserViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        return UserDetailSerializer

    @action(['GET'], detail=True)
    def favorites(self, request, pk):
        user = self.get_object()
        fav_posts = user.favorites.all()
        serializer = FavoriteSerializer(fav_posts, many=True)
        return Response(serializer.data, status=200)


# class UserListView(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserListSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#
#
# class UserDetailView(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserDetailSerializer
#     permission_classes = (permissions.IsAuthenticated,)
