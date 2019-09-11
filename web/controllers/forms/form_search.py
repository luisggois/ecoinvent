from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    choices = [('version', 'Version'), ('model', 'Model'), ('activity_name', 'Activity'),
               ('geography_name', 'Geography'), ('reference_product_name', 'Reference Product')]
    field = SelectField(choices=choices, validators=[DataRequired()])
    value = StringField(validators=[DataRequired()])
    search = SubmitField('Search')
