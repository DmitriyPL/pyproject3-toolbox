import re

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from wtforms.fields.html5 import TelField, EmailField


PASSWORD_MIN_LENGTH = 8
NAME_MIN_LENGTH = 2
PHONE_MIN_LENGTH = 6
PHONE_MAX_LENGTH = 12


def password_check(form, field):
    msg = "Пароль должен содержать латинские сивмолы в верхнем и нижнем регистре и цифры."

    patern1 = re.compile('[a-z]+')
    patern2 = re.compile('[A-Z]+')
    patern3 = re.compile('\\d+')

    if (not patern1.search(field.data) or
        not patern2.search(field.data) or
        not patern3.search(field.data)):

        raise ValidationError(msg)


class OrderedForm(FlaskForm):

    name = StringField('Ваше Имя',
                       [InputRequired(), Length(message="Имя из одной буквы?? Хм...", min=NAME_MIN_LENGTH)])

    adress = StringField('Адрес', [InputRequired()])

    email = EmailField('Электронная почта', [InputRequired()])

    phone = TelField('Ваш телефон',
                     [InputRequired(),
                      Length(message="Неверная длина номера телефона", min=PHONE_MIN_LENGTH, max=PHONE_MAX_LENGTH)]
                     )

    submit = SubmitField('Оформить заказ')


class LoginForm(FlaskForm):

    email = EmailField('Электронная почта', [InputRequired()])

    password = PasswordField('Пароль', [InputRequired()])

    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):

    email = EmailField('Электронная почта', [InputRequired()])

    password = PasswordField('Пароль',
                             [InputRequired(),
                              Length(min=PASSWORD_MIN_LENGTH, message="Пароль должен быть не менее 8 символов"),
                              EqualTo('confirm_password', message="Пароли не одинаковые"),
                              password_check
                              ]
                             )

    confirm_password = PasswordField('Подтвердить пароль', [InputRequired()])

    submit = SubmitField('Войти')


class ChangePasswordForm(FlaskForm):
    password = PasswordField('Пароль',
                             [
                                 InputRequired(),
                                 Length(min=PASSWORD_MIN_LENGTH, message="Пароль должен быть не менее 8 символов"),
                                 EqualTo('confirm_password', message="Пароли не одинаковые"),
                                 password_check
                             ]
                             )
    confirm_password = PasswordField("Пароль ещё раз")

    submit = SubmitField('Сохранить пароль')
