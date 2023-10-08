from . import models
from constance import config


def show_system_content(request):
    return {
        'blog_categories': models.PostCategory.objects.all(),
        'popular_posts': models.Post.objects.order_by('-pk').filter(status=0)[1:15],
        'config': config,
    }
