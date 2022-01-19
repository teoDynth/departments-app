"""Module with CreateEmployeeTest unittest Test Case class."""
import unittest
import main
from tests.test_functions import create_employee, delete_employee, browser


class CreateEmployeeTest(unittest.TestCase):
    """A Test Case class for creating an employee item in the database. Creates and then deletes an employee item."""
    def setUp(self):
        self.app = main.my_app.test_client()
        self.app.testing = True
        self.driver = browser

    def test_new_employee_creation(self):
        driver = self.driver
        create_employee(driver)
        employees = self.app.get('/employees')
        self.assertIn('Jesus Christ', str(employees.data))

    def tearDown(self):
        driver = self.driver
        delete_employee(driver, 'Jesus Christ')
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
