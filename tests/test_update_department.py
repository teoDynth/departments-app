"""Module with UpdateDepartmentTest unittest Test Case class."""
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from logs.web_logger import logger
from main import my_app

browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())


class UpdateDepartmentTest(unittest.TestCase):
    """
    A Test Case class for updating a department item in the database.
    Creates, updates and then deletes a department item.
    """
    def setUp(self):
        self.app = my_app.test_client()
        self.app.testing = True
        self.driver = browser

    def test_new_department_edit(self):
        """Create and update new department using Selenium webdriver."""
        logger.debug('Creating test department')
        driver = self.driver
        page_url = 'http://127.0.0.1:5000/new-department'
        driver.get(page_url)
        form = driver.find_element(By.XPATH, '//*[@id="name"]')
        form.send_keys('Test department')
        submit = driver.find_element(By.XPATH, '//*[@id="submit"]')
        submit.click()

        logger.debug('Updating test department')
        department_to_edit = driver.find_element(By.LINK_TEXT, 'Test department')
        department_to_edit.click()
        edit_button = driver.find_element(By.XPATH, '/html/body/a[1]/button')
        edit_button.click()

        form = driver.find_element(By.XPATH, '//*[@id="name"]')
        form.clear()
        form.send_keys('Test department edit')
        submit = driver.find_element(By.XPATH, '//*[@id="submit"]')
        submit.click()

        driver.get('http://127.0.0.1:5000')
        departments = self.app.get('/')
        self.assertIn('Test department edit', str(departments.data))

    def tearDown(self):
        logger.debug('Deleting test department')
        driver = self.driver
        department_to_delete = driver.find_element(By.LINK_TEXT, 'Test department edit')
        department_to_delete.click()
        delete_button = driver.find_element(By.XPATH, '/html/body/a[2]/button')
        delete_button.click()
        self.driver.close()

        
if __name__ == "__main__":
    unittest.main()
    
