from django.test import TestCase
from django.urls import reverse, resolve
from .views import HomePageView, ArticleList, ArticleCategoryList, ArticleDetail
from .models import Category, Article
from django.utils import timezone

class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func.view_class, HomePageView)


class ArticleListTests(TestCase):
    def test_articles_list_status_code(self):
        url = reverse('articles-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_articles_list_resolves_view(self):
        view = resolve('/articles')
        self.assertEqual(view.func.view_class, ArticleList)


class ArticleCategoryTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(category="Фільми", slug="Опенгеймер")

    def test_articles_category_status_code(self):
        url = reverse('articles-category-list', args=[self.category.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_articles_category_resolves_view(self):
        view = resolve(f'/articles/category/{self.category.slug}')
        self.assertEqual(view.func.view_class, ArticleCategoryList)


class ArticleDetailTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(category="Спорт", slug="Футбол")
        self.article = Article.objects.create(
            title="Перша стаття",
            description="Опис статті",
            slug="persha-stattya",
            category=self.category,
            pub_date=timezone.now(),
            main_page=True
        )

    def test_article_detail_status_code(self):
        url = reverse('news-detail', args=[
            self.article.pub_date.strftime("%Y"),
            self.article.pub_date.strftime("%m"),
            self.article.pub_date.strftime("%d"),
            self.article.slug
        ])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_article_detail_resolves_view(self):
        path = f'/articles/{self.article.pub_date.strftime("%Y")}/{self.article.pub_date.strftime("%m")}/{self.article.pub_date.strftime("%d")}/{self.article.slug}'
        view = resolve(path)
        self.assertEqual(view.func.view_class, ArticleDetail)