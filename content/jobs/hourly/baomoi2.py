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
import json

BAOMOI = {
    'Ngắm': "https://baomoi.com/kham-pha-viet-nam-top335.epi",
    'Chuyện gia đình': "https://baomoi.com/nang-luong-tich-cuc-top338.epi",
    'Ngắm': "https://baomoi.com/kham-pha-the-gioi-top363.epi",
    'Ngắm': "https://baomoi.com/khong-gian-kien-truc.epi",
    'Ngắm': "https://baomoi.com/nha-thanh-t35935608.epi",
    'Chuyện yêu': "https://baomoi.com/tinh-yeu-hon-nhan.epi",
    'Vào bếp': "https://baomoi.com/am-thuc.epi",
    'Vào bếp': "https://baomoi.com/van-hoa.epi",
}

class Job(HourlyJob):
    help = "Scrape from baomoi.com"

    @staticmethod
    def join_bodys(data):
        bodys = data['props']['pageProps']['resp']['data']['content']['bodys']
        content = ""
        for elem in bodys:
            if elem['type']=='text':
                content += f"<p>{elem['content']}</p>"
            elif elem['type']=='image':
                content += f"""<img src="{elem['originUrl']}" alt="" class="inner_image">"""
            elif elem['type']=='video':
                player = f"""
    <!-- Import Mediaelement CSS -->
    <link href="https://cdn.jsdelivr.net/npm/mediaelement@latest/build/mediaelementplayer.min.css" rel="stylesheet">
    <!-- Import Mediaelement JS -->
    <script src="https://cdn.jsdelivr.net/npm/mediaelement@latest/build/mediaelement-and-player.min.js"></script>

    <div class="player">
        <video id="player-demo" width="{elem['width']}" height="{elem['height']}" preload="none" style="max-width: 100%" controls="" poster="{elem['poster']}">
            <source src="{elem['originUrl']}" type="video/mp4">
        </video>
    </div>


    """
                content += player


        return content
    
    def parse_metadata(self, data):
        content = data['props']['pageProps']['resp']['data']['content']
        bodys = content['bodys']

        parsed = {}
        parsed['title'] = content['title']
        parsed['slug'] = slugify(content['title'])
        if content.get('thumbL'):
            thumbnail = content['thumbL']
        elif content.get('thumb'):
            thumbnail = content['thumb']
        else:
            thumbnail = ""
        parsed['thumbnail'] = thumbnail

        raw_text = ".".join([x['content'] for x in bodys if x['type']=='text'])
        parsed['excerpt'] = raw_text[:100] + "..."

        html = self.join_bodys(data)
        try:
            amp_content = TransformHtmlToAmp(html)().decode()
        except:
            amp_content = html
        parsed['amp_content'] = amp_content
        parsed['content'] = html

        parsed['excerpt'] = raw_text
        return parsed
    

    def parse_post(self, url, category_name, *args, **kwargs):
        print(f"   Scraping {url}")
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "lxml")
        internal_data_script = soup.find("script", id="__NEXT_DATA__").text
        data = json.loads(internal_data_script)
        parsed = self.parse_metadata(data)

        category = PostCategory.objects.get(title=category_name)
        try:
            the_post = Post.objects.create(category=category, **parsed)
            the_post.save()
            print(f"      Done Scraping {url}")
            print(f"      Post title {parsed['title']}")
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
        # self.parse_post("https://baomoi.com/can-tho-trao-giai-bao-chi-bua-liem-vang-lan-thu-ii-cho-50-tac-pham-c47387551.epi", category_name="Ngắm")
        # return