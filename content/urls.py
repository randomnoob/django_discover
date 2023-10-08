from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    # path('search/', views.Search.as_view(), name='search'),
    # path('blog/<int:pk>/', views.PostArchiveByCategoryPK.as_view(), name='blog_archive_by_category_pk'),
    path('blog/<str:slug>/', views.PostSingle.as_view(), name='blog_single'),
]
