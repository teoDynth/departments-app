from flask import render_template, redirect, url_for


def new_department():
    from models.db_models import db, Department
    from forms.web_forms import CreateDepartmentForm
    form = CreateDepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data)
        db.session.add(department)
        db.session.commit()
        return redirect(url_for('show_departments'))
    return render_template("make-department.html", form=form)


def new_employee():
    from models.db_models import db, Department, Employee
    from forms.web_forms import CreateEmployeeForm
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
        return redirect(url_for('show_employees'))
    return render_template("make-employee.html", form=form)


def show_departments():
    from models.db_models import Department
    all_departments = Department.query.all()
    return render_template('departments.html', departments=all_departments)


def show_department(department_id):
    from models.db_models import Department
    requested_department = None
    departments = Department.query.all()
    for department in departments:
        if department.id == department_id:
            requested_department = department
    return render_template('department.html', department=requested_department)


def show_employees():
    from models.db_models import Employee
    all_employees = Employee.query.all()
    return render_template('employees.html', employees=all_employees)


def show_employee(employee_id):
    from models.db_models import Department, Employee
    requested_employee = None
    all_employees = Employee.query.all()
    all_departments = Department.query.all()
    for employee in all_employees:
        if employee.id == employee_id:
            requested_employee = employee
    return render_template('employee.html', employee=requested_employee, departments=all_departments)


def edit_department(department_id):
    from forms.web_forms import CreateDepartmentForm
    from models.db_models import db, Department
    department = Department.query.get(department_id)
    edit_form = CreateDepartmentForm(name=department.name)
    if edit_form.validate_on_submit():
        department.name = edit_form.name.data
        db.session.commit()
        return redirect(url_for('show_department', department_id=department.id))
    return render_template('make-department.html', form=edit_form, is_edit=True, department_id=department_id)


def edit_employee(employee_id):
    from forms.web_forms import CreateEmployeeForm
    from models.db_models import db, Department, Employee
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
        return redirect(url_for('show_employee', employee_id=employee.id))
    return render_template('make-employee.html', form=edit_form, is_edit=True, employee_id=employee_id)


def delete_department(department_id):
    from models.db_models import db, Department
    department_to_delete = Department.query.get(department_id)
    db.session.delete(department_to_delete)
    db.session.commit()
    return redirect(url_for('show_departments'))


def delete_employee(employee_id):
    from models.db_models import db, Employee
    employee_to_delete = Employee.query.get(employee_id)
    db.session.delete(employee_to_delete)
    db.session.commit()
    return redirect(url_for('show_employees'))


def search_employee():
    from forms.web_forms import SearchByDateForm, SearchBetweenDatesForm
    from models.db_models import Employee
    search_by_date_form = SearchByDateForm()
    search_between_dates_form = SearchBetweenDatesForm()
    if search_by_date_form.validate_on_submit():
        results = Employee.query.filter_by(birthday=search_by_date_form.query_date.data).all()
        return render_template('search.html', first_form=search_by_date_form, second_form=search_between_dates_form,
                               results=results)
    if search_between_dates_form.validate_on_submit():
        results = Employee.query.filter(Employee.birthday <= search_between_dates_form.query_date_two.data). \
            filter(Employee.birthday >= search_between_dates_form.query_date_one.data)
        return render_template('search.html', first_form=search_by_date_form,
                               second_form=search_between_dates_form, results=results)
    return render_template('search.html', first_form=search_by_date_form, second_form=search_between_dates_form)
