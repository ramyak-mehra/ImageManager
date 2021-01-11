from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from .models import ImageHandler

class ImageListView(ListView):
    model = ImageHandler
    template_name = 'imagehandler/home.html'
    ordering = ['-created_at']
    paginate_by = 5

    def get_queryset(self):
        images = ImageHandler.objects.all()
        return images

class ImageHandlerCreateView(LoginRequiredMixin , CreateView):
    model = ImageHandler
    fields = ['title' , 'description' , 'original_image' , 'tags']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ImageHandlerUpdateView(LoginRequiredMixin , UserPassesTestMixin , UpdateView):
    model = ImageHandler
    fields = ['title' , 'description' , 'original_image' , 'tags']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == image.user:
            return True
        return False

class ImageHandlerDeleteView(LoginRequiredMixin , UserPassesTestMixin , DeleteView):
    model = ImageHandler
    success_url = '/'
    def test_func(self):
        image = self.get_object()
        if self.request.user == image.user:
            return True
        return False
