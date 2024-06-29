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
        super().__init__(master_window, padding=(0, 10))
        self.pack(fill=BOTH, expand=YES)
        self.root = master_window
        #default_label = ttk.Label(self, text="This is a test label", width = 50)
        #default_label.pack(fill=X, pady=10)

        self.side_menu_x = 0
        self.side_menu_active = True

        self.main_view_x = 300

        #Draw the Groupviewer
        self.navigation_bar = self.create_navigation_bar()
        self.main_view = self.create_main_view()


    def create_main_view(self):
        container = ttk.Frame(self, padding=(20,0))
        container.place(x=self.main_view_x, y=60, relwidth=1-self.get_width_percentage()-.1)#PUT THE CALCULATED WIDTH PERCENTAGE
        GroupViewer(container)

        return container

    def create_navigation_bar(self):
        top_container = ttk.Frame(self)
        top_container.pack(fill=X, side=TOP)
        toggle_button = ttk.Button(
                master = top_container,
                text="Classes Menu",
                command = self.toggle_side_menu,
                bootstyle=INFO,
                width=15
            )
        toggle_button.pack(side=LEFT, padx=5, pady=10)

        side_container = ttk.Frame(self, width=300) #This will push the group viewer to the right side when side_bar_panel is active
        side_container.pack(fill=Y, side=LEFT)

        side_bar_panel = ttk.Frame(self, bootstyle = 'secondary')
        side_bar_panel.place(x=self.side_menu_x, y=60, relheight=1, width=300)

        temp_text = ttk.Label(side_bar_panel, text="This is where the classes go")
        temp_text.pack(anchor=CENTER, pady=400)

        return {"menu":side_bar_panel, "container":side_container}# we must edit both the values of the menu and the container for popping in and out
    
    def toggle_side_menu(self):
        self.side_menu_active = not self.side_menu_active
        if self.side_menu_active:
            #move group viewer
            self.side_bar_enter()
        else:
            #move group viewer
            self.side_bar_exit()
    
    #Side bar pops in, and main view adjusts
    def side_bar_enter(self):
        self.side_menu_x += 20
        self.main_view_x += 20
        if self.side_menu_x <= 0 and self.main_view_x <= 300:
            self.navigation_bar['menu'].place(x=self.side_menu_x)
            self.main_view.place(x=self.main_view_x)
            self.root.after(10, self.side_bar_enter)

    #Side bar pops out, and main view expands
    def side_bar_exit(self):
        self.side_menu_x -= 20
        self.main_view_x -= 20
        if self.side_menu_x >= -300:
            self.navigation_bar['menu'].place(x=self.side_menu_x)
            self.main_view.place(x=self.main_view_x)
            self.root.after(10, self.side_bar_exit)

    def get_width_percentage(self):
        width = self.root.winfo_screenwidth()
        return 300/width


"""
This is the group viewer.
Includes: 
    - Notebook (tabs and pages)
"""
class GroupViewer(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        #self.place(relx=0.2, rely=0.2, relwidth=.8, relheight=1)
        self.pack(fill=BOTH, expand=YES)

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

        self.create_quality_meters()
        self.table = self.create_table()
        label = ttk.Label(self, text = label_text, font=("Helvetica", 18))
        label.pack(expand=True, fill='both', padx=20,pady=20)
        self.pack()

    def create_quality_meters(self):
        container = ttk.Frame(self)
        container.pack(side=TOP)
        meter1 = self.create_meter(container, 0.5, text = "quality 1 percentage")
        meter2 = self.create_meter(container, 0.5, text = "quality 2 percentage")
        meter3 = self.create_meter(container, 0.5, text = "quality 3 percentage")

    #Create meter
    def create_meter(self, parent, percentage, text = "group percentage"):
        meter = ttk.Meter(
            master = parent,
            metersize=150,
            padding=10,
            amounttotal=100,
            amountused = percentage * 100,# INSERT PERCENTAGE HERE (multiply by 100 if like 0.25 etc)
            metertype=FULL,
            subtext=text,
            interactive= True
        )
        meter.pack(side=LEFT)
        return meter
    
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

        table.pack(fill=BOTH, expand=YES, padx=10, pady=10, side=BOTTOM)
        return table

class NewGroupTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        placeholder = ttk.Label(self, text="Create a new group here", width = 50)
        placeholder.pack(fill=X, pady=10)
        self.pack()
