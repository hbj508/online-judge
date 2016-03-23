import os
import filecmp
import datetime
from .. import app
import dbOperations as dbOp
from ..models import Solution
from subprocess import Popen, PIPE

"""
This module is responsible for executing and checking code
"""

def start(solutionCode,userId,codeLang,problemId):
    _createSolution(solutionCode, userId, codeLang, problemId)

def _createSolution(solutionCode,userId,codeLang,problemId):
    """
        Creates instance of Solution model for storing solution code

        Args:
            solutionCode (str) :  complete source code submitted by user
            userId (str) : registration number of user of submitted the code
            codeLang (str) : extension of code langauange file
            problemId (int) : id of problem for which solution is submitted

        Note: Solution Model also contains more attributes which will be initliazed
        with some default values.
    """
    solution = Solution(solutionCode = solutionCode,
                    languangeExt = codeLang,
                    timeOfExecution = 0,
                    timestamp=datetime.datetime.now(),
                    resultCode = 'SE',
                    userId = userId,
                    problemId = problemId)
    dbOp.insertToDb(solution)
    _generate_output_file(solution)


def _get_solution_details(solutionId):
    """
        Retrieves solution base on their Id

        Args:
            solutionId(int) : id of the solution to retreive
        Returns:
            solution(Solution): solution row obtained from the database
    """
    session = get_session()
    solution = session.query(Solution).filter_by(id=solutionId).one()
    return solution


def _generate_solution_file(solution):
    """
        Generates solution file for execution

        Args:
            solution(Solution) : row of Solution model obtianed from query
    """
    solution_directory = os.path.join(app.config['SOLUTION_FILES_DEST'],solution.userId)
    solution_file_name = "Solution." + solution.languangeExt
    solution_path = os.path.join(solution_directory,solution_file_name)
    with open(solution_path,'w') as solution_file:
        solution_file.write(solution.solutionCode)
    return solution_path, solution_directory

def _generate_output_file(solution):
    command = ""
    solution_file_path, solution_directory =  _generate_solution_file(solution)
    print solution_file_path + " " + solution_directory
    output_file_path = os.path.join(solution_directory,"out.txt")
    if solution.languangeExt == 'java':
        command = " javac " +  solution_file_path + " && java -cp " + sol + " Solution \
                    > " + output_file_path
    elif solution.languangeExt == 'c':
        command = " gcc " + solution_file_path + " && ./a.out \
                    > " + output_file_path
    elif solution.languangeExt == 'cpp':
        command = " g++ " + solution_file_path + " && ./a.out \
                    > " + output_file_path

    process = Popen(command,shell=True,stderr=PIPE)
    error = process.stderr.read();
    print "MyERROR---------------"
    print error
