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
student_database = {'0': {'ID': '0', 'Name': 'John Doe', 'Ratings': {'Collaboration': [1, 2, 3], 'Ideas': [1, 2, 3], 'Leader': [1, 2, 3], 'Teamwork': [1, 2, 3]}}, '1': {'ID': '1', 'Name': 'Robert Redford', 'Ratings': {'Collaboration': [1, 2, 3, 9, 5, 5, 5, 10], 'Dedication': [8, 5, 5, 5, 10], 'Effort': [5, 9, 5, 5, 5, 5, 5, 5, 5, 10], 'Focus': [8, 5, 5, 5, 8], 'Ideas': [1, 2, 3, 5, 5, 5, 5, 5], 'Leader': [1, 2, 3], 'Teamwork': [1, 2, 3]}}, '2': {'ID': '2', 'Name': 'Paul Newman', 'Ratings': {'Collaboration': [6, 5, 5, 0, 5], 'Dedication': [7, 5, 5, 10, 5], 'Effort': [4, 6, 5, 5, 5, 5, 6, 4, 5, 5], 'Focus': [4, 5, 5, 9, 5], 'Ideas': [1, 2, 3, 3, 5, 5, 7, 5], 'Leader': [1, 2, 3], 'Teamwork': [1, 2, 3]}}, '3': {'ID': '3', 'Name': 'Lucy Kent', 'Ratings': {'Effort': [7, 5, 5, 10, 9], 'Focus': [5, 5, 5, 10, 8], 'Ideas': [1, 2, 3, 6, 5, 5, 9, 8], 'Leader': [1, 2, 3], 'Teamwork': [1, 2, 3]}}, '4': {'ID': '4', 'Name': 'Jonathan Davies', 'Ratings': {'Ideas': [1, 2, 3], 'Leader': [1, 2, 3], 'Teamwork': [1, 2, 3]}}}
"""
#Get all groups
with open("teacher_client/data/StartHack-2024-PROTOTYPE_SERVER/groups.json", 'r') as f:
    student_groups = json.load(f)
    print(student_groups)

#Define Variables
current_group = [] # group being worked on
current_group_qualities = [] # qualitites of group being worked on
qualities_options = ["Teamwork", "Leadership", "Focus", "Cooperation", "Communication", 
                     "Humility", "Reliability", "Organisation", "Problem Solving", "Initiative", 
                     "Motivation", "Time Management", "Respect", "Decision Making", "Creativity", 
                     "Constructive Feedback", "Resilience", "Research Skills", "Self Awareness", 
                     "Project Management", "Presentation Skills", "Resource Management", "Perseverance", 
                     "Listening Skills", "Accountability", "Technological Skills", "Effort", "Ideas"]

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
    student_groups[str(new_group_id)] = new_group

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
classes_list = []
with open("teacher_client/data/StartHack-2024-PROTOTYPE_SERVER/classes.json", 'r') as f:
    loaded_classes = json.load(f)
    for key in loaded_classes:
        classes_list.append(loaded_classes[key])
print(classes_list)


"""
Function: Group Quality Average
    - Return the average total quality score of the group. Only one quality score is returned, not all three
    - Parameters:
        - list of student id's 
        - quality
"""
def get_group_quality_average(student_ids_list, quality):
    total_quality_value = 0
    for next_student in student_ids_list:
        student_quality_value = float(0)
        #getting individual student quality value
        for rating in student_database[next_student]["Ratings"][quality]:
            student_quality_value += int(rating)
        student_quality_value = (student_quality_value * 10) / len(student_database[next_student]["Ratings"][quality])
        #adding student quality value to total
        total_quality_value += student_quality_value
        #dividing by number of students
    total_quality_value = total_quality_value / len(student_ids_list)
    
    return total_quality_value
print(get_group_quality_average(["1","2"],"Effort"))


"""
List: A list of students (list of dictionaries) containing Name, Average score for each quality
"""
students_quality_averages = []
for student in student_database:
    #making individual dictinary each
    student_averages = {}
    student_averages["Name"] = student_database[student]["Name"]
    #adding quality average keys
    for quality in student_database[student]["Ratings"]:
        current_quality_total = 0
        #finding quality average
        for next_rating in student_database[student]["Ratings"][quality]:
            current_quality_total += next_rating
        student_averages[quality] = (current_quality_total * 10) / len(student_database[student]["Ratings"][quality])
    students_quality_averages.append(student_averages)
print(students_quality_averages)
    


"""
Function:
    - Returns total quality percentage out of group
    - Parameters:
        - Group ID
        - Quality
"""

