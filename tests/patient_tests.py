
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest, time, re

timeout = 5

class PatientTesting(unittest.TestCase):

	def waitFor(self, element, selectorType):
		if selectorType == 'id':
			by = By.ID
		elif selectorType == 'css':
			by = By.CSS_SELECTOR
		elif selectorType == 'linktext':
			by = By.LINK_TEXT
		elif selectorType == 'name':
			by = By.NAME

		try:
		    element_present = EC.visibility_of_element_located((by, element))
		    WebDriverWait(self.driver, timeout).until(element_present)
		except TimeoutException:
		    print("Timed out waiting for page to load")


	def setUp(self):
		self.driver = webdriver.Firefox()
		self.driver.implicitly_wait(30)
		self.base_url = "http://localhost:5000"
		self.verificationErrors = []
		self.accept_next_alert = True
	
	def test_login(self):
		driver = self.driver
		driver.get(self.base_url + "/auth/login")
		self.waitFor("ID", 'id')
		driver.find_element_by_id("ID").clear()
		driver.find_element_by_id("ID").send_keys("14it137")
		driver.find_element_by_id("password").clear()
		driver.find_element_by_id("password").send_keys("password")
		driver.find_element_by_id("submit").click()
		self.assertTrue(self.is_element_present(By.XPATH, "//td[3]"))
		self.assertEqual("14IT137", driver.find_element_by_xpath("//td[3]").text)
		

	def test_medical_history(self):
		self.test_login()
		driver = self.driver
		driver.get(self.base_url + "/patient/profile")
		self.waitFor("Medical History", 'linktext')
		driver.find_element_by_link_text("Medical History").click()
		self.waitFor("p.ailment", 'css')
		driver.find_element_by_css_selector("p.ailment").click()
		self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "p.doctor-name"))
		self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "p.pres-id.pull-right"))
		self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "th"))
		self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "td"))
		driver.find_element_by_css_selector("p.ailment").click()

   
	def test_logout(self):
		self.test_login()
		driver = self.driver
		driver.implicitly_wait(300)
		driver.find_element_by_link_text("Ranganath Pai M").click()
		driver.find_element_by_link_text("Log Out").click()
		self.assertTrue(self.is_element_present(By.LINK_TEXT, "Click here to register"))
		self.assertEqual("Click here to register", driver.find_element_by_link_text("Click here to register").text)
		self.assertEqual("", driver.find_element_by_css_selector("img.nitk-logo").text)
	
	def test_book_appointment(self):
		self.test_login()
		driver = self.driver
		driver.get(self.base_url + "/patient/profile")
		self.waitFor("Appointments", 'linktext')
		driver.find_element_by_link_text("Appointments").click()
		print("waiting")
		driver.implicitly_wait(3000)
		print("done waiting")
		self.waitFor("PAEDIATRICS", 'name')
		driver.find_element_by_name("PAEDIATRICS").click()
		self.waitFor("datepicker", 'id')
		driver.find_element_by_id("datepicker").click()
		driver.find_element_by_link_text("28").click()
		driver.find_element_by_id("confirm-btn").click()
		self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "li.item > span"))
		self.assertEqual("Dr.Anil Kumar(Paediatrics)\n8:00:00 to 9:00:00", driver.find_element_by_css_selector("li.item > span").text)
		driver.find_element_by_name("SLOTID").click()
		# driver.refresh()
		# self.waitFor("li.item", 'css')
		# driver.implicitly_wait(300)
		# self.assertFalse(self.is_element_present(By.CSS_SELECTOR, "li.item"))
	
	def test_incorrect_password_login(self):
		driver = self.driver
		driver.get(self.base_url + "/auth/login")
		driver.find_element_by_id("ID").clear()
		driver.find_element_by_id("ID").send_keys("14it137")
		driver.find_element_by_id("password").clear()
		driver.find_element_by_id("password").send_keys("wrongpassword")
		driver.find_element_by_id("submit").click()
		self.assertTrue(self.is_element_present(By.XPATH, "//div/div"))
		self.assertEqual(u"×\nPlease check your password again!", driver.find_element_by_xpath("//div/div").text)
	
	def test_incorrect_username_login(self):
		driver = self.driver
		driver.get(self.base_url + "/auth/login")
		driver.find_element_by_id("ID").clear()
		driver.find_element_by_id("ID").send_keys("wrongusername")
		driver.find_element_by_id("password").clear()
		driver.find_element_by_id("password").send_keys("wrongpassword")
		driver.find_element_by_id("submit").click()
		self.assertTrue(self.is_element_present(By.XPATH, "//div/div"))
		self.assertEqual(u"×\nInvalid username! Please check your username again.", driver.find_element_by_xpath("//div/div").text)
	
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