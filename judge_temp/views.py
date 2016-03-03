from judge_temp import app
from flask import render_template, request
from models import User, Problem
from models import TestcaseFileType

import controllers as ctrl

@app.route('/')
@app.route('/index')
def index():
    return "Hello World"

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        # TODO: enclose this with try catch
        user = User(id=request.form['registrationNumber'],
                    firstName=request.form['firstName'],
                    lastName=request.form['lastName'],
                    password=request.form['password'],
                    email=request.form['email'],
                    contactNo=request.form['contactNo'],
                    branch=request.form['branch'])
        profilePic = request.files['profilePic']
        ctrl.saveProfilePic(profilePic, user.id)
        if profilePic!=None:
            profilePicExtension = ctrl.getExtensionOfFile(profilePic.filename)
        user.profilePicExtension = profilePicExtension
        ctrl.insertToDb(user)
    return render_template('registration_page.html')


@app.route('/addProblem',methods=['GET','POST'])
def addProblem():
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
        ctrl.insertToDb(problem)
        ctrl.saveTestCases(request.files.getlist('inputFiles'),problem.id,TestcaseFileType.INPUT)
        ctrl.saveTestCases(request.files.getlist('outputFiles'),problem.id,TestcaseFileType.OUTPUT)
    return render_template('add_problem.html')


@app.route('/<userId>/practice')
def practice(userId):
    user = ctrl.selectFromDb(User,key=userId)
    problems = ctrl.selectFromDb(Problem)
    return render_template('practice.html',user=user,problems=problems)


@app.route('/<userId>/practice/<int:problemId>')
def problemSolving(userId,problemId):
    user = ctrl.selectFromDb(User,key=userId)
    problem = ctrl.selectFromDb(Problem,key=problemId)
    return render_template('problem.html',user=user,problem=problem)
