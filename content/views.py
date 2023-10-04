from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic, View
from django.db.models import Q

from . import models
from .forms import SearchForm


class Index(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        context = {
            'last_blog': models.Post.objects.order_by('-pk').filter(publish=True)[:1],
            'blogs': models.Post.objects.order_by('-pk').filter(publish=True)[1:5],
        }
        return render(request, self.template_name, context)


class Search(View):
    template_name = 'search.html'

    def get(self, request, *args, **kwargs):
        form = SearchForm(self.request.GET)
        if form.is_valid():
            print('valid')
            query = form.cleaned_data['query']
            context = {
                'blogs': models.Post.objects.order_by('-pk').filter(
                    Q(title__icontains=query) | Q(content__icontains=query)
                ),
            }
        else:
            return redirect('content:index')
        return render(request, self.template_name, context)


class PostCategoryCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = models.PostCategory
    fields = '__all__'
    success_message = 'Post category was created successfully'

    def get_success_url(self):
        return reverse('content:blog_category_create')


class Post(generic.ListView):
    model = models.Post
    template_name = 'blog_archive.html'


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = models.Post
    fields = '__all__'
    success_message = 'Post was created successfully'

    def get_success_url(self):
        return reverse('content:blog_create')


class PostArchiveByCategoryPK(generic.ListView):
    model = models.Post
    template_name = 'blog_archive.html'

    def get_queryset(self):
        return self.model.objects.filter(category=self.kwargs['pk'])


class PostSingle(generic.DetailView):
    model = models.Post
    template_name = 'single.html'

    def get_queryset(self):
        return self.model.objects.filter(slug=self.kwargs['slug'])

