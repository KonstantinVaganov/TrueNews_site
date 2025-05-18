from django import template
import news.views as views

register = template.Library()  #Регистрация наших тегов


def get_categories():
    return views.cats_db