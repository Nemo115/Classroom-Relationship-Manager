"""
JSON and Data processing Logic will go here

All variables and functions will be called in frontend.py for display

Github Server API: https://github.com/Nemo115/StartHack-2024-PROTOTYPE_SERVER.git
    - Pull the students.json and groups.json from server
    - 
"""
import git
from git import Repo

import json

#Pull the git repo, can comment these two lines for testing
repo = git.Repo("teacher_client/data/StartHack-2024-PROTOTYPE_SERVER")
repo.git.fetch()
repo.git.reset('--hard', 'origin/main')

#Get all students
with open("teacher_client/data/StartHack-2024-PROTOTYPE_SERVER/students.json", 'r') as f:
    student_database = json.load(f)
    print(student_database)
"""
student_database = [{'ID': '0', 'Name': 'John Doe', 'Ratings': {'1': {'rating': 3, 'tags': ['Leader', 'Focused', 'Etc']}, '2': {'rating': 3, 'tags': ['Lazy', 'Distracted', 'Uncooperative']}, '3': {'rating': 5, 'tags': ['Leader', 'Focused', 'Etc']}}}, {'ID': '1', 'Name': 'Robert Redford', 'Ratings': {'0': {'rating': 3, 'tags': ['Leader', 'Focused', 'Etc']}, '2': {'rating': 3, 'tags': ['Lazy', 'Distracted', 'Uncooperative']}, '3': {'rating': 5, 'tags': ['Leader', 'Focused', 'Etc']}}}, {'ID': '2', 'Name': 'Robert Redford', 'Ratings': {'0': {'rating': 3, 'tags': ['SUSSY', 'Focused', 'Etc']}, '1': {'rating': 3, 'tags': ['Lazy', 'Distracted', 'Uncooperative']}, '3': {'rating': 5, 'tags': ['Leader', 'Focused', 'Etc']}}}]
"""
#Get all groups
with open("teacher_client/data/StartHack-2024-PROTOTYPE_SERVER/groups.json", 'r') as f:
    student_groups = json.load(f)
    print(student_groups)


"""
Function:
    - Return Group dictionary from group id
    - Parameters:
        - Group ID
"""
def get_group(id):
    return student_groups[id]


"""
List: a list of classes (list of dictionaries) from classes.json
"""

"""
Function:
    - Return average quality score by adding all elements of a quality list and divide by list length
    - Parameters:
        - Student ID, 
"""

"""
Function: Group Quality Average
    - Return the average total quality score of the group. Only one quality score is returned, not all three
    - Parameters:
        - list of student id's 
        - quality
"""

"""
List: A list of students (list of dictionaries) containing Name, Average score for each quality
"""

"""
Function:
    - Returns total quality percentage out of group
    - Parameters:
        - Group ID
        - Quality
"""


