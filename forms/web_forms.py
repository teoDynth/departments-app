"""
Module with Flask Forms used by functions that work with the database. Contains the following classes -

Classes:
CreateDepartmentForm -- creates a web form for adding and editing a department item
CreateEmployeeForm -- creates a web form for adding and editing an employee item
SearchByDateForm -- creates a web form for searching by specific date
SearchBetweenDatesForm -- creates a web form for searching between two specific dates
"""
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired


class CreateDepartmentForm(FlaskForm):
    """A Flask subclass of WTForms Form that creates a web form to add or edit a department item."""
    name = StringField(label='New department name:', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


class CreateEmployeeForm(FlaskForm):
    """A Flask subclass of WTForms Form that creates a web form to add or edit an employee item."""
    name = StringField(label='Employee name:', validators=[DataRequired()])
    salary = FloatField(label='Employee salary:', validators=[DataRequired()])
    birthday = DateField(label='Employee date of birth:', validators=[DataRequired()])
    department_id = SelectField(label='Choose a department of an employee:', validators=[DataRequired()], coerce=int)
    submit = SubmitField(label='Submit')


class SearchByDateForm(FlaskForm):
    """A Flask subclass of WTForms Form that creates a web form to search an employee item by birthday."""
    query_date = DateField(label='Search an employee by a certain date of birth:', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


class SearchBetweenDatesForm(FlaskForm):
    """A Flask subclass of WTForms Form that creates a web form to search an employee item by birthday between dates."""
    query_date_one = DateField(label='Earliest date of birth:', validators=[DataRequired()])
    query_date_two = DateField(label='Latest date of birth:', validators=[DataRequired()])
    submit = SubmitField(label='Submit')
