import unittest

from tests import test_create_department, test_update_department, test_delete_department,\
    test_create_employee, test_update_employee, test_delete_employee, test_search_employee,\
    test_page_view

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(test_create_department))
suite.addTests(loader.loadTestsFromModule(test_update_department))
suite.addTests(loader.loadTestsFromModule(test_delete_department))
suite.addTests(loader.loadTestsFromModule(test_create_employee))
suite.addTests(loader.loadTestsFromModule(test_update_employee))
suite.addTests(loader.loadTestsFromModule(test_delete_employee))
suite.addTests(loader.loadTestsFromModule(test_search_employee))
suite.addTests(loader.loadTestsFromModule(test_page_view))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
