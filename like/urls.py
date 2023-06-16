from django.urls import path

from like.views import LikeCreateView, LikeDeleteView

urlpatterns = [
    path('', LikeCreateView.as_view()),
    path('<int:pk>/', LikeDeleteView.as_view()),
]