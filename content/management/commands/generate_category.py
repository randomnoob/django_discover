from django.core.management.base import BaseCommand, CommandError
from content.models import PostCategory
from PyEditorial.settings import BLOG_CATEGORIES
from django.utils.text import slugify


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    # def add_arguments(self, parser):
        # parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        for cate_name in BLOG_CATEGORIES:
            category = PostCategory.objects.create(title=cate_name, slug=slugify(cate_name))
            category.save()

            self.stdout.write(
                self.style.SUCCESS('Successfully added PostCategory "%s"' % cate_name)
            )