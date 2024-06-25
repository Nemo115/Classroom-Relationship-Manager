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
        
        default_label = ttk.Label(self, text="This is a test label", width = 50)
        default_label.pack(fill=X, pady=10)
        
        #Draw the Groupviewer
        self.group_viewer = GroupViewer(self)


"""
This is the group viewer.
Includes: 
    - Notebook (tabs and pages)
"""
class GroupViewer(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0.2, rely=0.2, relwidth=0.8, relheight=0.8)
        self.pack(fill=BOTH)
        
        self.create_notebook()
        self.add_notebook_tabs()

        self.create_new_group_tab()
    
    def create_notebook(self):
        self.notebook = ttk.Notebook(self, bootstyle = "dark")
        self.notebook.pack(pady=20, padx=10, fill=BOTH)
    
    def add_notebook_tabs(self):
        new_tab = GroupTab(self, label_text="first tab text\ngroup 1")
        self.notebook.add(new_tab, text = "group 1")

        new_tab_2 = GroupTab(self, label_text="second tab text\ngroup 2")
        self.notebook.add(new_tab_2, text = "group 2")
    
    def create_new_group_tab(self):
        new_group_tab = NewGroupTab(self)
        self.notebook.add(new_group_tab, text="Create New Group")

"""
This is the pages displayed for each tab in the group viewer.
Should include: 
    - Calculated compatibility/collaborative percentage
    - List of students in the current group and the corresponding data.
"""
class GroupTab(ttk.Frame):
    def __init__(self, parent, label_text):
        super().__init__(parent)
        self.data = []

        self.create_meter(0.5)
        self.table = self.create_table()
        label = ttk.Label(self, text = label_text, font=("Helvetica", 18))
        label.pack(expand=True, fill='both', padx=20,pady=20)
        self.pack()

    #Create meter
    def create_meter(self, percentage):
        meter = ttk.Meter(
            master = self,
            metersize=150,
            padding=5,
            amounttotal=100,
            amountused = percentage * 100,# INSERT PERCENTAGE HERE (multiply by 100 if like 0.25 etc)
            metertype=FULL,
            subtext="Collaborative Percentage",
            interactive= True
        )
        meter.pack()
    
    def create_table(self):
        headers = [
            {"text": "Name", "stretch": True},
            {"text": "Student ID", "stretch": True},
            {"text": "Total Rating", "stretch": True}
        ]
        table = Tableview(
            master=self,
            coldata= headers,
            rowdata= self.data,
            paginated=True,
            searchable=True,#Searchbar
            bootstyle=PRIMARY,
            stripecolor=('green', None)
        )

        table.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        return table

class NewGroupTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        placeholder = ttk.Label(self, text="Create a new group here", width = 50)
        placeholder.pack(fill=X, pady=10)
        self.pack()
