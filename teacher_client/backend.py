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


#Define Variables
current_group = [] # group being worked on
current_group_qualities = [] # qualitites of group being worked on
qualities_options = ["Teamwork", "Leadership", "Focus", "Cooperation", "Communication", 
                     "Humility", "Reliability", "Organisation", "Problem Solving", "Initiative", 
                     "Motivation", "Time Management", "Respect", "Decision Making", "Creativity", 
                     "Constructive Feedback", "Resilience", "Research Skills", "Self Awareness", 
                     "Project Management", "Presentation Skills", "Resource Management", "Perseverance", 
                     "Listening Skills", "Accountability", "Technological Skills", "Effort", "Ideas"]

    #Are we doing a login page for the teachers?

# def valid_teacher_id(teacher_id):
#     if not teacher_id:
#         return (False, "Must input a Teacher ID")
#     #run id through the database of all teachers and check if it exists?
    
#     for teacher in teacher_database:
#         if teacher['ID'] == teacher_id:
#             #logged_in = True
#             return (True, "Success: You are now Logged In!")
    
#     #Teacher id not found
#     return (False, "Error: Teacher ID not found")

def create_group(group_name, group_members, group_qualities):
    #finding new group ID
    new_group_id = 0
    for group in student_groups:
        new_group_id += 1
    #making sure members list input is valid
    if type(group_members) != list: return (False, "group members must be a list")
    for member in group_members:
        if type(member) != str: return (False, "group members must be string type IDs")
    #making sure group qualities input is valid
    if type(group_qualities) != list: return (False, "group qualities must be a list")
    for quality in group_qualities:
        if quality not in qualities_options: return (False, ("group quality: " + quality + "not valid"))
    #making new group
    new_group = {
            "GroupID": new_group_id,
            "GroupName": group_name,
            "Members": group_members,
            "GroupQualities":group_qualities
        }
    #adding new group to groups list
    student_groups.append(new_group)