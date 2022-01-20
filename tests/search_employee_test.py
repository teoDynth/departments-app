"""Module with SearchEmployeeTest unittest Test Case class."""
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from main import my_app

browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())


class SearchEmployeeTest(unittest.TestCase):
    """
    A Test Case class for searching an employee item in the database by birthday.
    Creates, searches for and then deletes an employee item.
    """
    def setUp(self):
        self.app = my_app.test_client()
        self.app.testing = True
        self.driver = browser

    def test_search_employee(self):
        """Create and search for employee using Selenium webdriver."""
        driver = self.driver
        page_url = 'http://192.168.0.118:5000/new-employee'
        driver.get(page_url)
        name_form = driver.find_element(By.XPATH, '//*[@id="name"]')
        name_form.send_keys('Jesus Christ')
        salary_form = driver.find_element(By.XPATH, '//*[@id="salary"]')
        salary_form.send_keys('1')
        birth_form = driver.find_element(By.XPATH, '//*[@id="birthday"]')
        birth_form.send_keys('01011')
        submit = driver.find_element(By.XPATH, '//*[@id="submit"]')
        submit.click()

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
        employee_to_delete = driver.find_element(By.LINK_TEXT, 'Jesus Christ')
        employee_to_delete.click()
        delete_button = driver.find_element(By.XPATH, '/html/body/a[2]/button')
        delete_button.click()
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
