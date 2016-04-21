from wtforms import validators, ValidationError
from flask.ext.wtf import Form
from flask.ext.wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, IntegerField, SelectField, TextAreaField, SubmitField
from controllers.db_helpers import get_db_session
from controllers.file_operations import profile_pics
from models import User

"""
    Module handling all the form related queries such as validation, creation etc.
    It makes use of wtforms and Flask-WTF packages for it's working.
"""


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
    db_session = get_db_session()
    id_query = db_session.query(User).filter_by(id=field.data).all()
    db_session.close()
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
    db_session = get_db_session()
    email_query = db_session.query(User).filter_by(email=field.data).all()
    db_session.close()
    if email_query:
        raise ValidationError('Email id already registered')


class RegistrationForm(Form):
    """Creates Registration form for user

    WTForms creates registration form. It's also responsible for various validation
    check required on each field.

    Args:
        id (StringField) : registration number of the user.
        first_name (StringField) : first name of user
        last_name (StringField) : last name of user
        password (StringField) : must be of min_len=5 and max_len=20
        email (StringField): email_id of user. It'll be unique throughout the db
        contact_no (IntegerField) : contact no of user
        branch (SelectField):
            option available are:
            (1) Computer science,
            (2) Software Engineering,
            (3) Information Technology
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


class ProblemForm(Form):
    problem_title = StringField('Problem Title:*', [validators.required("*required")])
    problem_statement = TextAreaField('Problem Statement:*', [validators.required("*required")])
    input_format = TextAreaField('Input Format:*', [validators.required("*required")])
    output_format = TextAreaField('Output Format:*', [validators.required("*required")])
    constraints = TextAreaField('Constratints:*', [validators.required("*required")])
    time_limit = IntegerField('Time Limit (in sec.):*', [validators.required("*required")])
    sample_input = TextAreaField('Sample Input:*', [validators.required("*required")])
    sample_output = TextAreaField('Sample Output:*', [validators.required("*required")])
    explanation = TextAreaField('Explanation')
    difficulty_level = StringField('Difficulty Level:*', [validators.required("*required")])
    category = StringField('Category:*', [validators.required("*required")])
    input_test_case_file = FileField('Input Test Case File', validators=[FileRequired()])
    output_test_case_file = FileField('Output Test case File', validators=[FileRequired()])
    submit = SubmitField('Submit')


class ProfileForm(Form):
    first_name = StringField('First Name', [validators.Length(max=20, message="too long")])
    last_name = StringField('Last Name', [validators.Length(max=20, message="too long")])
    password = PasswordField('Password', [validators.Length(min=5, max=20, message="Minimum 5 characters")])
    contact_no = IntegerField('Contact No')
    profile_pic = FileField(validators=[FileRequired(),FileAllowed(profile_pics,
                                                                   message="Only image files")])
