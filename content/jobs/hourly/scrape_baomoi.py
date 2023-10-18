from django.conf import settings
from django.core.cache import caches

from django_extensions.management.jobs import HourlyJob

from django.db.utils import IntegrityError
from content.models import Post, PostCategory
from django.urls import reverse
from content.utils import remove_all_links, slugify
from amp_tools import TransformHtmlToAmp
from bs4 import BeautifulSoup
import requests
import traceback

BAOMOI = {
    'Ngắm': "https://baomoi.com/kham-pha-viet-nam-top335.epi",
    'Chuyện gia đình': "https://baomoi.com/nang-luong-tich-cuc-top338.epi",
    'Ngắm': "https://baomoi.com/kham-pha-the-gioi-top363.epi",
    'Ngắm': "https://baomoi.com/khong-gian-kien-truc.epi",
    'Chuyện yêu': "https://baomoi.com/tinh-yeu-hon-nhan.epi",
    'Vào bếp': "https://baomoi.com/am-thuc.epi",
}

class Job(HourlyJob):
    help = "Scrape from baomoi.com"

    def parse_post(self, url, category_name, *args, **kwargs):
        print(f"   Scraping {url}")
        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/111.0.0.0 Safari/537.36'})
        soup = BeautifulSoup(page.text, "lxml")
        title = soup.find('h1').text
        slug = slugify(title)
        try:
            thumbnail = soup.find("meta", attrs={"property":"og:image"}).get("content")
            if "base64" in thumbnail:
                thumbnail = ""
        except:
            thumbnail = ""

        mainelement = soup.find('h1').parent
        excerpt = soup.find("meta", attrs={"name": "description"})
        excerpt = excerpt['content']
        excerpt_h3 = mainelement.find("h3")
        remaining_content = excerpt_h3.next_sibling
        try:
            new_tag = soup.new_tag("div", class_="combined-content")
            new_tag.append(excerpt_h3)
            new_tag.append(remaining_content)
        except:
            print(f"      ++Error URL: {url}")
            traceback.print_exc()
        
        content = remove_all_links(new_tag) #output stringified soup
        try:
            amp_content = TransformHtmlToAmp(content)().decode()
        except:
            amp_content = content
        category = PostCategory.objects.get(title=category_name)
        try:
            the_post = Post.objects.create(title=title, slug=slug, thumbnail=thumbnail,
                                        content=content, amp_content=amp_content,
                                        excerpt=excerpt, category=category)
            the_post.save()
            print(f"      Done Scraping {url}")
            print(f"      Post title {title}")
        except IntegrityError:
            print(f"      ++Duplicated URL")
            pass

        return True

    def parse_pagination(self, url):
        index_page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/111.0.0.0 Safari/537.36'})
        index_soup = BeautifulSoup(index_page.text, "lxml")
        # subpage_urls = index_soup.find_all("a", attrs={'title': True})
        subpage_urls = index_soup.find_all("h3")
        subpage_urls = [x.find("a")['href'] for x in subpage_urls]
        subpage_urls = list(set(subpage_urls))
        return subpage_urls

    def execute(self):
        for cate_name, cate_url in BAOMOI.items():
            print(f"====Scraping Category {cate_name}===={cate_url}")
            post_urls = self.parse_pagination(cate_url)
            print(f"    Post URLs list contains {len(post_urls)} URLs")
            for url in post_urls:
                    url = "https://baomoi.com"+url
                    try:
                        self.parse_post(url, category_name=cate_name)
                    except:
                        pass
        # self.parse_post("https://baomoi.com/quang-binh-kho-quyet-toan-du-an-phat-trien-moi-truong-ha-tang-do-thi-c47246598.epi", category_name="Ngắm")
        return