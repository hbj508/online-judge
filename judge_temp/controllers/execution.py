import datetime
import os
from subprocess import Popen, PIPE

from db_helpers import get_db_session, insert_to_db
from .. import app
from ..models import Solution

"""
This module is responsible for executing and checking code
"""


def start(solution_code, user_id, code_lang, problem_id):
    _create_solution(solution_code, user_id, code_lang, problem_id)


def _create_solution(solution_code, user_id, code_lang, problem_id):
    """
        Creates instance of Solution model for storing solution code

        Args:
            solution_code (str) :  complete source code submitted by user
            user_id (str) : registration number of user of submitted the code
            code_lang (str) : extension of code language file
            problem_id (int) : id of problem for which solution is submitted

        Note: Solution Model also contains more attributes which will be initialized
        with some default values.
    """
    solution = Solution(solution_code=solution_code,
                        lang_ext=code_lang,
                        time_of_exec=0,
                        timestamp=datetime.datetime.now(),
                        result_code='SE',
                        user_id=user_id,
                        problem_id=problem_id)
    db_session = get_db_session()
    insert_to_db(db_session, solution)
    _generate_output_file(solution)


def _get_solution_details(solution_id):
    """
        Retrieves solution base on their Id

        Args:
            solution_id(int) : id of the solution to receive
        Returns:
            solution(Solution): solution row obtained from the database
    """
    db_session = get_db_session(create_new_instance=True)
    solution = db_session.query(Solution).filter_by(id=solution_id).one()
    db_session.close()
    return solution


def _generate_solution_file(solution):
    """
        Generates solution file for execution

        Args:
            solution(Solution) : row of Solution model obtained from query
        Returns:
            solution_path(str) : string representing path of solution file
            solution_directory(str) : string representing directory of solution
    """
    solution_directory = os.path.join(app.config['SOLUTION_FILES_DEST'], solution.user_id)
    solution_file_name = "Solution." + solution.lang_ext
    solution_path = os.path.join(solution_directory, solution_file_name)
    with open(solution_path, 'w') as solution_file:
        solution_file.write(solution.solution_code)
    return solution_path, solution_directory


def _generate_output_file(solution):
    command = ""
    solution_file_path, solution_directory = _generate_solution_file(solution)
    output_file_path = os.path.join(solution_directory, "out.txt")
    if solution.lang_ext == 'java':
        command = " javac " + solution_file_path + " && java -cp " + solution_directory + " Solution \
                    > " + output_file_path
    elif solution.lang_ext == 'c':
        command = " gcc " + solution_file_path + " && ./a.out \
                    > " + output_file_path
    elif solution.lang_ext == 'cpp':
        command = " g++ " + solution_file_path + " && ./a.out \
                    > " + output_file_path

    # TODO: try for any alternative of shell=True
    process = Popen(command, shell=True, stderr=PIPE)
    error = process.stderr.read()
    # TODO: do some error work
    print "MyERROR---------------"
    print error
