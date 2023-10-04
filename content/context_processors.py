from . import models
from constance import config


def show_system_content(request):
    return {
        'blog_categories': models.BlogCategory.objects.all(),
        'config': config,
    }
