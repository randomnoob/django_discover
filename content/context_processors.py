from . import models
from constance import config

latest_posts = models.Post.objects.order_by('-pk').filter(status=0)[1:20]

def show_system_content(request):
    return {
        'blog_categories': models.PostCategory.objects.all(),
        'featured_posts': latest_posts[:5],
        'popular_posts': latest_posts[5:10],
        'most_viewed': latest_posts[10:20],
        'config': config,
    }
