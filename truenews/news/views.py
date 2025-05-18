from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import News, Category


def index(request):
    post = News.published.all()
    data = {
        'posts': post,
            }
    return render(request, 'news/index.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound('Такой страницы не существует')


def show_post(request, post_slug):
    post = get_object_or_404(News, slug=post_slug)
    data = {
        'post': post,
    }
    return render(request, 'news/post.html', data)


def categories_posts(request, categories_slug):
    category = get_object_or_404(Category, slug=categories_slug)
    post = News.published.filter(categ_id=category.pk)
    posts = {
        'post': post,
        'post_category': category
    }
    return render(request, 'news/categories.html', posts)

