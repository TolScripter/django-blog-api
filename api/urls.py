#from django.contrib import admin
from django.urls import path
from api import views 

urlpatterns = [
    #path('admin/', admin.site.urls),
    
    #users routes
    path('user/register/', views.register),
    path('user/login/', views.login),
    path('user/details/<int:id>', views.account_details),

    #tags routes
    path('blog/tags/', views.tags_list),
    path('blog/tag/details/<int:id>', views.tag_details),

    #categories routes
    path('blog/categories/', views.categories_list),
    path('blog/category/details/<int:id>', views.category_details),

    #posts routes
    path('blog/posts/', views.posts_list),
    path('blog/post/details/<int:id>', views.post_details),

    #likes routes
    path('post/likes/', views.likes_list),
    path('post/like/details/<int:id>', views.like_details),

    #views routes
    path('post/views/', views.views_list),

    #collections routes
    path('post/collections/', views.collection_list),
    path('post/collection/details/<int:id>', views.collection_details),
]
