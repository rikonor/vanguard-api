from unittest import TestCase

from browser import Browser

class TestBrowser(TestCase):
    def setUp(self):
        self.b = Browser()
        self.b.start()

    def tearDown(self):
        self.b.close()

    def test_can_start_browser(self):
        pass

    def test_can_get_google(self):
        self.b.get("http://www.google.com")
        self.assertEqual(self.b.title, "Google")

    def test_can_get_inputs(self):
        raise NotImplemented

    def test_can_submit_form(self):
        raise NotImplemented

    def test_can_go_and_come_back(self):
        raise NotImplemented
