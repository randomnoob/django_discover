from django.conf import settings
from django.core.cache import caches

from django_extensions.management.jobs import DailyJob


from django.utils.text import slugify
from django.db.utils import IntegrityError
from content.models import Post, PostCategory
from content.utils import remove_all_links
from amp_tools import TransformHtmlToAmp
from bs4 import BeautifulSoup
import requests

BAOMOI = {
    'Ngắm': "https://baomoi.com/kham-pha-viet-nam-top335.epi",
    'Chuyện gia đình': "https://baomoi.com/nang-luong-tich-cuc-top338.epi",
    'Ngắm': "https://baomoi.com/kham-pha-the-gioi-top363.epi",
    'Ngắm': "https://baomoi.com/khong-gian-kien-truc.epi",
    'Chuyện yêu': "https://baomoi.com/tinh-yeu-hon-nhan.epi",
    'Vào bếp': "https://baomoi.com/am-thuc.epi",
}

class Job(DailyJob):
    help = "Scrape from baomoi.com"

    def parse_post(self, url, category_name, *args, **kwargs):
        print(f"   Scraping {url}")
        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/111.0.0.0 Safari/537.36'})
        soup = BeautifulSoup(page.text, "lxml")
        title = soup.find('h1').text
        slug = slugify(title, allow_unicode=False)
        try:
            thumbnail = soup.find("meta", attrs={"property":"og:image"}).get("content")
            if "base64" in thumbnail:
                thumbnail = ""
        except:
            thumbnail = ""

        mainelement = soup.find('h1').parent
        excerpt = mainelement.find('h3')
        try:
            content_detector = soup.find(lambda tag:tag.name=="div" and tag.get('class') and "body-image" in tag.get('class'))
            content = content_detector.parent
        except:
            print(f"      ++Error URL: {url}")
            return False
        
        content = remove_all_links(content) #output stringified soup
        try:
            amp_content = TransformHtmlToAmp(content)().decode()
        except:
            amp_content = content
        category = PostCategory.objects.get(title=category_name)
        try:
            post = Post.objects.create(title=title, slug=slug, thumbnail=thumbnail,
                                       content=content, amp_content=amp_content,
                                       excerpt=excerpt, category=category)
            post.save()
            print(f"      Done Scraping {url}")
        except IntegrityError:
            print(f"      ++Duplicated URL")
            pass

        return True

    def parse_pagination(self, url):
        index_page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/111.0.0.0 Safari/537.36'})
        index_soup = BeautifulSoup(index_page.text, "lxml")
        subpage_urls = index_soup.find_all("a", attrs={'title': True})
        subpage_urls = [x['href'] for x in subpage_urls if x['title']]
        subpage_urls = list(set(subpage_urls))
        return subpage_urls

    def execute(self):
        for cate_name, cate_url in BAOMOI.items():
            print(f"====Scraping Category {cate_name}===={cate_url}")
            post_urls = self.parse_pagination(cate_url)
            print(f"    Post URLs list contains {len(post_urls)} URLs")
            for url in post_urls:
                    url = "https://baomoi.com"+url
                    self.parse_post(url, category_name=cate_name)
        return