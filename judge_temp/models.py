"""
    This module contains different useful models for judge
"""

from sqlalchemy import Column, Integer, String, Text, CHAR, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
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
    """
    __tablename__ = 'user'
    id = Column(String(20), primary_key=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    password = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    contact_no = Column(Integer, nullable=False)
    branch = Column(Integer, nullable=False)
    profile_type = Column(CHAR, nullable=False)
    profile_pic_extension = Column(String)

    # TODO: insert check constraint on profile type

    def __str__(self):
        to_string = "<"
        to_string += " id :" + str(self.id) + ","
        to_string += " first_name :" + str(self.first_name) + ","
        to_string += " last_name :" + str(self.last_name) + ","
        to_string += " password :" + str(self.password) + ","
        to_string += " email :" + str(self.email) + ","
        to_string += " contact_no :" + str(self.contact_no) + ","
        to_string += " branch :" + str(self.branch) + ","
        to_string += " profile_type :" + str(self.profile_type) + ","
        to_string += " profile_pic_extension :" + str(self.profile_pic_extension) + " > "
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
    constraints = Column(String(200), nullable=False)
    time_limit = Column(Integer, nullable=False)
    input_format = Column(Text)
    sample_input = Column(String(200), nullable=False)
    output_format = Column(Text)
    sample_output = Column(String(200), nullable=False)
    explanation = Column(Text)
    difficulty_level = Column(String(30), nullable=False)
    category = Column(String(100), nullable=False)
    attempts = Column(Integer)
    successful_submission = Column(Integer)


class TestCaseFileType(Enum):
    """Enum INPUT, OUTPUT testcase files"""
    INPUT = 1
    OUTPUT = 2


class Solution(Base):
    """
        This model creates a Solution table for each solution that is submitted.
        It'll contains just plain text of solution code submitted by user. It needs
        to be first copied in a file with proper extension and then should be compiled
        or executed.

        Attributes:
            id (Column) : Priamry key of each solution
            solution_code (Column) : code submitted by user. Saved as plain text
            lang_ext (Column) : languange used by user. Stores extension of that languange
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

# Create engine
if __name__ == '__main__':
    engine = create_engine('sqlite:///db/judge_temp.db')
    Base.metadata.create_all(engine)
