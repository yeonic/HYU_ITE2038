from typing import Dict
from PyInquirer import prompt

initial_q = [{
    "type": "list",
    "name": "initial_task",
    "message": "Welcome to DummyTube. Choose your task",
    "choices": ["Sign up", "Sign in", "Quit"]
}]

signin_q = [{
    "type": "input",
    "name": "email",
    "message": "Type your email."
}, {
    "type": "password",
    "name": "password",
    "message": "Type your password."
}]

signup_q = [{
    "type": "input",
    "name": "name",
    "message": "Type your name."
}, {
    "type": "input",
    "name": "email",
    "message": "Type your email."
}, {
    "type": "input",
    "name": "password",
    "message": "Type your password."
}, {
    "type": "input",
    "name": "mobile phone",
    "message": "Type your phone number with hyphen. (ex 010-1234-3333)"
}]


def initial_seq(services: Dict):
    answers = prompt(initial_q)
    q_name = "initial_task"
    user_service = services["userService"]

    if answers.get(q_name) == 'Quit':
        print('Bye, bye')
        return 0

    if answers.get(q_name) == 'Sign up':
        answers2 = prompt(signup_q)

        res = user_service.sign_up(
            email=answers2.get("email"),
            password=answers2.get("password"),
            name=answers2.get("name"),
            pnum=answers2.get("mobile phone")
        )

        # if insertion failed, return to initial seq
        if res == 0:
            initial_seq(services)

        print('signed up successfully.')
        initial_seq(services)

    if answers.get(q_name) == "Sign in":
        answers3 = prompt(signin_q)

        res = user_service.sign_in(
            email=answers3.get("email"),
            password=answers3.get("password")
        )

        # if login failed, return to initial seq
        if res == 0:
            initial_seq(services)

        print('logged in successfully.')
        return int(res)

