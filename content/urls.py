from django.urls import path
from django.views.generic import TemplateView

from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitemap, StaticSitemap


sitemaps = {
    'blog': PostSitemap,
    'static': StaticSitemap,
}

flatpages = [
    path("about", TemplateView.as_view(template_name="flatpages/about.html"), name="about"),
    path("contact", TemplateView.as_view(template_name="flatpages/contact.html"), name="contact"),
    path("privacy", TemplateView.as_view(template_name="flatpages/privacy.html"), name="privacy"),
    path("terms", TemplateView.as_view(template_name="flatpages/terms.html"), name="terms"),
    path("chuyen-doi-muc-dich-su-dung", TemplateView.as_view(template_name="flatpages/chuyen-doi-muc-dich-su-dung.html"), name="chuyen-doi-muc-dich-su-dung"),
    path("noi-quy", TemplateView.as_view(template_name="flatpages/noi-quy.html"), name="noi-quy"),
]

urlpatterns = flatpages + [
    path('', views.Index.as_view(), name='index'),
    path('feed/', views.AllPostFeed(), name='all_feed'),
    # path('search/', views.Search.as_view(), name='search'),
    # path('blog/<int:pk>/', views.PostArchiveByCategoryPK.as_view(), name='blog_archive_by_category_pk'),
    path('<slug:slug>/', views.CategoryDetailView.as_view(), name='category_single'),
    path('<slug:slug>', views.PostSingle.as_view(), name='blog_single'),
    path('<slug:slug>/amp', views.PostSingleAMP.as_view(), name='blog_single_amp'),
    path('user/<int:pk>/', views.UserDetailView.as_view(), name='user_single'),
    path('<slug:category_slug>/feed/', views.PostsByCategory(), name='feed_by_category'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
