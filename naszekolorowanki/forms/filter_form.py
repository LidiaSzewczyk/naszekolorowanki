from flask_wtf import FlaskForm
from wtforms import StringField


class FilterForm(FlaskForm):
    search = StringField(label='Szukaj', render_kw={"placeholder": "Szukaj"})
