from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, Email, ValidationError

from naszekolorowanki.models.user_models import User


class LoginForm(FlaskForm):
    username = StringField('Your username:', validators=[DataRequired(message='This field is required.')])
    password = PasswordField('Password:', validators=[DataRequired(message='This field is required.'), Length(min=5,
                                                                                                              message='Field must be at least 5 characters long.')])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='This field is required.'), Length(3, 80),
                                                   Regexp('^[A-Za-z0-9_]{3,}$',
                                                          message='Usernames consist of numbers, letters and underscore.')])
    # email = StringField('Email', validators=[DataRequired(message='This field is required.'), Length(1, 120), Email()])
    password = PasswordField('Password', validators=[DataRequired(message='This field is required.'),
                                                     Length(min=5, message='Field must be at least 5 characters long.'),
                                                     EqualTo('password2', message='Password must match.')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(message='This field is required.')])
    submit = SubmitField('Sign up')

    # @staticmethod
    # def validate_email(self, email_field):
    #     if User.query.filter_by(email=email_field.data).first():
    #         raise ValidationError('There already is a user with this email address')

    @staticmethod
    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('This username is already taken.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Current password',
                                 validators=[DataRequired(message='This field is required.')])

    new_password = PasswordField('New password', validators=[DataRequired(message='This field is required.'),
                                                             Length(min=5,
                                                                    message='Field must be at least 5 characters long.'),
                                                             EqualTo('new_password2', message='Password must match.')])
    new_password2 = PasswordField('Confirm new password', validators=[DataRequired(message='This field is required.')
                                                                      ])
    submit = SubmitField('Submit')

    @staticmethod
    def validate_old_password(self, password):
        user = User.query.filter_by(username=current_user.username).first_or_404()
        if not user.check_password(password.data):
            raise ValidationError('Incorrect password')


class DeleteUserForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(message='This field is required.'), Length(min=5,
                                                                                                             message='Field must be at least 5 characters long.')])
    submit = SubmitField('Delete your account')

    @staticmethod
    def validate_password(self, password):
        user = User.query.filter_by(username=current_user.username).first_or_404()
        if not user.check_password(password.data):
            raise ValidationError('Incorrect password')


