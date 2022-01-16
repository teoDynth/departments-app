from flask_restful import reqparse, abort, inputs, Resource


parser = reqparse.RequestParser()
parser.add_argument('department', help='Department name')
parser.add_argument('employee', help='Employee name')
parser.add_argument('salary', type=float, help='Employee salary')
parser.add_argument('birthday', type=inputs.date, help='Employee birthday')
parser.add_argument('department_id', type=int, help='Employee department id')


def get_departments():
    dep_dict = {}
    from models.db_models import Department
    all_departments = Department.query.all()
    for d in all_departments:
        dep = {d.id: {'department': d.name}}
        dep_dict.update(dep)
    return dep_dict


def get_employees():
    emp_dict = {}
    from models.db_models import Employee
    all_employees = Employee.query.all()
    for e in all_employees:
        emp = {e.id: {'employee': e.name, 'salary': f'{e.salary}',
                      'birthday': f'{e.birthday.year}/{e.birthday.month}/{e.birthday.day}',
                      'department': e.department.name}}
        emp_dict.update(emp)
    return emp_dict


def abort_if_department_doesnt_exist(department_id):
    all_departments = get_departments()
    if department_id not in all_departments:
        abort(404, message=f"Department {department_id} doesn't exist")


def abort_if_employee_doesnt_exist(employee_id):
    all_employees = get_employees()
    if employee_id not in all_employees:
        abort(404, message=f"Employee {employee_id} doesn't exist")


class DepartmentList(Resource):
    def get(self):
        return get_departments()

    def post(self):
        from models.db_models import db, Department
        args = parser.parse_args(strict=True)
        department = Department(name=args['department'])
        db.session.add(department)
        db.session.commit()
        return get_departments(), 201


class EmployeeList(Resource):
    def get(self):
        return get_employees()

    def post(self):
        from models.db_models import db, Employee
        args = parser.parse_args(strict=True)
        employee = Employee(
            name=args['employee'],
            salary=args['salary'],
            birthday=args['birthday'],
            department_id=args['department_id']
        )
        db.session.add(employee)
        db.session.commit()
        return get_employees(), 201


class Department(Resource):
    def get(self, department_id):
        abort_if_department_doesnt_exist(department_id)
        all_departments = get_departments()
        return all_departments[department_id]

    def delete(self, department_id):
        from models.db_models import db, Department
        abort_if_department_doesnt_exist(department_id)
        department_to_delete = Department.query.get(department_id)
        db.session.delete(department_to_delete)
        db.session.commit()
        return '', 204

    def put(self, department_id):
        from models.db_models import db, Department
        args = parser.parse_args(strict=True)
        department = Department.query.get(department_id)
        department.name = args['department']
        db.session.commit()
        all_departments = get_departments()
        return all_departments[department_id], 201


class Employee(Resource):
    def get(self, employee_id):
        abort_if_employee_doesnt_exist(employee_id)
        all_employees = get_employees()
        return all_employees[employee_id]

    def delete(self, employee_id):
        from models.db_models import db, Employee
        employee_to_delete = Employee.query.get(employee_id)
        db.session.delete(employee_to_delete)
        db.session.commit()
        return '', 204

    def put(self, employee_id):
        from models.db_models import db, Employee
        args = parser.parse_args(strict=True)
        employee = Employee.query.get(employee_id)
        employee.name = args['employee']
        employee.salary = args['salary']
        employee.birthday = args['birthday']
        employee.department_id = args['department_id']
        db.session.commit()
        all_employees = get_employees()
        return all_employees[employee_id], 201
