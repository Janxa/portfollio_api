from django.urls import path
from projects import views

urlpatterns = [
    path('', views.project_list),
    path('<int:pk>/', views.project_detail),
]