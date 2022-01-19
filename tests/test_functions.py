"""
Module with Selenium webdriver installation and functions for unittest classes. Contains following functions -

Functions:
create_department -- creates a new test department item in the database
delete_department -- deletes a test department item from the database
create_employee -- creates a new test employee item in the database
delete_employee -- deletes a test employee item from the database
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())


def create_department(driver):
    """
    Create a new department item in the database using Selenium webdriver.

    Parameter:
    driver -- driver for chosen web browser
    """
    page_url = 'http://192.168.0.118:5000/new-department'
    driver.get(page_url)
    form = driver.find_element(By.XPATH, '//*[@id="name"]')
    form.send_keys('Test department')
    submit = driver.find_element(By.XPATH, '//*[@id="submit"]')
    submit.click()


def delete_department(driver, department_name):
    """
    Delete a department item in the database using Selenium webdriver.

    Parameters:
    driver -- driver for chosen web browser
    department_name -- name of a department item to delete
    """
    department_to_delete = driver.find_element(By.LINK_TEXT, f'{department_name}')
    department_to_delete.click()
    delete_button = driver.find_element(By.XPATH, '/html/body/a[2]/button')
    delete_button.click()


def create_employee(driver):
    """
    Create a new employee item in the database using Selenium webdriver.

    Parameter:
    driver -- driver for chosen web browser
    """
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


def delete_employee(driver, employee_name):
    """
    Delete an employee item in the database using Selenium webdriver.

    Parameters:
    driver -- driver for chosen web browser
    employee_name -- name of an employee item to delete
    """
    employee_to_delete = driver.find_element(By.LINK_TEXT, f'{employee_name}')
    employee_to_delete.click()
    delete_button = driver.find_element(By.XPATH, '/html/body/a[2]/button')
    delete_button.click()
