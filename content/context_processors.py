from . import models
from constance import config

latest_posts = models.Post.objects.order_by('-pk').filter(status=0)[1:15]

def show_system_content(request):
    return {
        'blog_categories': models.PostCategory.objects.all(),
        'popular_posts': latest_posts[:5],
        'most_viewed': latest_posts[6:15],
        'config': config,
    }
