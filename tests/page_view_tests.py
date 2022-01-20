"""
Module with unittest classes used for testing page viewing. Contains following classes:

Classes:
GeneralPagesViewTest -- tests general view URLs, not requiring a database item id
IndividualPagesViewTests -- tests individual view URls, requiring a database item id
"""
import unittest


class GeneralPagesViewTest(unittest.TestCase):
    """A Test Case class for viewing general URLs."""
    def setUp(self):
        from main import my_app
        self.app = my_app.test_client()
        self.app.testing = True

    def test_view_pages(self):
        departments = self.app.get('/')
        departments_departments = self.app.get('/departments')
        new_department = self.app.get('/new-department')
        employees = self.app.get('/employees')
        search = self.app.get('/search-employee')
        new_employee = self.app.get('/new-employee')
        self.assertIn('Departments', str(departments.data))
        self.assertIn('Departments', str(departments_departments.data))
        self.assertIn('New Department', str(new_department.data))
        self.assertIn('Employees', str(employees.data))
        self.assertIn('Search an employee by birthday', str(search.data))
        self.assertIn('New employee information', str(new_employee.data))


class IndividualPagesViewTests(unittest.TestCase):
    """A Test Case class for viewing individual URLs."""
    def setUp(self):
        from main import my_app
        self.app = my_app.test_client()
        self.app.testing = True

    def test_individual_view_pages(self):
        department = self.app.get('/departments/1')
        edit_department = self.app.get('/edit-department/1')
        employee = self.app.get('/employees/1')
        edit_employee = self.app.get('/edit-employee/1')
        self.assertIn('Average department salary', str(department.data))
        self.assertIn('Edit Department', str(edit_department.data))
        self.assertIn('Salary', str(employee.data))
        self.assertIn('Edit employee information', str(edit_employee.data))


if __name__ == "__main__":
    unittest.main()
