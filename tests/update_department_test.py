"""Module with UpdateDepartmentTest unittest Test Case class."""
import unittest
import main
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())


class UpdateDepartmentTest(unittest.TestCase):
    """A Test Case class for updating a department item in the database.
     Creates, updates and then deletes a department item."""
    def setUp(self):
        self.app = main.my_app.test_client()
        self.app.testing = True
        self.driver = browser

    def test_new_department_edit(self):
        from service.test_functions import create_department
        driver = self.driver
        create_department(driver)

        department_to_edit = driver.find_element(By.LINK_TEXT, 'Test department')
        department_to_edit.click()
        edit_button = driver.find_element(By.XPATH, '/html/body/a[1]/button')
        edit_button.click()

        form = driver.find_element(By.XPATH, '//*[@id="name"]')
        form.clear()
        form.send_keys('Test department edit')
        submit = driver.find_element(By.XPATH, '//*[@id="submit"]')
        submit.click()

        driver.get('http://192.168.0.118:5000')
        departments = self.app.get('/')
        self.assertIn('Test department edit', str(departments.data))

    def tearDown(self):
        from service.test_functions import delete_department
        driver = self.driver
        delete_department(driver, 'Test department edit')
        self.driver.close()
