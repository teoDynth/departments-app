"""Module with DeleteDepartmentTest unittest Test Case class."""
import unittest
import main
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())


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
        page_url = 'http://192.168.0.118:5000/new-department'
        driver.get(page_url)
        form = driver.find_element(By.XPATH, '//*[@id="name"]')
        form.send_keys('Test department')
        submit = driver.find_element(By.XPATH, '//*[@id="submit"]')
        submit.click()
        department_to_delete = driver.find_element(By.LINK_TEXT, 'Test department')
        department_to_delete.click()
        delete_button = driver.find_element(By.XPATH, '/html/body/a[2]/button')
        delete_button.click()
        departments = self.app.get('/')
        self.assertNotIn('Test department', str(departments.data))

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
