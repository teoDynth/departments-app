"""Module with UpdateEmployeeTest unittest Test Case class."""
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())


class UpdateEmployeeTest(unittest.TestCase):
    """A Test Case class for updating an employee item in the database.
     Creates, updates and then deletes an employee item."""
    def setUp(self):
        from main import my_app
        self.app = my_app.test_client()
        self.app.testing = True
        self.driver = browser

    def test_new_employee_edit(self):
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

        employee_to_edit = driver.find_element(By.LINK_TEXT, 'Jesus Christ')
        employee_to_edit.click()
        edit_button = driver.find_element(By.XPATH, '/html/body/a[1]/button')
        edit_button.click()

        name_form = driver.find_element(By.XPATH, '//*[@id="name"]')
        name_form.clear()
        name_form.send_keys('Jesus Christ Superstar')
        salary_form = driver.find_element(By.XPATH, '//*[@id="salary"]')
        salary_form.clear()
        salary_form.send_keys('1111111')
        birth_form = driver.find_element(By.XPATH, '//*[@id="birthday"]')
        birth_form.clear()
        birth_form.send_keys('11111111')
        submit = driver.find_element(By.XPATH, '//*[@id="submit"]')
        submit.click()

        driver.get('http://192.168.0.118:5000/employees')
        employees = self.app.get('/employees')
        self.assertIn('Jesus Christ Superstar', str(employees.data))

    def tearDown(self):
        driver = self.driver
        employee_to_delete = driver.find_element(By.LINK_TEXT, 'Jesus Christ Superstar')
        employee_to_delete.click()
        delete_button = driver.find_element(By.XPATH, '/html/body/a[2]/button')
        delete_button.click()
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
