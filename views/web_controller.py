"""
A module with functions that add URL rules and API resources.

Functions:
add_url_rules -- adds URL rules for application to follow
add_api_resources -- adds API resources for application to use
"""
from service import web_service
from rest import restful_departments


def add_url_rules(app):
    """
    Add URL rules to a specified application.

    Parameter:
    app -- Flask application of choice
    """
    app.add_url_rule('/', view_func=web_service.show_departments)
    app.add_url_rule('/departments', view_func=web_service.show_departments)
    app.add_url_rule('/departments/<int:department_id>', view_func=web_service.show_department)
    app.add_url_rule('/employees', view_func=web_service.show_employees)
    app.add_url_rule('/employees/<int:employee_id>', view_func=web_service.show_employee)
    app.add_url_rule(
        '/new-department',
        methods=['POST', 'GET'],
        view_func=web_service.new_department
    )
    app.add_url_rule(
        '/edit-department/<int:department_id>',
        methods=['POST', 'GET'],
        view_func=web_service.edit_department
    )
    app.add_url_rule(
        '/delete-department/<int:department_id>',
        view_func=web_service.delete_department
    )
    app.add_url_rule('/new-employee', methods=['POST', 'GET'], view_func=web_service.new_employee)
    app.add_url_rule(
        '/edit-employee/<int:employee_id>',
        methods=['POST', 'GET'],
        view_func=web_service.edit_employee
    )
    app.add_url_rule('/delete-employee/<int:employee_id>', view_func=web_service.delete_employee)
    app.add_url_rule(
        '/search-employee',
        methods=['POST', 'GET'],
        view_func=web_service.search_employee
    )


def add_api_resources(api):
    """
    Add API resources to a specified API.

    Parameter:
    api -- a Flask-Restful API used by an application
    """
    api.add_resource(restful_departments.DepartmentList, '/api/departments')
    api.add_resource(restful_departments.EmployeeList, '/api/employees')
    api.add_resource(restful_departments.OneDepartment, '/api/departments/<int:department_id>')
    api.add_resource(restful_departments.OneEmployee, '/api/employees/<int:employee_id>')
