# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class PharmaTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost:5000"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_pharma_login(self):
        driver = self.driver
        driver.get(self.base_url + "/auth/login/pharma")
        driver.find_element_by_name("PASSWORD").send_keys("password")
        driver.find_element_by_name("PASSWORD").send_keys(Keys.ENTER)
        # ERROR: Caught exception [ERROR: Unsupported command [keyPress | name=PASSWORD | \13]]
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Pharmacist"))
        self.assertEqual("Pharmacist", driver.find_element_by_link_text("Pharmacist").text)
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
