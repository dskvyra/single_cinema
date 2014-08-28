from django.test import TestCase, Client
from views import get_menu


class SingleCinemaTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_menu_names(self):
        items = ('home', 'contacts', 'xxx', 'one two')
        menu = get_menu(items)
        names = tuple(item.name for item in menu)

        self.assertEqual(names, items)

    def test_menu_to_unicode(self):
        items = ('home', 'contacts', 'xxx', 'one two')
        menu = get_menu(items)
        visual = tuple(unicode(item) for item in menu)

        self.assertEqual(visual, tuple(item.capitalize() for item in items))

    def test_menu_urls(self):
        items = ('home', 'contacts', 'xxx', 'one two')
        menu = get_menu(items)
        urls = tuple(item.url for item in menu)

        self.assertEqual(urls, ('home', 'contacts', 'xxx', 'one_two'))

    def test_rootpage_available(self):
        response = self.c.get('/')
        self.assertEquals(response.status_code, 200)

    def test_index_available(self):
        response = self.c.get('/index')
        self.assertEquals(response.status_code, 200)

    def test_homepage_available(self):
        response = self.c.get('/home')
        self.assertEquals(response.status_code, 200)

    def test_busypage_avalible(self):
        response = self.c.get('/busy')
        self.assertEquals(response.status_code, 200)
