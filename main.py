from flask import Flask
from flask_bootstrap import Bootstrap
from flask_restful import reqparse, abort, Api, Resource
from service import web_service
from flask_migrate import Migrate
from models.db_models import db, Employee
from rest import restful_departments

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.secret_key = "12345678"
    Bootstrap(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///department.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)
    return app


my_app = create_app()
my_app.app_context().push()
api = Api(my_app)


@my_app.context_processor
def utility_processor():
    def calculate_average_salary(department):
        average_salary = 0
        if len(department.employees) == 0:
            return average_salary
        else:
            for employee in department.employees:
                average_salary += employee.salary
            return average_salary / len(department.employees)

    return dict(calculate_average_salary=calculate_average_salary)


my_app.add_url_rule('/', view_func=web_service.show_departments)
my_app.add_url_rule('/departments', view_func=web_service.show_departments)
my_app.add_url_rule('/departments/<int:department_id>', view_func=web_service.show_department)
my_app.add_url_rule('/employees', view_func=web_service.show_employees)
my_app.add_url_rule('/employees/<int:employee_id>', view_func=web_service.show_employee)
my_app.add_url_rule('/new-department', methods=['POST', 'GET'], view_func=web_service.new_department)
my_app.add_url_rule('/edit-department/<int:department_id>', methods=['POST', 'GET'],
                    view_func=web_service.edit_department)
my_app.add_url_rule('/delete-department/<int:department_id>', view_func=web_service.delete_department)
my_app.add_url_rule('/new-employee', methods=['POST', 'GET'], view_func=web_service.new_employee)
my_app.add_url_rule('/edit-employee/<int:employee_id>', methods=['POST', 'GET'], view_func=web_service.edit_employee)
my_app.add_url_rule('/delete-employee/<int:employee_id>', view_func=web_service.delete_employee)
my_app.add_url_rule('/search-employee', methods=['POST', 'GET'], view_func=web_service.search_employee)

api.add_resource(restful_departments.DepartmentList, '/api/departments')
api.add_resource(restful_departments.EmployeeList, '/api/employees')
api.add_resource(restful_departments.Department, '/api/departments/<int:department_id>')
api.add_resource(restful_departments.Employee, '/api/employees/<int:employee_id>')


if __name__ == '__main__':
    my_app.run(debug=True)
