from browser import Browser

class Base(object):
    def __init__(self):
        self.browser = Browser()
        self.start_browser()

        self.logged_in = False

    def start_browser(self):
        self.browser.start()

    def close_browser(self):
        self.browser.close()
