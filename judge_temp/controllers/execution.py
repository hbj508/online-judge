import os
import filecmp

"""
This module is responsible for executing and checking code
"""

def start(userId,codeLang,problemId):
    #TODO: improve functionality, try using shell script
    filepath = "~/MyWorkspace/online-judge/judge_temp/static/sourceCodeFiles/" + str(userId)
    shOpenFilePath = "cd " + filepath
    inputFile = '/home/gahan/MyWorkspace/online-judge/judge_temp/static/testcaseFiles/'+str(problemId)+'/inputs/in1.txt'
    shCompileAndExecute = "javac Solution.java && java Solution <" + inputFile + "> out.txt"
    command = shOpenFilePath +"; " + shCompileAndExecute
    print command
    os.system(command)
    print "now checking the code"
    sampleOutput = '/home/gahan/MyWorkspace/online-judge/judge_temp/static/testcaseFiles/'+str(problemId)+'/outputs/out1.txt'
    output= '/home/gahan/MyWorkspace/online-judge/judge_temp/static/sourceCodeFiles/'+ str(userId) +'/out.txt'
    if filecmp.cmp(output, sampleOutput):
        return 'True'
    else:
        return 'False'
