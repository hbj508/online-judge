import os
from judge_temp import app
from flask import render_template, request, redirect, session, url_for, flash
from models import User, Problem
from models import TestCaseFileType
from forms import RegistrationForm
import controllers as ctrl
from controllers.db_helpers import db_session
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
            user = db_session.query(User).filter_by(id=username).one()
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
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user_id = form.id.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        password = form.password.data
        email = form.email.data
        contact_no = form.contact_no.data
        branch = form.branch.data
        profile_type = request.form['profile_type']
        profile_pic = request.files['profile_pic']
        user = User(id=user_id,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    email=email,
                    contact_no=contact_no,
                    branch=branch,
                    profile_type=profile_type)
        if profile_pic:
            profile_pic_extension = ctrl.get_extension_of_file(profile_pic.filename)
            user.profile_pic_extension = profile_pic_extension
            file_op.save_profile_pic(profile_pic, user.id)
        db_session.add(user)
        if profile_type != 'P':
            ctrl.mkdir_p(os.path.join(app.config['SOLUTION_FILES_DEST'], user.id))
        return render_template('forms/registration_success.html')
    return render_template('forms/register.html', form=form)


@app.route('/add_problem', methods=['GET', 'POST'])
def add_problem():
    # TODO checkout for errors. use try except write unit test
    if request.method == 'POST':
        problem = Problem(title=request.form['title'],
                          statement=request.form['statement'],
                          constraints=request.form['constraints'],
                          time_limit=request.form['time_limit'],
                          sample_input=request.form['sample_input'],
                          sample_output=request.form['sample_output'],
                          difficulty_level=request.form['difficulty_level'],
                          category=request.form['category'],
                          successful_submission=0,
                          attempts=0,
                          input_format=request.form['input_format'],
                          output_format=request.form['output_format'],
                          explanation=request.form['explanation'])
        db_session.add(problem)
        file_op.save_test_cases(request.files.getlist('input_files'), problem.id, TestCaseFileType.INPUT)
        file_op.save_test_cases(request.files.getlist('output_files'), problem.id, TestCaseFileType.OUTPUT)
    return render_template('add_problem.html')


@app.route('/practice')
def practice():
    user_id = session['username']
    user = db_session.query(User).filter_by(id=user_id).one()
    problems = db_session.query(Problem).all()
    return render_template('practice.html', user=user, problems=problems)


@app.route('/practice/<problem_id>', methods=['GET', 'POST'])
def problem_solving(problem_id):
    # TODO secure location for saving source code files
    user_id = session['username']
    if request.method == 'POST':
        solution_code = request.form['code']
        code_lang = request.form['code_lang']
        controllers.execution.start(solution_code, user_id, code_lang, problem_id)
    user = db_session.query(User).filter_by(id=user_id).one()
    problem = db_session.query(Problem).filter_by(id=problem_id).one()
    return render_template('problem.html', user=user, problem=problem)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
