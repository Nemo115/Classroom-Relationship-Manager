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
            pass
        else:
            LoginScreen(self)

"""
This will display if user is not logged in (based on backend)
"""
class LoginScreen(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0.2, rely=0.2, relwidth=0.8, relheight=0.8)
        self.pack(fill=BOTH)

        self.student_id = ttk.StringVar(value="")

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

        if not valid_student_id(student_id): #referring to backend to check student id
            toast = ToastNotification(
                title="Submission Error",
                message="Must Enter a student ID",
                duration = 3000
            )
            toast.show_toast()
        else:
            print(student_id)