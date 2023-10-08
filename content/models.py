from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from ckeditor_uploader.fields import RichTextUploadingField

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

def get_default_user():
    try:
        user = User.objects.get(username = "M. Trang")
    except:
        user = User.objects.create_user("M. Trang", "mtrang@gmail.com", "mtrangpassword")
    return user

class PostCategory(models.Model):
    title = models.CharField(
        max_length=512,
        verbose_name=_('Title :'),
        unique=True,
        blank=False,
        null=False
    )
    slug = models.SlugField(
        max_length=256,
        verbose_name=_('Slug :'),
        unique=True,
        null=False,
        blank=False
    )

    class Meta:
        verbose_name = _('Post Category')
        verbose_name_plural = _('Post Categories')

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(
        max_length=256,
        verbose_name=_('Title :'),
        unique=True,
        null=False,
        blank=False
    )
    slug = models.SlugField(
        max_length=256,
        verbose_name=_('Slug :'),
        unique=True,
        null=False,
        blank=False
    )
    thumbnail = models.CharField(
        max_length=1024,
        verbose_name=_('Thumbnail URL :'),
        default="https://afamilycdn.com/thumb_w/250/150157425591193600/2023/10/3/banh-tortilla-ga-cuon-8-16963228568751458823194-112-0-612-800-crop-1696324527645754379197.jpg"
    )
    category = models.ForeignKey(
        PostCategory,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    author = models.ForeignKey(
        User,
        on_delete= models.CASCADE,
        related_name='blog_posts',
        default=get_default_user
    )

    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def display_category(self):
        return ', '.join([cat.title for cat in self.category.all()])

    def __str__(self):
        return self.title


