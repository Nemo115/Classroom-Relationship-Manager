from backend import *

from PIL import Image
Image.CUBIC = Image.BICUBIC

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.validation import add_regex_validation

"""
This is the main frame in the window.
All visual objects will be initialized here.
"""
class App(ttk.Frame):
    def __init__(self, master_window):
        super().__init__(master_window, padding=(20, 10))
        self.pack(fill=BOTH, expand=YES)
        
        default_label = ttk.Label(self, text="This is a test label for main window", width = 50)
        default_label.pack(fill=X, pady=10)

        #Check whether student is logged in
        if logged_in:
            RatingPage(self, master_window)
        else:
            LoginScreen(self, master_window)

"""
This will display if user is not logged in (based on backend)
"""
class LoginScreen(ttk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        self.place(relx=0.2, rely=0.2, relwidth=0.8, relheight=0.8)
        self.pack(fill=BOTH)

        self.student_id = ttk.StringVar(value="")
        self.parent = parent
        self.root = root

        default_label = ttk.Label(self, text="Login Screen", width = 50)
        default_label.pack(fill=X, pady=10)

        #Put an entry box for student id
        id_entry = ttk.Entry(master=self, textvariable=self.student_id, width = 20)
        id_entry.pack(padx=20, fill=X, expand=YES)

        #Submit Button
        submit_btn = ttk.Button(master=self, text="Submit", command=self.submit_id, bootstyle=SUCCESS, width=10)
        submit_btn.pack(padx=5,pady=10)
    
    def submit_id(self):
        student_id = self.student_id.get()
        login_status = valid_student_id(student_id)

        logged_in = login_status[0]
        message = login_status[1]

        if not logged_in: #referring to backend to check student id
            toast = ToastNotification(
                title="Submission Error",
                message=message,
                duration = 3000
            )
            toast.show_toast()
        else:
            print(f"Success {student_id}")
            toast = ToastNotification(
                title="Submission Success",
                message=message,
                duration = 3000
            )
            toast.show_toast()

            #update the student id
            copy_student(student_id)

            #change the page
            self.destroy()
            RatingPage(self.parent, self.root)

class RatingPage(ttk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        self.place(relx=0.2, rely=0.2, relwidth=0.8, relheight=0.8)
        self.pack(fill=BOTH, anchor=CENTER)

        find_group_members(current_peers, current_groups, current_group_qualities)
        set_ratings()
        print(f"\n\ncurrent_peers = {current_peers}")

        self.root = root
        default_label = ttk.Label(self, text="Rating Page", width = 50)
        default_label.pack(fill=X, pady=10)
        
        """
        Label: How would you rate working with {INSERT NAME}
        Frame: 
            - Slider (1 to 5)
            - 
        Two buttons on the bottom, progress bar in middle to indicate index of group member: -[]--- (2/5)
        """
        self.current_peer_index = 0 #start on first peer in group
        self.current_peer_message = ttk.StringVar(value=f"How would you rate working with {self.current_peer()['Name']} in {self.current_group()['GroupName']}")# Value is updated in self.update_current_message()

        self.title = self.create_title()

        #Draw the rating stuff for the current peer
        self.peer_element = self.create_current_peer()

        self.bottom_buttons = self.create_buttons()
    
    def create_current_peer(self):
        peer_elem = RatePeerElement(self, self.current_peer(), self.current_group())
        return peer_elem

    def next_peer(self):
        if self.current_peer_index + 1 >= 0 and self.current_peer_index + 1 < len(current_peers):
            self.current_peer_index += 1
            self.refresh_elements()
            print(f"next peer clicked: {self.current_peer_index} {self.current_peer_message.get()}")
        
        if self.current_peer_index == len(current_peers) - 1:#On Last Page
            self.bottom_buttons.destroy()
            self.bottom_buttons = self.create_last_page_bottom()
        
    def previous_peer(self):
        if self.current_peer_index - 1 >= 0 and self.current_peer_index - 1 < len(current_peers):
            self.current_peer_index -= 1
            self.refresh_elements()
            print(f"prior peer clicked: {self.current_peer_index} {self.current_peer_message.get()}")
        
        #if self.current_peer_index == len(current_peers) - 2:#Exited Last Page
        #    self.bottom_buttons.destroy()
        #    self.bottom_buttons = self.create_buttons()

    def refresh_elements(self):
        self.update_current_message()
        self.peer_element.update_current_ratings()
        self.peer_element.destroy()
        self.peer_element = self.create_current_peer()
        self.bottom_buttons.destroy()
        self.bottom_buttons = self.create_buttons()


    def current_peer(self):
        return get_student(current_peers[self.current_peer_index][1])

    def current_group(self):
        return get_group(current_peers[self.current_peer_index][0])

    def update_current_message(self):# Updates the title text
        self.current_peer_message.set(f"How would you rate working with {self.current_peer()['Name']} in {self.current_group()['GroupName']}")

    def create_title(self):
        title = ttk.Label(self, textvariable=self.current_peer_message, width=50)
        title.pack(padx=10, pady=10, anchor=CENTER, fill = X)
        return title
        
    def create_group_index_slider(self):
        pass
    
    def create_buttons(self):
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=20)
        
        previous_peer_btn = ttk.Button(
            master = container,
            text="Previous Peer",
            command = self.previous_peer,
            bootstyle=INFO,
            width=15
        )
        previous_peer_btn.pack(side=LEFT, padx=5)
        
        next_peer_btn=ttk.Button(
            master = container,
            text="Next Peer",
            command = self.next_peer,
            bootstyle=INFO,
            width=15
        )
        next_peer_btn.pack(side=RIGHT, padx=5)

        return container
    def create_last_page_bottom(self):
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=20)
        
        previous_peer_btn = ttk.Button(
            master = container,
            text="Previous Peer",
            command = self.previous_peer,
            bootstyle=INFO,
            width=15
        )
        previous_peer_btn.pack(side=LEFT, padx=5)
        
        submit_btn=ttk.Button(
            master = container,
            text="Submit",
            command = self.submit_ratings,
            bootstyle=SUCCESS,
            width=15
        )
        submit_btn.pack(side=RIGHT, padx=5)

        return container
    def create_exit_button(self):
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=20)
        
        exit_btn = ttk.Button(
            master = container,
            text="Exit",
            command = self.root.destroy,
            bootstyle=DANGER,
            width=15
        )
        exit_btn.pack(side=BOTTOM, padx=5)
        return container
    
    def submit_ratings(self):
        upload_ratings()
        toast = ToastNotification(
            title="Ratings Submitted!",
            message="Your ratings have been uploaded!",
            duration = 3000
        )
        toast.show_toast()
        self.bottom_buttons.destroy()
        self.peer_element.destroy()
        self.bottom_buttons = self.create_exit_button()
        self.peer_element = RatingFinished(self)

