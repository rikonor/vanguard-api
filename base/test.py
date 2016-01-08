from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Remote(
   command_executor='http://192.168.99.100:4444/wd/hub',
   desired_capabilities=DesiredCapabilities.CHROME)

browser.get("http://www.yahoo.com") # Load page
assert "Yahoo" in browser.title
elem = browser.find_element_by_name("p") # Find the query box
elem.send_keys("seleniumhq" + Keys.RETURN)
time.sleep(0.2) # Let the page load, will be added to the API

try:
    browser.find_element_by_xpath("//a[contains(@href,'https://www.seleniumhq.org')]")
except NoSuchElementException:
    assert 0, "can't find seleniumhq"
browser.close()

