"""Module with CreateDepartmentTest unittest Test Case class."""
import unittest
import main
from test_functions import create_department, delete_department, browser


class CreateDepartmentTest(unittest.TestCase):
    """A Test Case class for creating a department item in the database. Creates and then deletes a department item."""
    def setUp(self):
        self.app = main.my_app.test_client()
        self.app.testing = True
        self.driver = browser

    def test_new_department_creation(self):
        driver = self.driver
        create_department(driver)
        departments = self.app.get('/')
        self.assertIn('Test department', str(departments.data))

    def tearDown(self):
        driver = self.driver
        delete_department(driver, 'Test department')
        self.driver.close()
