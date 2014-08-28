from django.test import TestCase, Client
from views import get_menu, decode_url, encode_url
from locking_tools import get_message, put_message


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
        items = ('home', 'contacts', 'xxx yy', 'one two')
        menu = get_menu(items)
        urls = tuple(item.url for item in menu)

        self.assertEqual(urls, ('home', 'contacts', 'xxx_yy', 'one_two'))

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

    def test_stop_page_404(self):
        response = self.c.get('/stop')
        self.assertEquals(response.status_code, 404)
        response = self.c.get('/stop/asdas')
        self.assertEquals(response.status_code, 404)
        response = self.c.get('/stop/-asdas')
        self.assertEquals(response.status_code, 404)

    def test_stop_page_302(self):
        response = self.c.get('/stop/123')
        self.assertEquals(response.status_code, 302)
        response = self.c.get('/stop/-123')
        self.assertEquals(response.status_code, 302)

    def test_put_to_and_get_from_queue(self):
        put_message()
        message = get_message()
        self.assertIsNotNone(message)

    def test_encode_url(self):
        urls = ('first second', 'www com')
        encoded_urls = tuple(encode_url(url) for url in urls)
        self.assertEqual(encoded_urls, ('first_second', 'www_com'))

    def test_decode_url(self):
        urls = ('first_second', 'www_com')
        decoded_urls = tuple(decode_url(url) for url in urls)
        self.assertEqual(decoded_urls, ('first second', 'www com'))