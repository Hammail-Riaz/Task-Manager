from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Regexp(r'^[A-Za-z0-9_]+$',
                   message="Letters, numbers, underscores only!"), Length(min=5, max=16)
            ])
    
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, max=16),
            Regexp(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{8,}$",
            message="Password must contain at least 1 uppercase, 1 lowercase, 1 number, 1 special character (including _), and be at least 8 characters long."
            )

            ])
    
    
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            ])
    
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            ])
    
    submit = SubmitField("Login In")