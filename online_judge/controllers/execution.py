import datetime
import os
from subprocess32 import PIPE, TimeoutExpired, check_output, STDOUT, CalledProcessError
from psutil import Popen
import filecmp
from db_helpers import get_db_session, insert_to_db
from .. import app
from ..models import Solution, ResultCodes, Problem

"""
This module is responsible for executing and checking code
"""


def start(solution_code, user_id, code_lang, problem_id):
    return _create_solution(solution_code, user_id, code_lang, problem_id)


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
    problem = db_session.query(Problem).filter_by(id=problem_id).one()
    problem.attempts += 1
    execution_time = _generate_output_file(solution, problem)
    result = solution.result_code
    if result == ResultCodes.CORRECT_ANSWER:
        problem.successful_submission += 1
    insert_to_db(db_session, solution, dont_close_session=True)
    insert_to_db(db_session, problem)
    return result, execution_time


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


def _generate_output_file(solution, problem):
    command = ""
    solution_file_path, solution_directory = _generate_solution_file(solution)
    output_file_path = os.path.join(solution_directory, "out.txt")
    test_case_dir = app.config['TEST_CASE_FILES_DEST']
    # TODO: try for any alternative of shell=True
    try:
        time_limit = int(problem.time_limit)

        if solution.lang_ext == 'java':
            time_limit *= 2
            compile_command = " javac " + solution_file_path
            command = "timeout " + str(
                time_limit) + " java -cp '" + solution_directory + "' " + " < " + test_case_dir + "/" + str(
                problem.id) + "/inputs/in.txt " + " Solution > " + output_file_path
        elif solution.lang_ext == 'c':
            compile_command = " gcc -o " + " < " + test_case_dir + "/" + str(
                problem.id) + "/inputs/in.txt " + solution_directory + "/Solution " + solution_file_path
            command = "timeout " + str(time_limit) + " " + solution_directory + "/Solution > " + output_file_path
        elif solution.lang_ext == 'cpp':
            compile_command = "g++ -o " + " < " + test_case_dir + "/" + str(
                problem.id) + "/inputs/in.txt " + solution_directory + "/Solution " + solution_file_path
            command = "timeout " + str(time_limit) + " " + solution_directory + "/Solution > " + output_file_path

        # print command
        # print compile_command
        check_output(compile_command, shell=True, stderr=STDOUT)
        process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        resource_usage = os.wait4(process.pid, 0)
        # print execution_times
        execution_time = resource_usage[2].ru_utime + resource_usage[2].ru_stime
        returncode = resource_usage[1]
        error = process.stderr.read()
        if returncode == 124:
            raise TimeoutExpired(command, timeout=time_limit, output=str(stderr))
        if error != '':
            raise CalledProcessError(process.returncode, command, output=str(error))

        user_output_file_path = os.path.join(app.config['SOLUTION_FILES_DEST'],
                                             solution.user_id, 'out.txt')
        output_test_file_path = os.path.join(app.config['TEST_CASE_FILES_DEST'],
                                             solution.problem_id, 'outputs',
                                             'out.txt')
        compare_files = filecmp.cmp(user_output_file_path,
                                    output_test_file_path)
        if compare_files:
            solution.result_code = ResultCodes.CORRECT_ANSWER
        else:
            solution.result_code = ResultCodes.WRONG_ANSWER
    except TimeoutExpired as e:
        solution.result_code = ResultCodes.TIME_LIMIT_EXCEED
        execution_time = time_limit + 0.001
    except CalledProcessError as c:
        solution.result_code = ResultCodes.COMPILE_ERROR
        execution_time = 0.0
        output = c.output
        if solution.lang_ext == "java":
            if output[0] != "E":
                output = output.split("Solution.java")[-1]
        elif solution.lang_ext == "c":
            output = output.split("Solution.c")[-1]
        elif solution.lang_ext == "cpp":
            output = output.split("Solution.cpp")[-1]
        output = "Line:" + output
        return "{0:.3f}".format(execution_time), output

    return "{0:.3f}".format(execution_time)
