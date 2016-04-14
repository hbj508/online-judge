"""
    This module contains different useful models for judge
"""

from sqlalchemy import Column, Integer, String, Text, CHAR, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from enum import Enum

# Construct base class
Base = declarative_base()


class User(Base):
    """
        This model contains various entities for user table.

        Attributes:
            id (Column(String,primary_key)) : contains registration number of each student or professor. It'll work as key for
                                            the relation
            first_name (Column(String))
            last_name (Column(String))
            password (Column(String))
            email(Column(String)) : email id of user. It has Unique contraint applied to it.
            contact_no (Column(String)): contact number of user. It must be an 10 digit mobile no or 11 digit landline with STD
                                      code.
            branch (Column(Integer)) : each integer value corresponds to different branch
                1 -- Computer Science and Engineering
                2 -- Information Technology
                3 -- Software Engineering
            profile_type (Column(CHAR)) : flag to distinguish between professor and student.
            profile_pic_extension (Column(String)): saves extension of profile pic uploaded by user.
            is_active(Column(CHAR)): whether user is active or not
    """
    __tablename__ = 'user'
    id = Column(String(20), primary_key=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20))
    password = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    contact_no = Column(Integer)
    branch = Column(Integer, nullable=False)
    profile_type = Column(CHAR, nullable=False)
    profile_pic_extension = Column(String)
    is_active = Column(CHAR, nullable=False)

    # TODO: insert check constraint on profile type

    def __repr__(self):
        repr_str = "< User ("
        repr_str += " id :" + str(self.id) + ","
        repr_str += " first_name :" + str(self.first_name) + ","
        repr_str += " last_name :" + str(self.last_name) + ","
        repr_str += " password :" + str(self.password) + ","
        repr_str += " email :" + str(self.email) + ","
        repr_str += " contact_no :" + str(self.contact_no) + ","
        repr_str += " branch :" + str(self.branch) + ","
        repr_str += " profile_type :" + str(self.profile_type) + ","
        repr_str += " profile_pic_extension :" + str(self.profile_pic_extension) + " ) > "
        return repr_str

    def __str__(self):
        to_string = str(self.id)
        return to_string


class Problem(Base):
    # TODO: Add problem setter in model
    """
        This model contains various attributes for problem table

        Attributes:
            id (Column(Integer,primary_key)) : id of problem. It'll be automatically incremented
            title (Column(String)) : title of each problem
            statement (Column(Text)) : problem statement
            constraints (Column(String)) : various contraints on inputs
            time_limit (Column(Integer)) : time limit for execution of code
            input_format (Column(String)) : explanation of how input is provided
            sample_input (Column(String)) : sample input for user
            output_format (Column(String)) : explanation of how output should be formatted
            sample_output (Column(String)) : sample output for user
            explanation (Column(Text)) :  explanation of sample output
            difficulty_level (Column(String)) : sets problem difficulty to easy, medium and hard
            category (Column(String)) : different categories of problem DP, Graph, ad-hoc etc
            attempts (Column(Integer)) : no of attempts made by all the user
            successful_submission (Column(Integer)) : no of successful submssion done by all the user

        Note: Output test case Files will be saved separately in /static/output_testcases/
        and will be served as and when necessary. Name of each folder will be equal to
        its id.
    """
    __tablename__ = 'problem'
    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    statement = Column(Text, nullable=False)
    constraints = Column(Text, nullable=False)
    time_limit = Column(Integer, nullable=False)
    input_format = Column(Text)
    sample_input = Column(Text, nullable=False)
    output_format = Column(Text)
    sample_output = Column(Text, nullable=False)
    explanation = Column(Text)
    difficulty_level = Column(String(30), nullable=False)
    category = Column(String(100), nullable=False)
    attempts = Column(Integer)
    successful_submission = Column(Integer)

    def __str__(self):
        return str(self.id)


class TestCaseFileType(Enum):
    """Enum INPUT, OUTPUT test case files"""
    INPUT = 1
    OUTPUT = 2


class Solution(Base):
    """Creates solution table

    This model creates a Solution table for each solution that is submitted.
    It'll contains just plain text of solution code submitted by user. It needs
    to be first copied in a file with proper extension and then should be compiled
    or executed.

    Args:
        id (Column) : Primary key of each solution
        solution_code (Column) : code submitted by user. Saved as plain text
        lang_ext (Column) : language used by user. Stores extension of that languange
        time_of_exec (Column) : (in sec)total time of execution for the selected problem for selected solution
        timestamp (Column) : DateTime timestamp at which particular solution code is submitted
        result_code (Column) : different result codes for solution submitted.
            SE: Server Error
            AC: Accepted Solution
            TLE: Time Limit exceeded
            WA: Wrong answer
            NZEC: Non zero execution code i.e. program didn't finish successfully
        problem_id (Column,Integer,Foreign Key REFERS Problem.id) : id of the problem for which solution is submitted.
            It's a Foreign key representing relation between Solution and Problem table
        user_id (Column, String(20), Foreign Key REFERS User.id) : id of the user who submitted the problem
        user_relation : defines relationship between user and solution table
        problem_relation : defines relationship between problem and solution table
    """
    __tablename__ = 'solution'
    id = Column(Integer, primary_key=True)
    solution_code = Column(Text, nullable=False)
    lang_ext = Column(String(4), nullable=False)
    time_of_exec = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    result_code = Column(String(5), nullable=False)
    problem_id = Column(Integer, ForeignKey('problem.id'), nullable=False)
    user_id = Column(String(20), ForeignKey('user.id'), nullable=False)
    user_relation = relationship('User', backref='user')
    problem_relation = relationship('Problem', backref='problem')


# Create engine
if __name__ == '__main__':
    engine = create_engine('sqlite:///db/judge_temp.db')
    Base.metadata.create_all(engine)
