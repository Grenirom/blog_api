from django.urls import path
from category import views
from category.views import CategoryDetailView

urlpatterns = [
    path('', views.CategoryCreateListView.as_view()),
    path('<int:pk>/', CategoryDetailView.as_view()),

]