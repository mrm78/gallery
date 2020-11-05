from django.urls import path
from .views import home, edit_product, add_product, add_article, edit_article, Article, article_commenting, list_articles

urlpatterns = [
    path('', home, name='home'),
    path('article/<int:ID>', Article, name='article'),
    path('list_article', list_articles, name='list_articles'),
    path('add_product', add_product, name='add_product'),
    path('edit_product/<int:ID>', edit_product, name='edit_product'),
    path('add_article', add_article, name='add_article'),
    path('edit_article/<int:ID>', edit_article, name='edit_article'),
    path('article_commenting', article_commenting, name='article_commenting'),
]