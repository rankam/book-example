from django.core.urlresolvers import resolve
from django.test import Client, TestCase
from django.http import HttpRequest

from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', response.content)
        self.assertTrue(response.content.strip().endswith('</html>'))


    def test_home_page_renders_correct_template(self):
        response = Client().get('/')
        self.assertTemplateUsed(response, 'home.html')

