"""Module with DeleteEmployeeTest unittest Test Case class."""
import unittest
import main
from tests.test_functions import browser


class DeleteEmployeeTest(unittest.TestCase):
    """
    A Test Case class for deleting an employee item from the database.
    Creates and then deletes an employee item.
    """
    def setUp(self):
        self.app = main.my_app.test_client()
        self.app.testing = True
        self.driver = browser

    def test_new_employee_deletion(self):
        from tests.test_functions import create_employee, delete_employee
        driver = self.driver
        create_employee(driver)
        delete_employee(driver, 'Jesus Christ')
        employees = self.app.get('/employees')
        self.assertNotIn('Jesus Christ', str(employees.data))

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
