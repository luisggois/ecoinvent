from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField
from wtforms.validators import Required


class SearchForm(FlaskForm):
    choices = [('version', 'Version'), ('model', 'Model'), ('activity_name', 'Activity'),
               ('geography_name', 'Geography'), ('reference_product_name', 'Reference Product')]
    field = SelectField(choices=choices, validators=[Required()])
    value = StringField(validators=[Required()])
    search = SubmitField('Search')
