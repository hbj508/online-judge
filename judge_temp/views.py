import os
from judge_temp import app
from flask import render_template, request, redirect, session, url_for, flash
from models import User, Problem
from models import TestcaseFileType
from forms import RegistrationForm
import controllers as ctrl
from controllers.dbHelpers import dbSession
import controllers.fileOperations as fileOp
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
            user = dbSession.query(User).filter_by(id=username).one()
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
        id = form.id.data
        firstName = form.firstName.data
        lastName = form.lastName.data
        password = form.password.data
        email = form.email.data
        contactNo = form.contactNo.data
        branch = form.branch.data
        profileType = request.form['profileType']
        profilePic = request.files['profilePic']
        user = User(id=id,
                    firstName=firstName,
                    lastName=lastName,
                    password=password,
                    email=email,
                    contactNo=contactNo,
                    branch=branch,
                    profileType=profileType)
        if profilePic:
            profilePicExtension = ctrl.getExtensionOfFile(profilePic.filename)
            user.profilePicExtension = profilePicExtension
            fileOp.saveProfilePic(profilePic, user.id)
        dbSession.add(user)
        if profileType != 'P':
            ctrl.mkdir_p(os.path.join(app.config['SOLUTION_FILES_DEST'], user.id))
        return render_template('forms/registration_success.html')
    return render_template('forms/register.html', form=form)


@app.route('/addProblem', methods=['GET', 'POST'])
def addProblem():
    # TODO checkout for errors. use try except write unit test
    if request.method == 'POST':
        problem = Problem(title=request.form['title'],
                          statement=request.form['statement'],
                          constraints=request.form['constraints'],
                          timeLimit=request.form['timeLimit'],
                          sampleInput=request.form['sampleInput'],
                          sampleOutput=request.form['sampleOutput'],
                          difficultyLevel=request.form['difficultyLevel'],
                          category=request.form['category'],
                          successfulSubmission=0,
                          attempts=0,
                          inputFormat=request.form['inputFormat'],
                          outputFormat=request.form['outputFormat'],
                          explanation=request.form['explanation'])
        dbSession.add(problem)
        fileOp.saveTestCases(request.files.getlist('inputFiles'), problem.id, TestcaseFileType.INPUT)
        fileOp.saveTestCases(request.files.getlist('outputFiles'), problem.id, TestcaseFileType.OUTPUT)
    return render_template('add_problem.html')


@app.route('/practice')
def practice():
    userId = session['username']
    user = dbSession.query(User).filter_by(id=userId)
    problems = dbSession.query(Problem).all()
    return render_template('practice.html', user=user, problems=problems)


@app.route('/practice/<int:problemId>', methods=['GET', 'POST'])
def problemSolving(problemId):
    # TODO secure location for saving soruce code files
    userId = session['username']
    if request.method == 'POST':
        solutionCode = request.form['code']
        codeLang = request.form['codeLang']
        controllers.execution.start(solutionCode, userId, codeLang, problemId)
    user = dbSession.query(User).filter_by(id=userId).one()
    problem = dbSession.query(Problem).filter_by(id=problemId).one()
    return render_template('problem.html', user=user, problem=problem)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
