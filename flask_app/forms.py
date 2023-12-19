from ast import Pass
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectField
from wtforms.validators import (
    InputRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
)


from .models import User


class SearchForm(FlaskForm):
    search_query = StringField(
        "Query", validators=[InputRequired(), Length(min=1, max=100)]
    )
    submit = SubmitField("Search")


# class MovieReviewForm(FlaskForm):
#     text = TextAreaField(
#         "Comment", validators=[InputRequired(), Length(min=5, max=500)]
#     )
#     submit = SubmitField("Enter Comment")

class CarReviewForm(FlaskForm):
    text = TextAreaField(
        "Comment", validators=[InputRequired(), Length(min=5, max=500)]
    )
    submit = SubmitField("Enter Comment")


class CarRatingForm(FlaskForm):
    rating = SelectField("Rating", choices=[(1, '1 star'), (2, '2 star'), (3, '3 star'), (4, '4 star'), (5, '5 star')],
                         coerce=int, validators=[InputRequired()])
    submit = SubmitField("Enter Rating")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")


# TODO: implement fields
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=40)])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField('Login')


# TODO: implement
class UpdateUsernameForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=40)])
    submit_username =SubmitField('Submit_Username')

    # TODO: implement
    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

# TODO: implement
class UpdateProfilePicForm(FlaskForm):
    picture = FileField('Picture', validators=[FileRequired(), FileAllowed(['jpg', 'png'], "Images Only!")])
    submit_picture = SubmitField('Submit_Picture')
