"""
Module with functions to work with DB(CRUD operations and search).

Functions:
new_department -- creates a new department item in the database
new_employee -- creates a new employee item in the database
show_departments -- reads the database to show department item list
show_department -- reads the database to show a specific department item
show_employees -- reads the database to show employee item list
show_employee -- reads the database to show a specific employee item
edit_department -- updates a specific department item in the database
edit_employee -- updates a specific employee item in the database
delete_department -- deletes a specific department item from the database
delete_employee -- deletes a specific employee item from the database
search_employee -- searches for a specific employee using employee birthday
"""
from flask import render_template, redirect, url_for

from models.db_models import db, Department, Employee
from forms.web_forms import CreateDepartmentForm, CreateEmployeeForm, SearchByDateForm,\
     SearchBetweenDatesForm
from logs.web_logger import logger


def new_department():
    """
    Render template with department creation web form.
    On form submit, create a new department item in the database
    and return redirect to department list URL.
    """
    form = CreateDepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data)
        db.session.add(department)
        db.session.commit()
        logger.debug('Creating %s', department)
        return redirect(url_for('show_departments'))
    return render_template("make-department.html", form=form)


def new_employee():
    """
    Render template with employee creation web form.
    On form submit, create a new employee item in the database
    and return redirect to employee list URL.
    """
    form = CreateEmployeeForm()
    form.department_id.choices = [(d.id, d.name) for d in Department.query.order_by('name')]
    if form.validate_on_submit():
        employee = Employee(
            name=form.name.data,
            salary=form.salary.data,
            birthday=form.birthday.data,
            department_id=form.department_id.data
        )
        db.session.add(employee)
        db.session.commit()
        logger.debug('Creating %s', employee)
        return redirect(url_for('show_employees'))
    return render_template("make-employee.html", form=form)


def show_departments():
    """Return template with department list URL."""
    all_departments = Department.query.all()
    logger.debug('Getting all departments')
    return render_template('departments.html', departments=all_departments)


def show_department(department_id):
    """
    Return template with a specific department URL.

    Parameter:
    department_id(int) -- unique id of a department item
    """
    requested_department = Department.query.filter_by(id=department_id).first()
    logger.debug('Getting %s', requested_department)
    return render_template('department.html', department=requested_department)


def show_employees():
    """Return template with employee list URL."""
    all_employees = Employee.query.all()
    logger.debug('Getting all employees')
    return render_template('employees.html', employees=all_employees)


def show_employee(employee_id):
    """
    Return template with a specific employee URL.

    Parameter:
    employee_id(int) -- unique id of an employee item
    """
    requested_employee = Employee.query.filter_by(id=employee_id).first()
    logger.debug('Getting %s', requested_employee)
    return render_template('employee.html', employee=requested_employee)


def edit_department(department_id):
    """
    Render template with department creation web form based on department id.
    On form submit, update a department item in the database
    and return redirect to updated department URL.

    Parameter:
    department_id(int) -- unique id of a department item
    """
    department = Department.query.get(department_id)
    edit_form = CreateDepartmentForm(name=department.name)
    if edit_form.validate_on_submit():
        department.name = edit_form.name.data
        db.session.commit()
        logger.debug('Updating %s', department)
        return redirect(url_for('show_department', department_id=department.id))
    return render_template(
        'make-department.html',
        form=edit_form,
        is_edit=True,
        department_id=department_id
    )


def edit_employee(employee_id):
    """
    Render template with employee creation web form based on employee id.
    On form submit, update an employee item in the database
    and return redirect to updated employee URL.

    Parameter:
    employee_id(int) -- unique id of an employee item
    """
    employee = Employee.query.get(employee_id)
    edit_form = CreateEmployeeForm(
        name=employee.name,
        salary=employee.salary,
        birthday=employee.birthday,
        department_id=employee.department_id
    )
    edit_form.department_id.choices = [(d.id, d.name) for d in Department.query.order_by('name')]
    if edit_form.validate_on_submit():
        employee.name = edit_form.name.data
        employee.salary = edit_form.salary.data
        employee.birthday = edit_form.birthday.data
        employee.department_id = edit_form.department_id.data
        db.session.commit()
        logger.debug('Updating %s', employee)
        return redirect(url_for('show_employee', employee_id=employee.id))
    return render_template(
        'make-employee.html',
        form=edit_form,
        is_edit=True,
        employee_id=employee_id
    )


def delete_department(department_id):
    """
    Delete a department item from the database using department id.
    Return redirect to department list URL.

    Parameter:
    department_id(int) -- unique id of a department item
    """
    department_to_delete = Department.query.get(department_id)
    db.session.delete(department_to_delete)
    db.session.commit()
    logger.debug('Deleting %s', department_to_delete)
    return redirect(url_for('show_departments'))


def delete_employee(employee_id):
    """
    Delete an employee item from the database using employee id.
    Return redirect to employee list URL.

    Parameter:
    employee_id(int) -- unique id of an employee item
    """
    employee_to_delete = Employee.query.get(employee_id)
    db.session.delete(employee_to_delete)
    db.session.commit()
    logger.debug('Deleting %s', employee_to_delete)
    return redirect(url_for('show_employees'))


def search_employee():
    """
    Render template with employee search by birthday web forms.
    On form submit, return search results
    and render template with these results displayed.
    """
    search_by_date_form = SearchByDateForm()
    search_between_dates_form = SearchBetweenDatesForm()
    if search_by_date_form.validate_on_submit():
        results = Employee.query.filter_by(birthday=search_by_date_form.query_date.data).all()
        logger.debug('Searching employee by birthday')
        return render_template(
            'search.html',
            first_form=search_by_date_form,
            second_form=search_between_dates_form,
            results=results
        )
    if search_between_dates_form.validate_on_submit():
        results = Employee.query.filter(
            Employee.birthday <= search_between_dates_form.query_date_two.data). \
            filter(Employee.birthday >= search_between_dates_form.query_date_one.data)
        logger.debug('Searching employee by birthday')
        return render_template(
            'search.html',
            first_form=search_by_date_form,
            second_form=search_between_dates_form,
            results=results
        )
    return render_template(
        'search.html',
        first_form=search_by_date_form,
        second_form=search_between_dates_form
    )
