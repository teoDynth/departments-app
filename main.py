"""Main file that runs the app."""
import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_restful import Api

from models.db_models import db
from views.web_controller import add_url_rules, add_api_resources
from logs.web_logger import logger

migrate = Migrate()


def create_app():
    """
    Create application using Flask constructor, initialize the use of Flask-Bootstrap,
    initialize the application for the use with the database setup, add URL rules and API resources.
    """
    logger.debug('App creation started')
    app = Flask(__name__)
    api = Api(app)
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
    add_api_resources(api)
    logger.debug('App creation finished')
    return app


my_app = create_app()
my_app.app_context().push()


@my_app.context_processor
def utility_processor():
    """Inject a new variable in the context of templates."""

    def calculate_average_salary(department):
        """
        Calculate average department salary.

        Parameter:
        department -- class object of SQLAlchemy database model Department
        """
        logger.debug('Calculating average salary for %s', department)
        average_salary = 0
        if department.employees:
            for employee in department.employees:
                average_salary += employee.salary
        else:
            logger.debug('%s average salary calculated as %s', department, average_salary)
            return average_salary
        average_salary = average_salary / len(department.employees)
        logger.debug('%s average salary calculated as %s', department, average_salary)
        return average_salary
    return dict(calculate_average_salary=calculate_average_salary)


if __name__ == '__main__':
    logger.debug('Running app')
    os.environ.setdefault('FLASK_ENV', 'development')
    my_app.run(use_reloader=False)
    logger.debug('Closing app')
