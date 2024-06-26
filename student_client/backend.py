"""
Handle Data Processing Here.
Automatically log the student in with their ID from data file.

Upload the ratings from the student to the server.

    - Git pull the students.json
    - Read and rewrite to students.json once updated student data
    - Git push to students.json
"""
import git
from git import Repo

import json


#Open the student json file
with open('student_client/data/student_data.json', 'r') as f:
    student_data = json.load(f)

#check whether the student is logged in by seeing if student id is not null
logged_in = True if student_data['ID'] != None else False

#Pull the git repo

def valid_student_id(student_id):
    if not student_id:
        return False
    #run id through the database of all students and check if it exists

    return True