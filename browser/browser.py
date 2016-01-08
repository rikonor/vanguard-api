from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Browser(object):
    def __init__(self):
        self.remote = "http://192.168.99.100:4444/wd/hub"
        self.browser_type = DesiredCapabilities.CHROME

        self.browser = None

    def start(self):
        self.driver = webdriver.Remote(
           command_executor=self.remote,
           desired_capabilities=self.browser_type)

    def get(self, path):
        self.driver.get(path)

    def close(self):
        self.driver.close()

    @property
    def inputs(self):
        return []

    @property
    def title(self):
        return self.driver.title
