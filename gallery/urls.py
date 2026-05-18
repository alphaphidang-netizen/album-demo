from django.urls import path
from . import views

urlpatterns = [
    path('', views.AlbumListView.as_view(), name='album-list'),
    path('album/new/', views.AlbumCreateView.as_view(), name='album-create'),
    path('album/<int:pk>/', views.AlbumDetailView.as_view(), name='album-detail'),
    path('album/<int:pk>/edit/', views.AlbumUpdateView.as_view(), name='album-update'),
    path('album/<int:pk>/delete/', views.AlbumDeleteView.as_view(), name='album-delete'),
    
    path('album/<int:album_id>/photo/add/', views.PhotoCreateView.as_view(), name='photo-create'),
    path('photo/<int:pk>/delete/', views.PhotoDeleteView.as_view(), name='photo-delete'),
]