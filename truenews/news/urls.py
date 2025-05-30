from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('categories/<slug:categories_slug>/', views.categories_posts, name='categories'),
]
