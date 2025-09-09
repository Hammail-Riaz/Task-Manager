from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Regexp

class CreateTaskForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[DataRequired()],
        render_kw={
            "placeholder" : "Enter task title here"
        }
        )
    description = TextAreaField(
        "Description",
        validators=[DataRequired()],
        render_kw={
            "placeholder" : "Enter task title here"
        }
        )
    status = SelectField(
        "Task Status",
        choices=[
            ("Completed" , "Completed"), 
            ('Pending', "Pending"),
            ('In Progress' , "In Progress"),
            ('Cancelled', "Cancelled")
        ], 
        default="Pending", 
        validators=[DataRequired()]
        )
    
    submit = SubmitField("Create  Task")
    
class EditTaskForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[DataRequired()]
        )
    description = TextAreaField(
        "Description",
        validators=[DataRequired()]
        )
    
    status = SelectField(
        "Task Status",
        choices=[
            ("Completed" , "Completed"), 
            ('Pending', "Pending"),
            ('In Progress' , "In Progress"),
            ('Cancelled', "Cancelled")
        ], 
        default="pending", 
        validators=[DataRequired()]
        )
    
    submit = SubmitField("Made Changes")


class DeleteTaskForm(FlaskForm):
    submit = SubmitField("Delete")
