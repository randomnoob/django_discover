from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('search/', views.Search.as_view(), name='search'),
    path('blog/', views.Blog.as_view(), name='blog'),
    path('create/blog/', views.BlogCreateView.as_view(), name='blog_create'),
    path('create/blog_category/', views.BlogCategoryCreateView.as_view(), name='blog_category_create'),
    path('blog/<int:pk>/', views.BlogArchiveByCategoryPK.as_view(), name='blog_archive_by_category_pk'),
    path('blog/<str:slug>/', views.BlogSingle.as_view(), name='blog_single'),
]
