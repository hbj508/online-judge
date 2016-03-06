import os

"""
This module is responsible for executing and checking code
"""

def start(userId,codeLang):
    #TODO: improve functionality, try using shell script
    filepath = "~/MyWorkspace/online-judge/judge_temp/static/sourceCodeFiles/" + str(userId)
    shOpenFilePath = "cd " + filepath
    shCompileAndExecute = "javac Solution.java && java Solution > out.txt"
    command = shOpenFilePath +"; " + shCompileAndExecute
    print command
    os.system(command)
