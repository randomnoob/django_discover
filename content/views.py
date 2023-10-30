from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView, MultipleObjectMixin
from django.db.models import Q

from content.models import Post, PostCategory, get_default_user
from content.utils import textify
from constance import config
from django.contrib.auth.models import User

from django.contrib.syndication.views import Feed


class Index(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        context = {
            'last_blog': Post.objects.order_by('-pk').filter(status=0)[:1],
            'blogs': Post.objects.order_by('-pk').filter(status=0)[1:15],
        }
        return render(request, self.template_name, context)

class PostSingle(DetailView):
    model = Post
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
    

# =========Begin RSS Feed Views=========

class PostsByCategory(Feed):
    author_name = get_default_user().username

    def get_object(self, request, category_slug):
        return PostCategory.objects.get(slug=category_slug)

    def title(self, obj):
        return "Bài viết mới nhất trong chuyên mục: %s" % obj.title

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return obj.title

    def items(self, obj):
        return Post.objects.filter(category=obj).order_by("-pk")[:100]
    
    def item_title(self, item):
        # Tra ve title cho tung post
        return item.title
    def item_description(self, item):
        # Tra ve desc cho tung post
        if len(item.excerpt) >= 50:
            return item.excerpt
        else:
            return textify(item.content)[:100]
    def item_pubdate(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        pubdate.
        """
        return item.created_on

class AllPostFeed(Feed):
    title = f"Bài viết mới nhất trên {config.SITE_TITLE}"
    author_name = get_default_user().username
    link = "/feed/"

    def description(self, obj):
        return f"Mới nhất trên {config.SITE_TITLE}"

    def items(self):
        return Post.objects.order_by("-created_on")[:50]
    def item_title(self, item):
        # Tra ve title cho tung post
        return item.title
    def item_description(self, item):
        # Tra ve desc cho tung post
        if len(item.excerpt) >= 50:
            return item.excerpt
        else:
            return textify(item.content)[:100]
    def item_pubdate(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        pubdate.
        """
        return item.created_on
# =========End RSS Feed Views=========
