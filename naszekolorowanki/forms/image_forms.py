from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, FileField, SubmitField, RadioField, BooleanField
from wtforms.validators import DataRequired


class ImageForm(FlaskForm):
    username = StringField('Twoje imię lub pseudonim', validators=[DataRequired(message='Wypełnij to pole.')])
    image = FileField("Wybierz obrazek", validators=[FileAllowed(["jpg", "jpeg", "png"], "Tylko obrazki."), DataRequired(message="Dodaj obrazek")])
    description = StringField('Twój opis', render_kw={"placeholder": "Możesz wpisać nazwę kolorowanki, stosowaną technikę."})
    submit = SubmitField('Dodaj obrazek')


class EditImageForm(FlaskForm):
    username = StringField('Autor')
    description = StringField('Opis autora')
    info = StringField('Nasze informacje')
    status = BooleanField(label='Zaakceptowane')
    submit = SubmitField('Zatwierdź')
