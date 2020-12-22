from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, FileField, SubmitField, RadioField, BooleanField
from wtforms.validators import DataRequired


class ImageForm(FlaskForm):
    username = StringField('Your name', validators=[DataRequired(message='This field is required.')])
    image = FileField("Wybierz obrazek", validators=[FileAllowed(["jpg", "jpeg", "png"], "Tylko obrazki.")])
    description = StringField('Twój opis')
    submit = SubmitField('Dodaj obrazek')


class EditImageForm(FlaskForm):
    status = BooleanField(label='Status')
    submit = SubmitField('Zatwierdź')
