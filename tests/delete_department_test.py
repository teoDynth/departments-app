"""Module with DeleteDepartmentTest unittest Test Case class."""

import unittest
import main
from test_functions import create_department, delete_department, browser


class DeleteDepartmentTest(unittest.TestCase):
    """
    A Test Case class for deleting a department item from the database.
    Creates and then deletes a department item.
    """
    def setUp(self):
        self.app = main.my_app.test_client()
        self.app.testing = True
        self.driver = browser

    def test_new_department_deletion(self):
        driver = self.driver
        create_department(driver)
        delete_department(driver, 'Test department')
        departments = self.app.get('/')
        self.assertNotIn('Test department', str(departments.data))

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
