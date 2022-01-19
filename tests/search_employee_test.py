"""Module with SearchEmployeeTest unittest Test Case class."""
import unittest
import main
from tests.test_functions import create_employee, delete_employee, browser
from selenium.webdriver.common.by import By


class SearchEmployeeTest(unittest.TestCase):
    """
    A Test Case class for searching an employee item in the database by birthday.
    Creates, searches for and then deletes an employee item.
    """
    def setUp(self):
        self.app = main.my_app.test_client()
        self.app.testing = True
        self.driver = browser

    def test_search_employee(self):
        driver = self.driver
        create_employee(driver)

        search_button = driver.find_element(By.XPATH, '/html/body/a[1]/button')
        search_button.click()

        date_form = driver.find_element(By.XPATH, '//*[@id="query_date"]')
        date_form.send_keys('01011')
        submit = driver.find_element(By.XPATH, '//*[@id="submit"]')
        submit.click()

        result = driver.find_element(By.LINK_TEXT, 'Jesus Christ')
        self.assertIn('Jesus Christ', result.text)

    def tearDown(self):
        driver = self.driver
        driver.get('http://192.168.0.118:5000/employees')
        delete_employee(driver, 'Jesus Christ')
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
