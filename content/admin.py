from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from . import models


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'display_category', 'publish']
    list_editable = ('publish',)
    list_filter = ('publish', 'category',)
    search_fields = ('title',)
    models.Post.display_category.short_description = _('Categories')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(models.PostCategory)
# admin.site.register(models.Post, PostAdmin)
