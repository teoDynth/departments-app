from webtest import TestApp

from main import my_app


def before_scenario(context, scenario):
    context.client = TestApp(my_app)


def after_scenario(context, scenario):
    del context.client
