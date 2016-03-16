import os
from judge_temp import app
from flask import render_template, request, redirect, session, url_for
from models import User, Problem
from models import TestcaseFileType
import controllers as ctrl
import controllers.dbOperations as dbOp
import controllers.fileOperations as fileOp
import controllers.execution

@app.route('/',methods=['GET','POST'])
@app.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = dbOp.selectFromDb(User,username)
        print user.password
        print password
        if user.password==password:
            session['username'] = username
            return redirect(url_for('practice'))
    if 'username' in session:
        return redirect(url_for('practice'))
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        # TODO checkout for errors. use try except write unit test
        user = User(id=request.form['registrationNumber'],
                    firstName=request.form['firstName'],
                    lastName=request.form['lastName'],
                    password=request.form['password'],
                    email=request.form['email'],
                    contactNo=request.form['contactNo'],
                    branch=request.form['branch'],
                    profileType='S')
        profilePic = request.files['profilePic']
        if profilePic!=None:
            profilePicExtension = ctrl.getExtensionOfFile(profilePic.filename)
        user.profilePicExtension = profilePicExtension
        fileOp.saveProfilePic(profilePic,user.id)
        dbOp.insertToDb(user)
        ctrl.mkdir_p(os.path.join(app.config['SOURCE_CODE_FILES_DEST'],user.id))
    return render_template('registration_page.html')


@app.route('/addProblem',methods=['GET','POST'])
def addProblem():
    # TODO checkout for errors. use try except write unit test
    if request.method=='POST':
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
        dbOp.insertToDb(problem)
        fileOp.saveTestCases(request.files.getlist('inputFiles'),problem.id,TestcaseFileType.INPUT)
        fileOp.saveTestCases(request.files.getlist('outputFiles'),problem.id,TestcaseFileType.OUTPUT)
    return render_template('add_problem.html')


@app.route('/practice')
def practice():
    userId = session['username']
    user = dbOp.selectFromDb(User,key=userId)
    problems = dbOp.selectFromDb(Problem)
    return render_template('practice.html',user=user,problems=problems)


@app.route('/practice/<int:problemId>', methods=['GET','POST'])
def problemSolving(problemId):
    # TODO secure location for saving soruce code files
    userId = session['username']
    if request.method=='POST':
        sourceCode = request.form['code']
        fileOp.saveSourceCode(sourceCode, 'java', userId, problemId)
        return controllers.execution.start(userId,'java' , problemId)
    user = dbOp.selectFromDb(User,key=userId)
    problem = dbOp.selectFromDb(Problem,key=problemId)
    return render_template('problem.html',user=user,problem=problem)

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))
