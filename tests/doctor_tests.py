# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

timeout = 10
class DoctorDiagnosis(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Firefox()
		self.base_url = "http://localhost:5000"
		self.verificationErrors = []
		self.accept_next_alert = True

	def test_doctor_diagnosis(self):
		self.test_workbench()
		driver = self.driver
		self.waitFor('indcn', 'id')
		driver.find_element_by_id("indcn").clear()
		driver.find_element_by_id("indcn").send_keys("Cold")
		self.waitFor('span.select2-selection.select2-selection--single', 'css')
		driver.find_element_by_css_selector("span.select2-selection.select2-selection--single").click()
		driver.find_element_by_css_selector("input.select2-search__field").clear()
		driver.find_element_by_css_selector("input.select2-search__field").send_keys("a")
		driver.find_element_by_name("DRUG_QTY0").clear()
		driver.find_element_by_name("DRUG_QTY0").send_keys("20")
		driver.find_element_by_name("DRUG_SCHEDULE0").clear()
		driver.find_element_by_name("DRUG_SCHEDULE0").send_keys("10-10-10")
		driver.find_element_by_name("DRUG_COMMENTS0").clear()
		driver.find_element_by_name("DRUG_COMMENTS0").send_keys("Take everyday")
		driver.find_element_by_name("DRUG_SCHEDULE0").clear()
		driver.find_element_by_name("DRUG_SCHEDULE0").send_keys("1-0-1")
		driver.find_element_by_css_selector("input.btn.btn-success").click()
		self.waitFor('div.pad-down.container > span', 'css')
		self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.pad-down.container > span"))
		self.assertEqual("Success!", driver.find_element_by_css_selector("div.pad-down.container > span").text)

	def test_history(self):
		self.test_login()
		driver = self.driver
		driver.get(self.base_url + "/doctor/")
		driver.find_element_by_link_text("History").click()
		self.waitFor("DATE", "name")
		driver.find_element_by_name("DATE").clear()
		driver.find_element_by_name("DATE").send_keys("2017-04-12")
		driver.find_element_by_css_selector("button.btn.btn-default").click()
		self.waitFor("div.visit-title.lightestcolor2", "css")
		self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.visit-title.lightestcolor2"))
		self.assertEqual("Patient ID :100035", driver.find_element_by_css_selector("p.ailment").text)
		driver.find_element_by_css_selector("p.ailment").click()
		self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "td"))

	def waitFor(self, element, selectorType):
		if selectorType == 'id':
			by = By.ID
		elif selectorType == 'css':
			by = By.CSS_SELECTOR
		elif selectorType == 'linktext':
			by = By.LINK_TEXT
		elif selectorType == 'name':
			by = By.NAME
		elif selectorType == 'xpath':
			by = By.XPATH

		try:
			element_present = EC.visibility_of_element_located((by, element))
			WebDriverWait(self.driver, timeout).until(element_present)
		except TimeoutException:
			print("Timed out waiting for page to load")

	def test_login(self):
		driver = self.driver
		driver.get(self.base_url + "/auth/login/doctor")
		driver.find_element_by_id("password").clear()
		driver.find_element_by_id("password").send_keys("password")
		driver.find_element_by_id("doctorID").clear()
		driver.find_element_by_id("doctorID").send_keys("1")
		driver.find_element_by_id("submit").click()
		self.waitFor('ID', 'id')
		self.assertTrue(self.is_element_present(By.ID, 'ID'))
		self.assertTrue(self.is_element_present(By.ID, 'submit'))


	def test_upcoming_appointments(self):
		self.test_login()
		driver = self.driver
#		driver.get(self.base_url + "/doctor/")
		driver.find_element_by_link_text("Upcoming Appointments").click()
		self.waitFor('h1.page-header', 'css')
		self.assertEqual("Upcoming Appointments", driver.find_element_by_css_selector("h1.page-header").text)


	def test_workbench(self):
		self.test_login()
		driver = self.driver
		driver.get(self.base_url + "/doctor/")
		driver.find_element_by_id("patientType-0").click()
		driver.find_element_by_id("ID").clear()
		driver.find_element_by_id("ID").send_keys("14it137")
		driver.find_element_by_id("submit").click()
		self.waitFor('indication', 'id')
		self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "a > b > i"))
		self.assertEqual("Ranganath Pai M", driver.find_element_by_css_selector("a > b > i").text)
		self.assertTrue(self.is_element_present(By.ID, "indication"))
  
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
