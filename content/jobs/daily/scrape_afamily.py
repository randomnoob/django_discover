from django.conf import settings
from django.core.cache import caches

from django_extensions.management.jobs import DailyJob


from django.utils.text import slugify
from django.db.utils import IntegrityError
from content.models import Post, PostCategory
from bs4 import BeautifulSoup
import requests

from PyEditorial import BLOG_CATEGORIES

class Job(DailyJob):
    help = "Scrape from afamily.vn category Nau An https://afamily.vn/an-ngon.chn"

    def parse_post(self, url, *args, **kwargs):
        print(f"Scraping {url}")
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "lxml")
        title = soup.find('h1').text
        slug = slugify(title, allow_unicode=False)
        try:
            thumbnail = soup.find("meta", attrs={"property":"og:image"}).get("content")
        except:
            thumbnail = "https://picsum.photos/500"
        content = str(soup.find(id='af-detail-content'))
        category = PostCategory.objects.first()
        try:
            post = Post.objects.create(title=title, slug=slug, thumbnail=thumbnail, content=content, category=category)
            post.save()
            print(f"Done Scraping {url}")
        except IntegrityError:
            print(f"Duplicated URL")
            pass

        return True

    def parse_pagination(self, url):
        index_page = requests.get(url)
        index_soup = BeautifulSoup(index_page.text, "lxml")
        subpage_blocks = index_soup.find_all("li", class_="afctru-li") + \
                            index_soup.find_all("li", class_="afwblu-li")
        subpage_urls = [x.find('a').get('href') for x in subpage_blocks if x.find('a').get('href')]
        subpage_urls = list(set(subpage_urls))
        return subpage_urls

    def execute(self):
        pagination = [f"https://afamily.vn/timeline/134/trang-{x}.chn" for x in range(1,4)]
        subpage_urls = []
        for x in pagination:
            urls = self.parse_pagination(x)
            subpage_urls.extend(urls)

        for url in subpage_urls:
                url = "https://afamily.vn"+url
                self.parse_post(url)
        return