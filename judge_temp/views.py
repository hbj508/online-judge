from judge_temp import app
from flask import render_template, request
from models import User, Problem

import controllers as ctrl

@app.route('/')
@app.route('/index')
def index():
    return "Hello World"

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        # TODO: enclose this with try catch
        user = User(registrationNumber=request.form['registrationNumber'],
                    firstName=request.form['firstName'],
                    lastName=request.form['lastName'],
                    password=request.form['password'],
                    email=request.form['email'],
                    contactNo=request.form['contactNo'],
                    branch=request.form['branch'])
        profilePic = request.files['profilePic']
        ctrl.saveProfilePic(profilePic, user.registrationNumber)
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
                          category=request.form['category'])
        ctrl.insertToDb(problem)
        ctrl.saveTestCases(request.files.getlist('inputFiles'),123,app.config['FILE_INPUT_TESTCASE'])
        ctrl.saveTestCases(request.files.getlist('outputFiles'),123,app.config['FILE_OUTPUT_TESTCASE'])
    return render_template('add_problem.html')
