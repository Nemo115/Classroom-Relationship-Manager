"""
Handle Data Processing Here.
Automatically log the student in with their ID from data file.

Upload the ratings from the student to the server.

Github Server API: https://github.com/Nemo115/StartHack-2024-PROTOTYPE_SERVER.git
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

#Pull the git repo, can comment these two lines for testing
repo = git.Repo("student_client/data/StartHack-2024-PROTOTYPE_SERVER")
repo.git.pull()

#Get all students
with open("student_client/data/StartHack-2024-PROTOTYPE_SERVER/students.json", 'r') as f:
    student_database = json.load(f)['students']
    print(student_database)
"""
student_database = [{'ID': '0', 'Name': 'John Doe', 'Ratings': {'1': {'rating': 3, 'tags': ['Leader', 'Focused', 'Etc']}, '2': {'rating': 3, 'tags': ['Lazy', 'Distracted', 'Uncooperative']}, '3': {'rating': 5, 'tags': ['Leader', 'Focused', 'Etc']}}}, {'ID': '1', 'Name': 'Robert Redford', 'Ratings': {'0': {'rating': 3, 'tags': ['Leader', 'Focused', 'Etc']}, '2': {'rating': 3, 'tags': ['Lazy', 'Distracted', 'Uncooperative']}, '3': {'rating': 5, 'tags': ['Leader', 'Focused', 'Etc']}}}, {'ID': '2', 'Name': 'Robert Redford', 'Ratings': {'0': {'rating': 3, 'tags': ['SUSSY', 'Focused', 'Etc']}, '1': {'rating': 3, 'tags': ['Lazy', 'Distracted', 'Uncooperative']}, '3': {'rating': 5, 'tags': ['Leader', 'Focused', 'Etc']}}}]
"""
#Get all groups
with open("student_client/data/StartHack-2024-PROTOTYPE_SERVER/groups.json", 'r') as f:
    student_groups = json.load(f)['groups']
    print(student_groups)

current_groups = [] # every group the student is in

def valid_student_id(student_id):
    if not student_id:
        return (False, "Must input a Student ID")
    #run id through the database of all students and check if it exists
    
    for student in student_database:
        if student['ID'] == student_id:
            #logged_in = True
            return (True, "Success: You are now Logged In!")
    
    #student id not found
    return (False, "Error: Student ID not found")

def copy_student(student_id):
    for student in student_database:
        if student['ID'] == student_id:
            student_data = student
    #pass values to student_data from student_id
    with open('student_client/data/student_data.json', 'w') as f:
        json.dump(student_data, f)

def get_student(student_id):
    for student in student_database:
        if student['ID'] == student_id:
            return student

def get_group(group_id):
    for group in student_groups:
        if group['GroupID'] == group_id:
            return group

def find_group_members(current_groups):
    #Find the group the student is in
    for group in student_groups:
        if student_data['ID'] in group['Members']:
            for member in group['Members']:#add each member to the group list except for self
                if member != student_data['ID']:
                    current_groups.append((group['GroupID'], member))
    
def group_qualities(group):
    #group is the indexed group
    return student_groups[group]['GroupQualities']
