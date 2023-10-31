from django.conf import settings
from django.core.cache import caches

from django_extensions.management.jobs import HourlyJob


from django.utils.text import slugify
from django.db.utils import IntegrityError
from content.models import Post, PostCategory
from content.utils import remove_all_links
from amp_tools import TransformHtmlToAmp
from bs4 import BeautifulSoup
import requests

from PyEditorial.settings import SCRAPE_LIST


class Job(HourlyJob):
    help = "Scrape from afamily.vn category Nau An https://afamily.vn/an-ngon.chn"

    def baomoi_soupcleaner(self, soup):
        h1_title = soup.find('h1')
        title = h1_title.text
        main_container = h1_title.parent
        #Delete the source link
        _source_link = main_container.find(lambda tag:tag.name=="a" and "Gốc" in str(tag))
        _source_container = _source_link.parent
        _source_container.decompose()
        # Delete default players
        _default_players = main_container.find_all(lambda tag:tag.name=="div" and "player-default" in str(tag))
        for p in _default_players:
            p.decompose()

        return

    def parse_post(self, url, category_name, *args, **kwargs):
        print(f"   Scraping {url}")
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "lxml")
        title = soup.find('h1').text
        slug = slugify(title, allow_unicode=False)
        try:
            thumbnail = soup.find("meta", attrs={"property":"og:image"}).get("content")
            if "base64" in thumbnail:
                thumbnail = ""
        except:
            thumbnail = ""
        content = soup.find(id='af-detail-content')
        content = remove_all_links(content) #output stringified soup
        try:
            amp_content = TransformHtmlToAmp(content)().decode()
        except:
            amp_content = content
        category = PostCategory.objects.get(title=category_name)
        try:
            post = Post.objects.create(title=title, slug=slug, thumbnail=thumbnail,
                                       content=content, amp_content=amp_content,
                                       category=category)
            post.save()
            print(f"      Done Scraping {url}")
        except IntegrityError:
            print(f"      ++Duplicated URL")
            pass

        return True

    def parse_pagination(self, url):
        index_page = requests.get(url)
        index_soup = BeautifulSoup(index_page.text, "lxml")
        # subpage_blocks = index_soup.find_all("a", attrs={"class":"thumb"})
        # subpage_urls = [x.get('href') for x in subpage_blocks if x.get('href')]
        subpage_blocks = index_soup.find_all("h2")
        subpage_blocks = subpage_blocks + index_soup.find_all("h3")
        subpage_urls = [x.find("a").get("href") for x in subpage_blocks \
                                if x.find("a").get("href")]
        subpage_urls = list(set(subpage_urls))
        return subpage_urls

    def execute(self):
        page_limit = 5
        for cate_name, cate_url in SCRAPE_LIST.items():
            print(f"====Scraping Category {cate_name}====")
            pagination = [cate_url.format(pagenum=x) for x in range(page_limit)]
            post_urls = []
            print(pagination)
            for x in pagination:
                urls = self.parse_pagination(x)
                post_urls.extend(urls)
            print(f"    Post URLs list contains {len(post_urls)} URLs")
            for url in post_urls:
                    url = "https://afamily.vn"+url
                    self.parse_post(url, category_name=cate_name)
        return