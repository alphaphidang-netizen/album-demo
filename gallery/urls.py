from django.urls import path
from . import views

urlpatterns = [
    path('', views.AlbumListView.as_view(), name='album-list'),
    path('new/', views.AlbumCreateView.as_view(), name='album-create'),
    path('<int:pk>/edit/', views.AlbumUpdateView.as_view(), name='album-update'),
    path('<int:pk>/delete/', views.AlbumDeleteView.as_view(), name='album-delete'),
]