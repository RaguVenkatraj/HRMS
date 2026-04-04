from behave import given, when, then


@given(u'I navigate to the login page')
def step_impl(context):
    context.login_page.launch_url()


@when('I provide credentials "{username}" "{password}"')
def step_impl(context, username, password):
    context.login_page.provide_email_and_password(username, password)


@then('I click on login button')
def step_impl(context):
    context.login_page.click_login()



