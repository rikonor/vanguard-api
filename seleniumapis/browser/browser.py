from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.common.exceptions import *

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
        print "trying to get"
        self.driver.get(path)

    def close(self):
        self.driver.close()

    @property
    def inputs(self):
        return []

    @property
    def title(self):
        return self.driver.title

    def contains_text(self, text):
        return text in self.driver.page_source

    def find_element_by_any(self, search_term):
        """
        Find an element by a search term
        Try ID, then fallback to Name
        """
        return self.find_element_by_id(search_term) or \
               self.find_element_by_name(search_term)

    def find_element_by_id(self, eid):
        try:
            return self.driver.find_element_by_id(eid)
        except NoSuchElementException:
            return None

    def find_element_by_name(self, name):
        try:
            return self.driver.find_element_by_name(name)
        except NoSuchElementException:
            return None

    def find_element_by_class(self, eclass):
        try:
            return self.driver.find_element_by_class_name(eclass)
        except NoSuchElementException:
            return None

    def find_element_by_xpath(self, xpath):
        try:
            return self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return None

    def fill_form(self, form_id, form_info, submit_id=None):
        """
        Fill out a form on the currently visible page
        form_id - is the identifier for the form
        form_info is a mapping from input ids to values
        """
        # Try and find the form element
        form_el = self.find_element_by_any(form_id)
        found_form = form_el is not None

        if not form_el:
            form_el = self

        for input_id, input_val in form_info.items():
            input_el = form_el.find_element_by_id(input_id)
            input_el.send_keys(input_val)

        if found_form is True:
            return form_el.submit()

        submit = form_el.find_element_by_any(submit_id)
        submit.click()
