import os
import filecmp
import datetime
import dbOperations as dbOp
from ..models import Solution

"""
This module is responsible for executing and checking code
"""

def start(solutionCode,userId,codeLang,problemId):
    #TODO: improve functionality, try using shell script
    # filepath = "~/MyWorkspace/online-judge/judge_temp/static/sourceCodeFiles/" + str(userId)
    # shOpenFilePath = "cd " + filepath
    # inputFile = '/home/gahan/MyWorkspace/online-judge/judge_temp/static/testcaseFiles/'+str(problemId)+'/inputs/in1.txt'
    # shCompileAndExecute = "javac Solution.java && java Solution <" + inputFile + "> out.txt"
    # command = shOpenFilePath +"; " + shCompileAndExecute
    # print command
    # os.system(command)
    # print "now checking the code"
    # sampleOutput = '/home/gahan/MyWorkspace/online-judge/judge_temp/static/testcaseFiles/'+str(problemId)+'/outputs/out1.txt'
    # output= '/home/gahan/MyWorkspace/online-judge/judge_temp/static/sourceCodeFiles/'+ str(userId) +'/out.txt'
    # if filecmp.cmp(output, sampleOutput):
    #     return 'True'
    # else:
    #     return 'False'
    _createSolution(solutionCode, userId, codeLang, problemId)

def _createSolution(solutionCode,userId,codeLang,problemId):
    try:
        solution = Solution(solutionCode = solutionCode,
                        languangeExt = codeLang,
                        timeOfExecution = 0,
                        timestamp=datetime.datetime.now(),
                        resultCode = 'SE',
                        userId = userId,
                        problemId = problemId)
        dbOp.insertToDb(solution)
        print "success"
    except:
        print "failure"
