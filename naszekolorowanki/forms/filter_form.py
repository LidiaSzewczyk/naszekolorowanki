from flask_wtf import FlaskForm
from wtforms import StringField, RadioField


class FilterForm(FlaskForm):
    search = StringField(label='Szukaj', render_kw={"placeholder": "Szukaj"})
    # status = RadioField(label='Status', choices=[(True, "Zaakceptowane"), (False, 'Niezaakceptowane')])
