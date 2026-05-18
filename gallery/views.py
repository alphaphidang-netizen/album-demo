from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Album
from .forms import AlbumForm

class AlbumListView(ListView):
    model = Album
    template_name = 'gallery/album_list.html'
    context_object_name = 'albums'

class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm
    template_name = 'gallery/album_form.html'
    success_url = reverse_lazy('album-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user # Auto-assign logged-in user
        return super().form_valid(form)

class AlbumUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'gallery/album_form.html'
    success_url = reverse_lazy('album-list')

    def test_func(self):
        album = self.get_object()
        # RBAC: Allow if user is the owner OR user is in 'Managers' group
        return self.request.user == album.owner or self.request.user.groups.filter(name='Managers').exists()

class AlbumDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Album
    template_name = 'gallery/album_confirm_delete.html'
    success_url = reverse_lazy('album-list')

    def test_func(self):
        album = self.get_object()
        return self.request.user == album.owner or self.request.user.groups.filter(name='Managers').exists()