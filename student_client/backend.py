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
repo.git.fetch()
repo.git.reset('--hard', 'origin/main')
#repo.git.merge('origin/main')
#repo.git.pull()

#Get all students
with open("student_client/data/StartHack-2024-PROTOTYPE_SERVER/students.json", 'r') as f:
    student_database = json.load(f)
    print(student_database)
"""
student_database = [{'ID': '0', 'Name': 'John Doe', 'Ratings': {'1': {'rating': 3, 'tags': ['Leader', 'Focused', 'Etc']}, '2': {'rating': 3, 'tags': ['Lazy', 'Distracted', 'Uncooperative']}, '3': {'rating': 5, 'tags': ['Leader', 'Focused', 'Etc']}}}, {'ID': '1', 'Name': 'Robert Redford', 'Ratings': {'0': {'rating': 3, 'tags': ['Leader', 'Focused', 'Etc']}, '2': {'rating': 3, 'tags': ['Lazy', 'Distracted', 'Uncooperative']}, '3': {'rating': 5, 'tags': ['Leader', 'Focused', 'Etc']}}}, {'ID': '2', 'Name': 'Robert Redford', 'Ratings': {'0': {'rating': 3, 'tags': ['SUSSY', 'Focused', 'Etc']}, '1': {'rating': 3, 'tags': ['Lazy', 'Distracted', 'Uncooperative']}, '3': {'rating': 5, 'tags': ['Leader', 'Focused', 'Etc']}}}]
"""
#Get all groups
with open("student_client/data/StartHack-2024-PROTOTYPE_SERVER/groups.json", 'r') as f:
    student_groups = json.load(f)['groups']
    print(student_groups)

current_groups = [] # every group the student is in
current_group_qualities = []
current_peers = [] #every peer the student must rate and their corresponding groups
current_ratings = {} # ratings to be dumped to json. Format: {'0': {'Ratings': {'1': {'Effort': 4, 'Focus': 2, 'Ideas': 1}, '2': {'Effort': 4, 'Focus': 2, 'Ideas': 1}, '3': {'Effort': 4, 'Focus': 2, 'Ideas': 1}}, '2': {'Ratings': {'1': {'Effort': 2, 'Dedication': 2, 'Collaboration': 2}, '2': {'Effort': 2, 'Dedication': 2, 'Collaboration': 2}}}}}}, {'ID': '2', 'Name': 'Lucy Kent', 'Groups': {'0': {'Ratings': {'1': {'Effort': 4, 'Focus': 2, 'Ideas': 1}, '2': {'Effort': 4, 'Focus': 2, 'Ideas': 1}, '3': {'Effort': 4, 'Focus': 2, 'Ideas': 1}}, '2': {'Ratings': {'1': {'Effort': 2, 'Dedication': 2, 'Collaboration': 2}, '2': {'Effort': 2, 'Dedication': 2, 'Collaboration': 2}}}}}}, {'ID': '3', 'Name': 'Luke Belfort', 'Groups': {'0': {'Ratings': {'1': {'Effort': 4, 'Focus': 2, 'Ideas': 1}, '2': {'Effort': 4, 'Focus': 2, 'Ideas': 1}, '3': {'Effort': 4, 'Focus': 2, 'Ideas': 1}}, '2': {'Ratings': {'1': {'Effort': 2, 'Dedication': 2, 'Collaboration': 2}, '2': {'Effort': 2, 'Dedication': 2, 'Collaboration': 2}}

def valid_student_id(student_id):
    if not student_id:
        return (False, "Must input a Student ID")
    #run id through the database of all students and check if it exists
    
    if student_id in student_database:
        return (True, "Success: You are now Logged In!")            
    
    #student id not found
    return (False, "Error: Student ID not found")

def copy_student(student_id):
    if student_id in student_database:
        student_data.clear()
        student_data['ID'] = student_id
        student_data.update(student_database[student_id])
    #pass values to student_data from student_id
    with open('student_client/data/student_data.json', 'w') as f:
        json.dump(student_data, f)

def get_student(student_id):
    return student_database[student_id]

def get_group(group_id):
    for group in student_groups:
        if group['GroupID'] == group_id:
            return group

def find_group_members(current_peers, current_groups, current_group_qualities):
    #Find the group the student is in
    for group in student_groups:
        if student_data['ID'] in group['Members']:
            current_groups.append(group['GroupID'])
            current_group_qualities.append((group['GroupID'], group['GroupQualities']))
            for member in group['Members']:#add each member to the group list except for self
                if member != student_data['ID']:
                    current_peers.append((group['GroupID'], member))
    
def group_qualities(group):
    #group is the indexed group
    return student_groups[group]['GroupQualities']


