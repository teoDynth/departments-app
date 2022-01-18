"""
Module with Python classes describing DB models. Contains the following classes -

Classes:
Employee -- describes employee item database model
Department -- describes department item database model
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Employee(db.Model):
    """A SQLAlchemy database model class describing an employee item"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.Float(50), nullable=False)
    birthday = db.Column(db.Date, nullable=False)

    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    department = db.relationship(
        'Department',
        backref=db.backref('employees', lazy=True, cascade='all,delete')
    )

    def __repr__(self):
        return f'<Employee {self.name!r}>'


class Department(db.Model):
    """A SQLAlchemy database model class describing a department item"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Department {self.name!r}>'

