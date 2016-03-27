"""
    Module handling all the form related queries such as validation, creation etc.
    It makes use of wtforms for it's working.
"""

from wtforms import Form, StringField, PasswordField, IntegerField, SelectField
from wtforms import validators, ValidationError
from controllers.db_helpers import db_session
from models import User


def validate_user_id(form, field):
    """
        Perform necessary lookup for user ID to avoid multiple user registering
        with same id.

        Args:
            form (Optional) : form currently being used
            field (Optional) : field which requires check

        Raises:
            ValidationError: if user already registered
    """
    id_query = db_session.query(User).filter_by(id=field.data).all()
    if id_query:
        raise ValidationError('User already exists')


def validate_email(form, field):
    """
        Perform necessary lookup for EMAIL to avoid multiple user registering
        with same email.

        Args:
            form (Optional) : form currently being used
            field (Optional) : field which requires check

        Raises:
            ValidationError: if email already registered
    """
    email_query = db_session.query(User).filter_by(email=field.data).all()
    if email_query:
        raise ValidationError('Email id already registered')


class RegistrationForm(Form):
    """
        Creates registration form for user. It's also responsible for various validation
        check required on each field.

        Attributes:
            id (StringField): string field of registration form
    """
    id = StringField('Registration Number', [validators.required("*required"),
                                             validators.Length(max=20, message="too long"),
                                             validate_user_id])
    first_name = StringField('First Name', [validators.required(message="*required"),
                                            validators.Length(max=20, message="too long")])
    last_name = StringField('Last Name', [validators.Length(max=20, message="too long")])
    password = PasswordField('Password', [validators.required(message="*required"),
                                          validators.Length(min=5, max=20, message="Minimum 5 characters")])
    email = StringField('Email', [validators.required(message='*required'),
                                  validators.Email(message='Please enter valid email id'),
                                  validators.Length(max=50, message="too long"),
                                  validate_email])
    contact_no = IntegerField('Contact No')
    branch = SelectField('Branch', choices=[('1', 'Computer Science and Engineering'),
                                            ('2', 'Software Engineering'),
                                            ('3', 'Information Technology')])