"""
This Function puts all the ratings of each group peer into current_ratings dictionary
This is necessary because we need to know what the student rated each peer.
"""
def set_ratings():#reads all the groups and members, and generates default values for ratings
    #cant believe this shit works lmao, my brain hurts so much
    rating_dict = {}#{'0': {'1': {'Effort': 4, 'Focus': 2, 'Ideas': 1}, '2': {'Effort': 4, 'Focus': 2, 'Ideas': 1}, '3': {'Effort': 4, 'Focus': 2, 'Ideas': 1}}, '1': {'1': {'Effort': 2, 'Dedication': 2, 'Collaboration': 2}, '2': {'Effort': 2, 'Dedication': 2, 'Collaboration': 2}}}}, {'ID': '1', 'Name': 'Robert Redford', 'Ratings': {'0': {'1': {'Effort': 4, 'Focus': 2, 'Ideas': 1}, '2': {'Effort': 4, 'Focus': 2, 'Ideas': 1}, '3': {'Effort': 4, 'Focus': 2, 'Ideas': 1}}, '2': {'1': {'Effort': 2, 'Dedication': 2, 'Collaboration': 2}, '2': {'Effort': 2, 'Dedication': 2, 'Collaboration': 2}}
    for group in current_groups:
        rating_dict[group] = {}#{'0':{}}
        for peer in current_peers:
            if group == peer[0]:
                rating_dict[group][peer[1]] = {}
                for qualities in current_group_qualities:
                    if qualities[0] == group:
                        for quality in qualities[1]:
                            rating_dict[group][peer[1]][quality] = 5
    current_ratings.update(rating_dict)
    print(f"current_ratings = {current_ratings}")#{'0': {'1': {'Effort': 0, 'Focus': 0, 'Ideas': 0}, '2': {'Effort': 0, 'Focus': 0, 'Ideas': 0}, '3': {'Effort': 0, 'Focus': 0, 'Ideas': 0}}, '1': {'2': {'Effort': 0, 'Dedication': 0, 'Collaboration': 0}, '1': {'Effort': 0, 'Dedication': 0, 'Collaboration': 0}}}

"""
This Function will read each rating in current_rating, 
and append to quality for each peer

Then dump to JSON and upload it to server.
"""
def upload_ratings():
    """
    Dump JSON
    Student Data = {'ID': '0', 'Name': 'John Doe', 'Ratings': {'0': {'1': {'Effort': 4, 'Focus': 2, 'Ideas': 1}, '2': {'Effort': 4, 'Focus': 2, 'Ideas': 1}, '3': {'Effort': 4, 'Focus': 2, 'Ideas': 1}}, '1': {'1': {'Effort': 2, 'Dedication': 2, 'Collaboration': 2}, '2': {'Effort': 2, 'Dedication': 2, 'Collaboration': 2}}}}
    current_ratings = {'0': {'1': {'Effort': 0, 'Focus': 0, 'Ideas': 0}, '2': {'Effort': 0, 'Focus': 0, 'Ideas': 0}, '3': {'Effort': 0, 'Focus': 0, 'Ideas': 0}}, '1': {'2': {'Effort': 0, 'Dedication': 0, 'Collaboration': 0}, '1': {'Effort': 0, 'Dedication': 0, 'Collaboration': 0}}}
    """

    for group in current_ratings:
        #group = '0'
        rated_peer = current_ratings[group]
        for peer in rated_peer:
            #peer = '1' (student id)
            rated_qualities = rated_peer[peer]
            for quality in rated_qualities:
                #quality = 'Effort'
                rating = rated_qualities[quality]
                if quality in student_database[peer]['Ratings']: # check if student has the quality in their ratings
                    student_database[peer]['Ratings'][quality].append(rating)
                else:# if not, add the quality to their ratings
                    student_database[peer]['Ratings'][quality] = [rating]


    '''
    student_data['Ratings'] = current_ratings
    with open('student_client/data/student_data.json', 'w') as f:
        json.dump(student_data, f)
    print(student_data)
    '''
    """
    student_index = 0
    for student in student_database:
        if student['ID'] == student['ID']:
            student_database[student_index] = student_data
            break
    """
    
    students_json = {"students":student_database}
    with open('student_client/data/StartHack-2024-PROTOTYPE_SERVER/students.json', 'w') as f:
        #json.dump(students_json, f)
        f.write(
            json.dumps(students_json, indent=4, sort_keys=True)
        )
    #upload to git server

    repo.git.add(update=True)
    repo.index.commit(f"new commit by {student_data['Name']}")
    origin = repo.remote(name='origin')
    origin.push()
    