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
            firstName (Column(String))
            lastName (Column(String))
            password (Column(String))
            email(Column(String)) : email id of user. It has Unique contraint applied to it.
            contactNo (Column(String)): contact number of user. It must be an 10 digit mobile no or 11 digit landline with STD
                                      code.
            branch (Column(Integer)) : each integer value corresponds to different branch
                1 -- Computer Science and Engineering
                2 -- Information Technology
                3 -- Software Engineering
            profileType (Column(CHAR)) : flag to distinguish between professor and student.
            profilePicExtension (Column(String)): saves extension of profile pic uploaded by user.
    """
    __tablename__='user'
    id = Column(String(20),primary_key=True)
    firstName = Column(String(20),nullable=False)
    lastName = Column(String(20),nullable=False)
    password = Column(String(20),nullable=False)
    email = Column(String(50),nullable=False,unique=True)
    contactNo = Column(Integer,nullable=False)
    branch = Column(Integer,nullable=False)
    profileType = Column(CHAR,nullable=False)
    profilePicExtension = Column(String)
    #TODO: insert check constratint on profile type


class Problem(Base):
    #TODO: Add problem setter in model
    """
        This model contains various attributes for problem table

        Attributes:
            id (Column(Integer,primary_key)) : id of problem. It'll be automatically incremented
            title (Column(String)) : title of each problem
            statement (Column(Text)) : problem statement
            constraints (Column(String)) : various contraints on inputs
            timeLimit (Column(Integer)) : time limit for execution of code
            inputFormat (Column(String)) : explanation of how input is provided
            sampleInput (Column(String)) : sample input for user
            outputFormat (Column(String)) : explanation of how output should be formatted
            sampleOutput (Column(String)) : sample output for user
            explanation (Column(Text)) :  explanation of sample output
            difficultyLevel (Column(String)) : sets problem difficulty to easy, medium and hard
            category (Column(String)) : different categories of problem DP, Graph, ad-hoc etc
            attempts (Column(Integer)) : no of attempts made by all the user
            successfulSubmission (Column(Integer)) : no of successful submssion done by all the user

        Note: Output Testcase Files will be saved separatley in /static/output_testcases/
        and will be served as and when necessary. Name of each folder will be equal to
        its id.
    """
    __tablename__='problem'
    id = Column(Integer,primary_key=True)
    title = Column(String(80),nullable=False)
    statement = Column(Text,nullable=False)
    constraints = Column(String(200),nullable=False)
    timeLimit = Column(Integer,nullable=False)
    inputFormat= Column(Text)
    sampleInput = Column(String(200),nullable=False)
    outputFormat = Column(Text)
    sampleOutput = Column(String(200),nullable=False)
    explanation = Column(Text)
    difficultyLevel = Column(String(30),nullable=False)
    category = Column(String(100),nullable=False)
    attempts = Column(Integer)
    successfulSubmission = Column(Integer)


class TestcaseFileType(Enum):
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
            id (Column(Integer,primary_key)) : Priamry key of each solution
            solutionCode (Column, Text) : code submitted by user. Saved as plain text
            languangeExt (Column,String(4)) : languange used by user. Stores extension of that languange
            timeOfExecution (Column, Integer) : (in sec)total time of execution for the selected problem for selected solution
            timestamp (Column, Integer) : DateTime timestamp at which particular solution code is submitted
            resultCode (Column, String(10)) : different result codes for solution submitted.
                SE: Server Error
                AC: Accepted Solution
                TLE: Time Limit exceeded
                WA: Wrong answer
                NZEC: Non zero execution code i.e. program didn't finish successfully
            problemId (Column,Integer,Foreign Key REFERS Problem.id) : id of the problem for which solution is submitted.
                It's a Foreign key representing relation between Solution and Problem table
            userId (Column, String(20), Foreign Key REFERS User.id) : id of the user who submitted the problem
    """
    __tablename__ = 'solution'
    id = Column(Integer,primary_key=True)
    solutionCode = Column(Text,nullable=False)
    languangeExt = Column(String(4),nullable=False)
    timeOfExecution = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    resultCode = Column(String(5), nullable=False)
    problemId = Column(Integer, ForeignKey('problem.id'),nullable=False)
    userId = Column(String(20), ForeignKey('user.id'),nullable=False)


# Create engine
if __name__ == '__main__':
    engine = create_engine('sqlite:///db/judge_temp.db')
    Base.metadata.create_all(engine)
