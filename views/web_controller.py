"""
A module with functions that add URL rules and API resources.

Functions:
add_url_rules -- adds URL rules for application to follow
add_api_resources -- adds API resources for application to use
"""
from service.web_service import *
from rest.restful_departments import *
from logs.web_logger import logger

url_rules = {
    '/': show_departments,
    '/departments': show_departments,
    '/departments/<int:department_id>': show_department,
    '/employees': show_employees,
    '/employees/<int:employee_id>': show_employee,
    '/new-department': new_department,
    '/edit-department/<int:department_id>': edit_department,
    '/delete-department/<int:department_id>': delete_department,
    '/new-employee': new_employee,
    '/edit-employee/<int:employee_id>': edit_employee,
    '/delete-employee/<int:employee_id>': delete_employee,
    '/search-employee': search_employee
}

api_resources = {
    DepartmentList: '/api/departments',
    EmployeeList: '/api/employees',
    OneDepartment: '/api/departments/<int:department_id>',
    OneEmployee: '/api/employees/<int:employee_id>'
}


def add_url_rules(app):
    """
    Add URL rules to a specified application.

    Parameter:
    app -- Flask application of choice
    """
    logger.debug('Adding URL rules')
    for key, value in url_rules.items():
        app.add_url_rule(key, view_func=value, methods=['POST', 'GET'])


def add_api_resources(api):
    """
    Add API resources to a specified API.

    Parameter:
    api -- a Flask-Restful API used by an application
    """
    logger.debug('Adding API resources')
    for key, value in api_resources.items():
        api.add_resource(key, value)
