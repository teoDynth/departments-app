from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired


class CreateDepartmentForm(FlaskForm):
    name = StringField(label='New department name:', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


class CreateEmployeeForm(FlaskForm):
    name = StringField(label='Employee name:', validators=[DataRequired()])
    salary = FloatField(label='Employee salary:', validators=[DataRequired()])
    birthday = DateField(label='Employee date of birth:', validators=[DataRequired()])
    department_id = SelectField(label='Choose a department of an employee:', validators=[DataRequired()], coerce=int)
    submit = SubmitField(label='Submit')


class SearchByDateForm(FlaskForm):
    query_date = DateField(label='Search an employee by a certain date of birth:', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


class SearchBetweenDatesForm(FlaskForm):
    query_date_one = DateField(label='Earliest date of birth:', validators=[DataRequired()])
    query_date_two = DateField(label='Latest date of birth:', validators=[DataRequired()])
    submit = SubmitField(label='Submit')
