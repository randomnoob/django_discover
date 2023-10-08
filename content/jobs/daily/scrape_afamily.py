from django.conf import settings
from django.core.cache import caches

from django_extensions.management.jobs import DailyJob

from content.models import Post, PostCategory


class Job(DailyJob):
    help = "Scrape from afamily.vn category Nau An https://afamily.vn/an-ngon.chn"

    def execute(self):

        return