from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,BooleanField
from wtforms.validators import Required

class CategoryForm(FlaskForm):
    category = TextAreaField('Enter Pitch')
    submit = SubmitField('Submit')


class ContentForm(FlaskForm):
    pitch = TextAreaField('Pitch')
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment')
    submit = SubmitField('Submit')

class PitchForm(FlaskForm):
    content = TextAreaField('Pitch', validators=[Required()])
    submit = SubmitField('Submit')


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.', validators=[Required()])
    submit = SubmitField('Submit')
