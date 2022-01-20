"""Main file that runs the app."""
import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_restful import Api

from models.db_models import db
from views.web_controller import add_url_rules, add_api_resources

migrate = Migrate()


def create_app():
    """
    Create application using Flask constructor, initialize the use of Flask-Bootstrap,
    initialize the application for the use with the database setup, add application URL rules.
    """
    app = Flask(__name__)
    Bootstrap(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL?sslmode=require'.replace('postgres://', 'postgresql://'),
        'sqlite:///department.db'
    )
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '12345678')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)
    add_url_rules(app)
    return app


my_app = create_app()
my_app.app_context().push()

api = Api(my_app)
add_api_resources(api)


@my_app.context_processor
def utility_processor():
    """Inject a new variable in the context of templates."""
    def calculate_average_salary(department):
        """
        Calculate average department salary.

        Parameter:
        department -- class object of SQLAlchemy database model Department
        """
        average_salary = 0
        if len(department.employees) == 0:
            return average_salary
        for employee in department.employees:
            average_salary += employee.salary
        return average_salary / len(department.employees)
    return dict(calculate_average_salary=calculate_average_salary)


if __name__ == '__main__':
    my_app.run(host='0.0.0.0', port=5000)
