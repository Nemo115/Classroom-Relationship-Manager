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

"""
List: a list of classes (list of dictionaries) from classes.json
"""
classes_list = []
with open("teacher_client/data/StartHack-2024-PROTOTYPE_SERVER/classes.json", 'r') as f:
    loaded_classes = json.load(f)
    for key in loaded_classes:
        classes_list.append(loaded_classes[key])
print(classes_list)
print(f"\n\nloaded_classes = {loaded_classes}\n\n")

#Define Variables
current_group = [] # group being worked on
current_group_qualities = [] # qualitites of group being worked on
qualities_options = ["Teamwork", "Leadership", "Focus", "Cooperation", "Communication", 
                     "Humility", "Reliability", "Organisation", "Problem Solving", "Initiative", 
                     "Motivation", "Time Management", "Respect", "Decision Making", "Creativity", 
                     "Constructive Feedback", "Resilience", "Research Skills", "Self Awareness", 
                     "Project Management", "Presentation Skills", "Resource Management", "Perseverance", 
                     "Listening Skills", "Accountability", "Technological Skills", "Effort", "Ideas"]

"""
List: A list of students (list of dictionaries) containing Name, Average score for each quality
"""
students_quality_averages_dict = {}
students_quality_averages_list = []
def find_quality_averages():
    students_quality_averages_dict.clear()
    students_quality_averages_list.clear()
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
            student_averages[quality] = ((current_quality_total * 10) / len(student_database[student]["Ratings"][quality])) if len(student_database[student]["Ratings"][quality]) else 0
        
        students_quality_averages_list.append(student_averages)
        students_quality_averages_dict[student] = student_averages
find_quality_averages()
print(students_quality_averages_list)


def add_group_to_class(class_id, group_id):
    loaded_classes[class_id]['Groups'].append(group_id)

def save_changes():
    with open('teacher_client/data/StartHack-2024-PROTOTYPE_SERVER/students.json', 'w') as f:
        f.write(
            json.dumps(student_database, indent=4, sort_keys=True)
        )
    with open("teacher_client/data/StartHack-2024-PROTOTYPE_SERVER/groups.json", 'w') as f:
        f.write(
            json.dumps(student_groups, indent=4, sort_keys=True)
        )
    with open("teacher_client/data/StartHack-2024-PROTOTYPE_SERVER/classes.json", 'w') as f:
        f.write(
            json.dumps(loaded_classes, indent=4, sort_keys=True)
        )

    #upload to git server
    repo.git.add(update=True)
    repo.index.commit("new commit by Mr Teacher")
    origin = repo.remote(name='origin')
    origin.push()

def create_group(group_name, group_members, group_qualities, class_id):
    #finding new group ID
    new_group_id = 0
    for group in student_groups:
        new_group_id += 1
    #making sure members list input is valid
    if type(group_members) != list: return (False, "group members must be a list")
    for member in group_members:
        if type(member) != str: return (False, "group members must be string type IDs")

        for quality in group_qualities:
            if not (quality in student_database[member]['Ratings']):
                student_database[member]['Ratings'][quality] = []
    #making sure group qualities input is valid
    if type(group_qualities) != list: return (False, "group qualities must be a list")
    for quality in group_qualities:
        if quality not in qualities_options: return (False, ("group quality: " + quality + "not valid"))
    #making new group
    new_group = {
            "GroupID": str(new_group_id),
            "GroupName": group_name,
            "Members": group_members,
            "GroupQualities":group_qualities
        }
    #adding new group to groups list
    student_groups[str(new_group_id)] = new_group

    add_group_to_class(class_id, str(new_group_id))
    find_quality_averages()
    save_changes()

"""
Function:
    - Return Group dictionary from group id
    - Parameters:
        - Group ID
"""
def get_group(id):
    return student_groups[id]

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
        student_quality_value = ((student_quality_value * 10) / len(student_database[next_student]["Ratings"][quality])) if len(student_database[next_student]["Ratings"][quality]) != 0 else 0
        #adding student quality value to total
        total_quality_value += student_quality_value
        #dividing by number of students
    total_quality_value = round(total_quality_value / len(student_ids_list),2)
    
    return total_quality_value
print(get_group_quality_average(["1","2"],"Effort"))

"""
Function:
    - Parameters:
        - Group Dictionary
    - Returns list of tuples: (student name, 1st group quality average, 2nd group quality average, 3rd group quality average)
"""
def row_data(group):
    qualities = group['GroupQualities']

    rows = []
    for student in group['Members']:
        name = students_quality_averages_dict[student]['Name']
        first_quality_avg = round(students_quality_averages_dict[student][qualities[0]], 1)
        second_quality_avg = round(students_quality_averages_dict[student][qualities[1]], 1)
        third_quality_avg = round(students_quality_averages_dict[student][qualities[2]], 1)
        
        new_row = (name, first_quality_avg, second_quality_avg, third_quality_avg)#(name, 1st quality, 2nd quality, 3rd quality)
        rows.append(new_row)
    
    return rows
