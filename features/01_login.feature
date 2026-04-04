@allure.label.owner=qa_team

Feature: 01. Login Page

  @allure.severity=critical
 Scenario Outline: Login with credentials
  Given I navigate to the login page
  When I provide credentials "<username>" "<password>"
  Then I click on login button

Examples:
  | username            | password   | result      |
  | invalid@example.com | wrongpass  | login_page  |
  | " "                  | admin123   | login_page  |
  | admin@example.com   | " "         | login_page  |
  | rahul.employee@test.com | Employee@123   | dashboard   |