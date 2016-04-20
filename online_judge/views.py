import os
from . import app
from flask import render_template, request, redirect, session, url_for, flash, jsonify
from models import User, Problem, Solution, ResultCodes
from models import TestCaseFileType
from forms import RegistrationForm, ProblemForm
import controllers as ctrl
from controllers.db_helpers import get_db_session, insert_to_db
import controllers.file_operations as file_op
import controllers.execution


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        return redirect(url_for('practice'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            db_session = get_db_session()
            user = db_session.query(User).filter_by(id=username).one()
            db_session.close()
            if user.password == password:
                session['username'] = username
                return redirect(url_for('practice'))
            else:
                raise
        except Exception as e:
            flash('Invalid Credentials')
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(csrf_enabled=False)
    if request.method == 'POST' and form.validate():
        user = User()
        user.id = form.id.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.password = form.password.data
        user.email = form.email.data
        user.contact_no = form.contact_no.data
        user.branch = form.branch.data
        user.profile_type = request.form['profile_type']
        profile_pic = request.files['profile_pic']

        if profile_pic:
            profile_pic_extension = ctrl.get_extension_of_file(profile_pic.filename)
            user.profile_pic_extension = profile_pic_extension
            file_op.save_profile_pic(profile_pic, user.id)

        if user.profile_type != 'P':
            ctrl.mkdir_p(os.path.join(app.config['SOLUTION_FILES_DEST'], user.id))
        user.is_active = 'Y'

        db_session = get_db_session()
        insert_to_db(db_session, user)
        return render_template('forms/registration_success.html')
    return render_template('forms/register.html', form=form)


@app.route('/add_problem', methods=['GET', 'POST'])
def add_problem():
    problem_form = ProblemForm(csrf_enabled=False)
    if request.method == 'POST':
        problem = Problem(
            title=problem_form.problem_title.data,
            statement=problem_form.problem_statement.data,
            constraints=problem_form.constraints.data,
            time_limit=problem_form.time_limit.data,
            sample_input=problem_form.sample_input.data,
            sample_output=problem_form.sample_output.data,
            difficulty_level=problem_form.difficulty_level.data,
            category=problem_form.category.data,
            successful_submission=0,
            attempts=0,
            input_format=problem_form.input_format.data,
            output_format=problem_form.output_format.data,
            explanation=problem_form.explanation.data
        )

        db_session = get_db_session()
        db_session.add(problem)
        db_session.commit()
        problem_id = problem.id
        db_session.close()

        file_op.save_test_cases(problem_form.input_test_case_file.data, problem_id,
                                TestCaseFileType.INPUT)
        file_op.save_test_cases(problem_form.output_test_case_file.data, problem_id,
                                TestCaseFileType.OUTPUT)
    return render_template('forms/add_problem.html', form=problem_form)


@app.route('/practice')
def practice():
    user_id = session['username']
    db_session = get_db_session()
    user = db_session.query(User).filter_by(id=user_id).one()
    problems = db_session.query(Problem).all()
    db_session.close()
    return render_template('student/practice.html', user=user, problems=problems)


@app.route('/practice/<problem_id>')
def problem_solving(problem_id):
    # TODO secure location for saving source code files
    user_id = session['username']
    db_session = get_db_session()
    user = db_session.query(User).filter_by(id=user_id).one()
    problem = db_session.query(Problem).filter_by(id=problem_id).one()
    db_session.close()
    return render_template('student/problem.html', user=user, problem=problem)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/_get_result', methods=['POST'])
def get_result():
    solution_code = request.form['code']
    code_lang = request.form['code_lang']
    user_id = request.form['user_id']
    problem_id = request.form['problem_id']
    result, exec_time = controllers.execution.start(solution_code, user_id, code_lang, problem_id)
    return jsonify(result=result, time=exec_time)


@app.route('/dashboard')
def dashboard():
    user_id = session['username']
    user = get_db_session().query(User).filter_by(id=user_id).one()

    problem_solved_ids = \
        get_db_session().query(Solution) \
            .filter_by(user_id=user_id, result_code=ResultCodes.CORRECT_ANSWER) \
            .distinct(Solution.problem_id) \
            .with_entities(Solution.problem_id).all()

    problem_attempted = get_db_session().query(Solution).filter_by(user_id=user_id) \
        .distinct(Solution.problem_id).with_entities(Solution.problem_id).count()

    problem_wrong_ans =get_db_session().query(Solution) \
            .filter_by(user_id=user_id, result_code=ResultCodes.WRONG_ANSWER).count()

    problem_correct_ans = get_db_session().query(Solution) \
        .filter_by(user_id=user_id, result_code=ResultCodes.CORRECT_ANSWER).count()

    problem_tle = get_db_session().query(Solution) \
        .filter_by(user_id=user_id, result_code=ResultCodes.TIME_LIMIT_EXCEED).count()

    problem_compile_err = get_db_session().query(Solution) \
        .filter_by(user_id=user_id, result_code=ResultCodes.COMPILE_ERROR).count()

    return render_template('student/dashboard.html',
                           user=user,
                           problem_solved_ids=problem_solved_ids,
                           problem_attempted=problem_attempted,
                           problem_correct_ans=problem_correct_ans,
                           problem_wrong_ans=problem_wrong_ans,
                           problem_tle=problem_tle,
                           problem_compile_err=problem_compile_err)