class RatePeerElement(ttk.Frame):
    def __init__(self, parent, student, group):
        super().__init__(parent)
        self.place(relx=0.2, rely=0.2, relwidth=0.8, relheight=0.8)
        self.pack(fill=BOTH, anchor=CENTER)

        #Need to get these values from backend.current_ratings
        self.first_quality_rating = ttk.IntVar()
        self.second_quality_rating = ttk.IntVar()
        self.third_quality_rating = ttk.IntVar()

        self.student = student
        self.group = group
        self.qualities = group['GroupQualities']
        self.id = student['ID']

        self.create_quality_rating_form(self.qualities[0], self.first_quality_rating)
        self.create_quality_rating_form(self.qualities[1], self.second_quality_rating)
        self.create_quality_rating_form(self.qualities[2], self.third_quality_rating)

        self.get_current_ratings()
        """
        Contains:
            - 3 bars for each group quality
            - Label next to each bar for the group quality name
        """

    def update_current_ratings(self):
        """
        setting values for current_ratings from backend
        """
        current_ratings[self.group['GroupID']][self.id][self.qualities[0]] = self.first_quality_rating.get()
        current_ratings[self.group['GroupID']][self.id][self.qualities[1]] = self.second_quality_rating.get()
        current_ratings[self.group['GroupID']][self.id][self.qualities[2]] = self.third_quality_rating.get()

    def get_current_ratings(self):#{'0': {'1': {'Effort': 0, 'Focus': 0, 'Ideas': 0}, '2': {'Effort': 0, 'Focus': 0, 'Ideas': 0}, '3': {'Effort': 0, 'Focus': 0, 'Ideas': 0}}, '1': {'2': {'Effort': 0, 'Dedication': 0, 'Collaboration': 0}, '1': {'Effort': 0, 'Dedication': 0, 'Collaboration': 0}}}
        self.first_quality_rating.set(current_ratings[self.group['GroupID']][self.id][self.qualities[0]])
        self.second_quality_rating.set(current_ratings[self.group['GroupID']][self.id][self.qualities[1]])
        self.third_quality_rating.set(current_ratings[self.group['GroupID']][self.id][self.qualities[2]])

    def create_quality_rating_form(self, quality, rating_var):
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=20)

        label = ttk.Label(master=container, text=quality, width=15)
        label.pack(side=LEFT, padx = 12)

        slider = ttk.Scale(master=container, from_= 0, to=10, variable=rating_var)
        slider.pack(side=RIGHT, fill=X, padx=15, expand=YES)
    
class RatingFinished(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0.2, rely=0.2, relwidth=0.8, relheight=0.8)
        self.pack(fill=BOTH, anchor=CENTER)

        default_label = ttk.Label(self, text="Ratings have been uploaded!\nThank you!", width = 50)
        default_label.pack(fill=X, pady=10)

