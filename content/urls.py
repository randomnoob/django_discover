from django.urls import path
from django.views.generic import TemplateView

from . import views

flatpages = [
    path("about", TemplateView.as_view(template_name="flatpages/about.html"), name="about"),
    path("contact", TemplateView.as_view(template_name="flatpages/contact.html"), name="contact"),
    path("privacy", TemplateView.as_view(template_name="flatpages/privacy.html"), name="privacy"),
    path("terms", TemplateView.as_view(template_name="flatpages/terms.html"), name="terms"),
    path("chuyen-doi-muc-dich-su-dung", TemplateView.as_view(template_name="flatpages/chuyen-doi-muc-dich-su-dung.html"), name="chuyen-doi-muc-dich-su-dung"),
]

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    # path('search/', views.Search.as_view(), name='search'),
    # path('blog/<int:pk>/', views.PostArchiveByCategoryPK.as_view(), name='blog_archive_by_category_pk'),
    path('content/<str:slug>/', views.PostSingle.as_view(), name='blog_single'),
] + flatpages
