from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

"""
    This module contains different useful models for judge. Following models are
    created for judge
    1. User - contains various user info including login info
    2. Problem - various problem set
"""

# Construct base clas
Base = declarative_base()

class User(Base):
    """
        This model contains various entities for user such as:
        1. Registration Number - (String, primary key)
        2. First Name
        3. Last Name
        4. Password
        5. Email - (unique)
        6. Contact Number
        7. Branch - (Intger)
            1.CSE
            2.IT
            3.SWE
        8. Profile Type - (P)professior/(S)student
        Note: Profile pictures will be saved separatley in /static/profile_pic_db/
        and will be served as and when necessary. Name of each file will be unique
        i.e. as per their registrationNumber
    """
    __tablename__='user'
    registrationNumber = Column(String(20),primary_key=True)
    firstName = Column(String(20),nullable=False)
    lastName = Column(String(20),nullable=False)
    password = Column(String(20),nullable=False)
    email = Column(String(50),nullable=False,unique=True)
    contactNo = Column(Integer,nullable=False)
    branch = Column(Integer,nullable=False)
    #TODO: insert check constratint on profile type

class Problem(Base):
    """
        This model contains various entities for user such as:
        1. id - (Integer, primary key
        2. Title
        3. Statement
        4. Constraints
        5. Sample Input
        6. Sample Output
        7. difficultyLevel
        8. category: DP, Graph, Ad-Hoc etc.
        9. attempt
        10 successfulSubmission
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
    sampleInput = Column(String(200),nullable=False)
    sampleOutput = Column(String(200),nullable=False)
    difficultyLevel = Column(String(30),nullable=False)
    category = Column(String(100),nullable=False)
    attempts = Column(Integer)
    successfulSubmission = Column(Integer)


# Create engine
if __name__ == '__main__':
    # engine = create_engine(app.config['DB_URI'])
    # TODO: change url to static. find how to do it.
    engine = create_engine('sqlite:///db/judge_temp.db')
    Base.metadata.create_all(engine)
