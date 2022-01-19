"""Module with UpdateEmployeeTest unittest Test Case class."""
import unittest
import main
from tests.test_functions import create_employee, delete_employee, browser
from selenium.webdriver.common.by import By


class UpdateEmployeeTest(unittest.TestCase):
    """A Test Case class for updating an employee item in the database.
     Creates, updates and then deletes an employee item."""
    def setUp(self):
        self.app = main.my_app.test_client()
        self.app.testing = True
        self.driver = browser

    def test_new_employee_edit(self):
        driver = self.driver
        create_employee(driver)

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

        driver.get('http://http://192.168.0.118:5000/employees')
        employees = self.app.get('/employees')
        self.assertIn('Jesus Christ Superstar', str(employees.data))

    def tearDown(self):
        driver = self.driver
        delete_employee(driver, 'Jesus Christ Superstar')
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
