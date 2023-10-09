from django.core.management.base import BaseCommand, CommandError
from content.models import PostCategory
from django.utils.text import slugify


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    # def add_arguments(self, parser):
        # parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        categories = [
            'Dạy con', #https://afamily.vn/giao-duc/day-con.chn
            'Chuyện gia đình', #https://afamily.vn/yeu/chuyen-gia-dinh.chn
            'Chuyện yêu', #https://afamily.vn/yeu/chuyen-yeu.chn
            'Hẹn hò', #https://afamily.vn/yeu/hen-ho.chn
            'Sống khỏe', #https://afamily.vn/suc-khoe/song-khoe.chn
            'Tư vấn tình dục', # https://afamily.vn/suc-khoe/tu-van-tinh-duc.html
            'Ngắm', # https://afamily.vn/tieu-dung/ngam.chn
            'Chi tiêu', #https://afamily.vn/tieu-dung/chi-tieu.chn
            'Vào bếp', #https://afamily.vn/an-ngon/toi-vao-bep.chn
            'Mẹo vặt gia đình', #https://afamily.vn/an-ngon/meo-vat.chn
            'Tâm sự', #https://afamily.vn/tam-su.chn
        ]
        for cate_name in categories:
            try:
                category = PostCategory.objects.create(name=cate_name, slug=slugify(cate_name))
                category.save()

            except:
                pass

            self.stdout.write(
                self.style.SUCCESS('Successfully added PostCategory "%s"' % cate_name)
            )