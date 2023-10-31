from django.contrib.sitemaps import Sitemap
from content.models import Post
from django.urls import reverse
 
 
class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.created_on


class StaticSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return ["content:about", "content:contact", "content:privacy",
                "content:terms", "content:chuyen-doi-muc-dich-su-dung",
                "content:noi-quy"]

    def location(self, item):
        return reverse(item)