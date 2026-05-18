from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Album, Photo
from .forms import AlbumForm, PhotoForm

# --- ALBUM VIEWS ---

class AlbumListView(LoginRequiredMixin, ListView):
    model = Album
    template_name = 'albums/album_list.html'
    context_object_name = 'albums'

    def get_queryset(self):
        # RBAC: Users only see their own albums
        return Album.objects.filter(owner=self.request.user).order_by('-created_at')

class AlbumDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Album
    template_name = 'albums/album_detail.html'

    def test_func(self):
        # RBAC: Only the owner can view details
        return self.get_object().owner == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photo_form'] = PhotoForm()
        return context

class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm
    template_name = 'albums/album_form.html'
    success_url = reverse_lazy('album-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class AlbumUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'albums/album_form.html'
    
    def test_func(self):
        return self.get_object().owner == self.request.user

    def get_success_url(self):
        return reverse_lazy('album-detail', kwargs={'pk': self.object.pk})

class AlbumDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Album
    template_name = 'albums/album_confirm_delete.html'
    success_url = reverse_lazy('album-list')

    def test_func(self):
        return self.get_object().owner == self.request.user

# --- PHOTO VIEWS ---

class PhotoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Photo
    form_class = PhotoForm

    def test_func(self):
        # Ensure user adding photo actually owns the target album
        album = get_object_or_404(Album, pk=self.kwargs['album_id'])
        return album.owner == self.request.user

    def form_valid(self, form):
        form.instance.album = get_object_or_404(Album, pk=self.kwargs['album_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('album-detail', kwargs={'pk': self.kwargs['album_id']})

class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Photo
    
    def test_func(self):
        return self.get_object().album.owner == self.request.user

    def get_success_url(self):
        return reverse_lazy('album-detail', kwargs={'pk': self.object.album.pk})