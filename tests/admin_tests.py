 # -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import unittest, time, re


class AdminTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        # self.driver.implicitly_wait(3000)
        self.base_url = "http://localhost:5000"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_admin_login(self):
        driver = self.driver
        driver.get(self.base_url + "/auth/login/admin")
        driver.find_element_by_name("PASSWORD").send_keys("admin")
        driver.find_element_by_name("PASSWORD").send_keys(Keys.ENTER)
        # ERROR: Caught exception [ERROR: Unsupported command [keyPress | name=PASSWORD | \13]]
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Admin"))
        )
        self.assertEqual("Admin", driver.find_element_by_link_text("Admin").text)

    def test_generate_slots(self):
        driver = self.driver
        self.test_admin_login()
        driver.get(self.base_url + "/admin/reschedule")
        driver.find_element_by_id("datepicker").click()
        driver.find_element_by_link_text("Next").click()
        driver.find_element_by_link_text("Next").click()
        driver.find_element_by_link_text("30").click()
        driver.find_element_by_id("generate-slots-btn").click()
        element = WebDriverWait(driver, 2).until(EC.alert_is_present())
        self.assertEqual("Slots have been opened till 2017-6-30", self.close_alert_and_get_its_text())

    def test_book_appointment(self):
        self.test_admin_login()
        driver = self.driver
        driver.get(self.base_url + "/admin/appointments")
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "PAEDIATRICS"))
        )
        driver.find_element_by_name("PAEDIATRICS").click()
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "pType"))
        )
        driver.find_element_by_name("pType").click()
        driver.find_element_by_id("ID").clear()
        driver.find_element_by_id("ID").send_keys("14it137")
        driver.find_element_by_id("make-appointment-btn").click()
        datepicker = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "datepicker"))
        )
        datepicker.click()
        driver.find_element_by_link_text("25").click()
        driver.find_element_by_id("make-appointment-btn").click()
        driver.find_element_by_id("confirm-btn").click()
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "#mainrow > span"))
        self.assertEqual("Success!", driver.find_element_by_css_selector("#mainrow > span").text)

    def test_cancel_appointment(self):
        self.test_admin_login()
        driver = self.driver
        driver.get(self.base_url + "/admin/appointments")
        appointment = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Appointments"))
        )
        appointment.click()
        paediatrics = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "PAEDIATRICS"))
        )
        sleep(3)
        driver.find_element_by_name("PAEDIATRICS").click()
        datepicker = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "datepicker"))
        )
        datepicker.click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.LINK_TEXT, "25"))
        )
        driver.find_element_by_link_text("25").click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "li.item"))
        )
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "li.item"))
        self.assertEqual("Ranganath Pai M---\nDr.Anil Kumar\n\nCancel Appointment",
                         driver.find_element_by_css_selector("li.item").text)
        driver.find_element_by_name("SLOTID").click()
        self.assertFalse(self.is_element_present(By.CSS_SELECTOR, "booked-appointments-list.item"))

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
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
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
