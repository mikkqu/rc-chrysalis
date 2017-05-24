from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SelectField, SubmitField, StringField
from wtforms import widgets, validators
from wtforms.validators import DataRequired
from . import models

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

goals = [(str(i), x) for i, x in enumerate(models.goals)]

class GoalForm(FlaskForm):
    goals_mcheckbox = MultiCheckboxField('Label', choices=goals)
    person_text = StringField("Choose a person")
    submit_button = SubmitField("Submit")