from behave import *


@when(u'I navigate to Departments Page')
def step_impl(ctx):
    ctx.resp = ctx.client.get('/')


@then(u'Departments Page should be displayed')
def step_impl(ctx):
    assert 'Departments' in ctx.resp
