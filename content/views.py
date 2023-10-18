from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView, MultipleObjectMixin
from django.db.models import Q

from . import models
from .models import Post, PostCategory
from django.contrib.auth.models import User
from .forms import SearchForm


class Index(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        context = {
            'last_blog': models.Post.objects.order_by('-pk').filter(status=0)[:1],
            'blogs': models.Post.objects.order_by('-pk').filter(status=0)[1:15],
        }
        return render(request, self.template_name, context)

class PostSingle(DetailView):
    model = models.Post
    template_name = 'content/post.html'

    def get_queryset(self):
        return self.model.objects.filter(slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['reverse_url'] = reverse('blog_single', kwargs={'slug': self.kwargs['slug']})
        return context

class PostSingleAMP(PostSingle):
    template_name = 'content/amp-post.html'


class CategoryDetail(DetailView):
    template_name= 'category_detail.html'

    def get_queryset(self):
        return self.model.objects.filter(slug=self.kwargs['slug'])

class CategoryDetailView(DetailView, MultipleObjectMixin):
    model=PostCategory
    paginate_by = 10
    template_name= 'content/category_detail.html'

    def get_context_data(self, **kwargs):
        object_list = self.object.blog_posts.all().order_by('-pk')
        context = super(CategoryDetailView, self).get_context_data(object_list=object_list, **kwargs)
        context['paginate'] = True
        return context

class UserDetailView(DetailView, MultipleObjectMixin):
    model=User
    paginate_by = 10
    template_name= 'content/user_detail.html'

    def get_context_data(self, **kwargs):
        object_list = self.object.blog_posts.all().order_by('-pk')
        context = super(UserDetailView, self).get_context_data(object_list=object_list, **kwargs)
        context['paginate'] = True
        return context