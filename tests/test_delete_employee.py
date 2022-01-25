"""Module with DeleteEmployeeTest unittest Test Case class."""
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from logs.web_logger import logger
from main import my_app

browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())


class DeleteEmployeeTest(unittest.TestCase):
    """
    A Test Case class for deleting an employee item from the database.
    Creates and then deletes an employee item.
    """
    def setUp(self):
        self.app = my_app.test_client()
        self.app.testing = True
        self.driver = browser

    def test_new_employee_deletion(self):
        """Create and delete new employee using Selenium webdriver."""
        logger.debug('Creating test employee')
        driver = self.driver
        page_url = 'http://127.0.0.1:5000/new-employee'
        driver.get(page_url)
        name_form = driver.find_element(By.XPATH, '//*[@id="name"]')
        name_form.send_keys('Jesus Christ')
        salary_form = driver.find_element(By.XPATH, '//*[@id="salary"]')
        salary_form.send_keys('1')
        birth_form = driver.find_element(By.XPATH, '//*[@id="birthday"]')
        birth_form.send_keys('01011')
        submit = driver.find_element(By.XPATH, '//*[@id="submit"]')
        submit.click()
        logger.debug('Deleting test employee')
        employee_to_delete = driver.find_element(By.LINK_TEXT, 'Jesus Christ')
        employee_to_delete.click()
        delete_button = driver.find_element(By.XPATH, '/html/body/a[2]/button')
        delete_button.click()
        employees = self.app.get('/employees')
        self.assertNotIn('Jesus Christ', str(employees.data))

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
