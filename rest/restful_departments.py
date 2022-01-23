"""
Module with RESTful service implementation.

Adds arguments to Request Parser from Flask-RESTful extension.

Functions:
get_departments -- returns a dictionary representation of all departments in the database
get_employees -- returns a dictionary representation of all employees in the database
abort_if_department_doesnt_exist -- aborts operation if department does not exist in the database
abort_if_employee_doesnt_exist -- aborts operation if an employee does not exist in the database

Classes:
DepartmentList -- shows department list and lets you POST to add new departments
EmployeeList -- shows employee list and lets you POST to add new employees
OneDepartment -- shows a single department item and lets you delete a department item
OneEmployee -- shows a single employee item and lets you delete an employee item
"""
from flask_restful import reqparse, abort, inputs, Resource

from models.db_models import db, Department, Employee
from logs.web_logger import logger

parser = reqparse.RequestParser()
parser.add_argument('department', help='Department name')
parser.add_argument('employee', help='Employee name')
parser.add_argument('salary', type=float, help='Employee salary')
parser.add_argument('birthday', type=inputs.date, help='Employee birthday')
parser.add_argument('department_id', type=int, help='Employee department id')


def get_departments():
    """
    Get the list of all department items in the database and return it in the form of a dictionary.
    """
    logger.debug('Getting all departments')
    dep_dict = {}
    all_departments = Department.query.all()
    for d in all_departments:
        dep = {d.id: {'department': d.name}}
        dep_dict.update(dep)
    return dep_dict


def get_employees():
    """
    Get the list of all employee items in the database and return it in the form of a dictionary.
    """
    logger.debug('Getting all employees')
    emp_dict = {}
    all_employees = Employee.query.all()
    for e in all_employees:
        emp = {e.id: {
            'employee': e.name,
            'salary': f'{e.salary}',
            'birthday': f'{e.birthday.year}/{e.birthday.month}/{e.birthday.day}',
            'department': e.department.name}
        }
        emp_dict.update(emp)
    return emp_dict


def abort_if_department_doesnt_exist(department_id):
    """
    Check if a department item is in the database, if not abort.

    Parameter:
    department_id(int) -- unique id of a department item
    """
    all_departments = get_departments()
    if department_id not in all_departments:
        abort(404, message=f"Department {department_id} doesn't exist")


def abort_if_employee_doesnt_exist(employee_id):
    """
    Check if an employee item is in the database, if not abort.

    Parameter:
    employee_id(int) -- unique id of an employee item
    """
    all_employees = get_employees()
    if employee_id not in all_employees:
        abort(404, message=f"Employee {employee_id} doesn't exist")


class DepartmentList(Resource):
    """
    A class used to represent a CRUD resource for the application.
    Gives access to HTTP methods GET and POST.
    This particular resource deals with the list of departments.

    Methods:
        get -- gets the list of all department items in the database
        post -- adds a new department item to the database
    """
    def get(self):
        """Return the list of all department items."""
        return get_departments()

    def post(self):
        """
        Add a new department item to the database.
        Return the list of all department items including a new one.
        """
        args = parser.parse_args(strict=True)
        department = Department(name=args['department'])
        db.session.add(department)
        db.session.commit()
        logger.debug(f' Creating {department}')
        return get_departments(), 201


class EmployeeList(Resource):
    """
    A class used to represent a CRUD resource for the application.
    Gives access to HTTP methods GET and POST.
    This particular resource deals with the list of employees.

    Methods:
        get -- gets the list of all employee items in the database
        post -- adds a new employee item to the database
    """
    def get(self):
        """Return the list of all employee items."""
        return get_employees()

    def post(self):
        """
        Add a new employee item to the database.
        Return the list of all employee items including a new one.
        """
        args = parser.parse_args(strict=True)
        employee = Employee(
            name=args['employee'],
            salary=args['salary'],
            birthday=args['birthday'],
            department_id=args['department_id']
        )
        db.session.add(employee)
        db.session.commit()
        logger.debug(f'Creating {employee}')
        return get_employees(), 201


class OneDepartment(Resource):
    """
    A class used to represent a CRUD resource for the application.
    Gives access to HTTP methods GET and POST.
    This particular resource deals with the specified department item.

    Methods:
        get -- gets the specified department item
        delete -- deletes the specified department item
        put -- edits the specified department item
    """
    def get(self, department_id):
        """
        Return the specified department item.

        Parameter:
        department_id(int) -- unique id of a department item
        """
        abort_if_department_doesnt_exist(department_id)
        all_departments = get_departments()
        logger.debug(f'Getting department with id {department_id}')
        return all_departments[department_id]

    def delete(self, department_id):
        """
        Delete the specified department item.

        Parameter:
        department_id(int) -- unique id of a department item
        """
        abort_if_department_doesnt_exist(department_id)
        department_to_delete = Department.query.get(department_id)
        db.session.delete(department_to_delete)
        db.session.commit()
        logger.debug(f'Deleting department with id {department_id}')
        return '', 204

    def put(self, department_id):
        """
        Edit the specified department item.

        Parameter:
        department_id(int) -- unique id of a department item
        """
        args = parser.parse_args(strict=True)
        department = Department.query.get(department_id)
        department.name = args['department']
        db.session.commit()
        all_departments = get_departments()
        logger.debug(f'Updating department with id {department_id}')
        return all_departments[department_id], 201


class OneEmployee(Resource):
    """
    A class used to represent a CRUD resource for the application.
    Gives access to HTTP methods GET and POST.
    This particular resource deals with the specified employee item.

    Methods:
        get -- gets the specified employee item
        delete -- deletes the specified employee item
        put -- edits the specified employee item
    """
    def get(self, employee_id):
        """
        Return the specified employee item.

        Parameter:
        employee_id(int) -- unique id of an employee item
        """
        abort_if_employee_doesnt_exist(employee_id)
        all_employees = get_employees()
        logger.debug(f'Getting employee with id {employee_id}')
        return all_employees[employee_id]

    def delete(self, employee_id):
        """
        Delete the specified employee item.

        Parameter:
        employee_id(int) -- unique id of an employee item
        """
        employee_to_delete = Employee.query.get(employee_id)
        db.session.delete(employee_to_delete)
        db.session.commit()
        logger.debug(f'Deleting employee with id {employee_id}')
        return '', 204

    def put(self, employee_id):
        """
        Edit the specified employee item.

        Parameter:
        employee_id(int) -- unique id of an employee item
        """
        args = parser.parse_args()
        employee = Employee.query.get(employee_id)
        employee.name = args['employee']
        employee.salary = args['salary']
        employee.birthday = args['birthday']
        employee.department_id = args['department_id']
        db.session.commit()
        all_employees = get_employees()
        logger.debug(f'Updating employee with id {employee_id}')
        return all_employees[employee_id], 201
