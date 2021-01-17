from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError

from naszekolorowanki.models.user_models import User


class LoginForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired(message='To pole jest wymagane.')])
    password = PasswordField('Hasło', validators=[DataRequired(message='To pole jest wymagane.'), Length(min=8,
                                                                                                         message='Długość hasła to min 8 znaków.')])
    remember_me = BooleanField('Nie wylogowuj')
    submit = SubmitField('Zaloguj się')


class SignUpForm(FlaskForm):
    username = StringField('Nazwa użytkownika',
                           validators=[DataRequired(message='To pole jest wymagane.'), Length(3, 80),
                                       Regexp('^[A-Za-z0-9_]{3,}$',
                                              message='Nazwa  użytkownika składa się z liter, cyfr, podkreśleń.')])
    password = PasswordField('Hasło', validators=[DataRequired(message='To pole jest wymagane.'),
                                                  Length(min=8, message='Długość hasła to min 8 znaków.'),
                                                  EqualTo('password2', message='Hasło musi pasować.')])
    password2 = PasswordField('Potwierdź hasło', validators=[DataRequired(message='To pole jest wymagane.')])
    submit = SubmitField('Zarejestruj')

    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('Ta nazwa użytkownika już jest zajęta.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Obecne hasło',
                                 validators=[DataRequired(message='To pole jest wymagane.')])

    new_password = PasswordField('Nowe hasło', validators=[DataRequired(message='To pole jest wymagane.'),
                                                           Length(min=8,
                                                                  message='Długość hasła to min 8 znaków.'),
                                                           EqualTo('new_password2', message='Hasło musi pasować.')])
    new_password2 = PasswordField('Potwierdź nowe hasło', validators=[DataRequired(message='To pole jest wymagane.')
                                                                      ])
    submit = SubmitField('Zatwierdź')

    def validate_old_password(self, password):
        user = User.query.filter_by(username=current_user.username).first_or_404()
        if not user.check_password(password.data):
            raise ValidationError('Nieprawidłowe hasło')


class DeleteUserForm(FlaskForm):
    password = PasswordField('Hasło', validators=[DataRequired(message='To pole jest wymagane.'), Length(min=8,
                                                                                                         message='Długość hasła to min 8 znaków.')])
    submit = SubmitField('Skasuj Twoje konto')

    @staticmethod
    def validate_password(self, password):
        user = User.query.filter_by(username=current_user.username).first_or_404()
        if not user.check_password(password.data):
            raise ValidationError('Nieprawidłowe hasło')
