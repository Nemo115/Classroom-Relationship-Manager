from backend import *

from PIL import Image
Image.CUBIC = Image.BICUBIC

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.validation import add_regex_validation
from ttkbootstrap.scrolled import ScrolledFrame

"""
This is the main frame in the window.
All visual objects will be initialized here.
"""
class App(ttk.Frame):
    def __init__(self, master_window):
        super().__init__(master_window, padding=(0, 10))
        self.pack(fill=BOTH, expand=YES)
        self.root = master_window

        self.side_menu_x = 0
        self.side_menu_active = True

        self.main_view_x = 300

        #Draw the Groupviewer
        self.navigation_bar = self.create_navigation_bar()
        self.main_view = self.create_main_view()

        self.insert_classes()


    def create_main_view(self):
        container = ttk.Frame(self, padding=(20,0))
        container.place(x=self.main_view_x, y=60, relwidth=1-self.get_width_percentage()-.1)#PUT THE CALCULATED WIDTH PERCENTAGE
        group_view = GroupViewer(container, root=self.root)
        #group_view.set_class_data()## Insert the first class from backend

        return {'container':container, 'group_view':group_view}

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

        side_bar_panel = ttk.Frame(self, bootstyle = 'secondary')
        side_bar_panel.place(x=self.side_menu_x, y=60, relheight=1, width=300)

        #temp_text = ttk.Label(side_bar_panel, text="This is where the classes go")
        #temp_text.pack(anchor=CENTER, pady=400)

        return side_bar_panel
    
    def insert_classes(self):
        for _class in classes_list: #for class in classes list
            ClassTab(self.navigation_bar, main_view=self.main_view, class_data=_class)
        
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
            self.navigation_bar.place(x=self.side_menu_x)
            self.main_view['container'].place(x=self.main_view_x)
            self.root.after(10, self.side_bar_enter)

    #Side bar pops out, and main view expands
    def side_bar_exit(self):
        self.side_menu_x -= 20
        self.main_view_x -= 20
        if self.side_menu_x >= -300:
            self.navigation_bar.place(x=self.side_menu_x)
            self.main_view['container'].place(x=self.main_view_x)
            self.root.after(10, self.side_bar_exit)

    def get_width_percentage(self):
        width = self.root.winfo_screenwidth()
        return 300/width

class ClassTab(ttk.Frame):
    def __init__(self, parent, main_view, class_data): # Currently put sample data in the class tab for testing
        super().__init__(parent)
        self.pack(fill=X, pady=10, side=TOP)

        self.parent = parent
        self.class_data = class_data
        self.main_view = main_view
        
        self.create_button()

    def create_button(self):
        button = ttk.Button(self, 
                            text = self.class_data['ClassName'], 
                            command=self.view_class)
        button.pack(fill=X)

    def view_class(self):
        print(f"\nclass: {self.class_data['ClassName']} clicked")
        ##call create notebook function in self.main_view['group_view']. Pass in parameters.
        self.main_view['group_view'].create_tabs(self.class_data)

"""
This is the group viewer.
Includes:
    - Notebook (tabs and pages)
"""
class GroupViewer(ttk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        #self.place(relx=0.2, rely=0.2, relwidth=.8, relheight=1)
        self.pack(fill=BOTH, expand=YES)

        self.root = root
        self.class_data = None

        self.create_notebook()
        self.create_tabs(classes_list[0])
    
    def create_tabs(self, class_data):
        self.class_data = class_data

        #RESET all tabs by deleting current ones
        for tab in self.notebook.master.winfo_children()[1:]:
            tab.destroy()

        # for group in class_data['Groups'], add new notebook tab with group passed as parameter
        for group_id in class_data['Groups']:
            group = get_group(group_id)
            self.add_notebook_tab(group)

        #make sure to put the add group tab at the end
        self.create_new_group_tab()
        
    def create_notebook(self):
        self.notebook = ttk.Notebook(self, bootstyle = "dark")
        self.notebook.pack(pady=20, padx=10, fill=BOTH)
        self.notebook.bind('<<NotebookTabChanged>>', self.tab_transition_anim)
    
    def add_notebook_tab(self, group):
        tab = GroupTab(self, group = group, root = self.root)#pass in group parameter from backend function. Containing the entire dict for the group
        self.notebook.add(tab, text=group['GroupName'])

    def create_new_group_tab(self):
        new_group_tab = NewGroupTab(self, self.class_data['ID'])
        self.notebook.add(new_group_tab, text=" + ")
    
    def refresh_groups(self):
        self.create_tabs(self.class_data)
        self.notebook.select(get_latest_group_in_class(self.class_data['ID']))
    
    def tab_transition_anim(self, *args):##Supposed to play meter enter animation
        print("Changed Tabs")
        #list(self.notebook.master.children.values())[self.notebook.index('current')+1].meters_enter_animation()

"""
This is the pages displayed for each tab in the group viewer.
Should include: 
    - Calculated compatibility/collaborative percentage
    - List of students in the current group and the corresponding data.
"""
class GroupTab(ttk.Frame):
    def __init__(self, parent, group, root):
        super().__init__(parent)
        self.data = row_data(group)
        self.group = group
        self.qualities = group['GroupQualities']
        self.root = root

        self.current_totals = {self.qualities[0]:0, self.qualities[1]:0, self.qualities[2]:0}
        self.quality_vars()

        self.quality_meters = self.create_quality_meters()
        self.table = self.create_table()
        label = ttk.Label(self, text = group['GroupName'], font=("Helvetica", 18))
        label.pack(expand=True, fill='both', padx=20,pady=20)
        self.pack()
    
    def quality_vars(self):
        qualities = self.group['GroupQualities']
        members = self.group['Members']
        self.totals = {qualities[0]:get_group_quality_average(members, qualities[0]), qualities[1]:get_group_quality_average(members, qualities[1]), qualities[2]:get_group_quality_average(members, qualities[2])}


    def meters_enter_animation(self):##Work on this logic
        # Animate the Meters when loaded and when new tab is clicked        
        for i in range(0,3):
            if self.current_totals[self.qualities[i]] < self.totals[self.qualities[i]]:
                self.current_totals[self.qualities[i]] += 1
        for i in range(0,3):
            if self.current_totals[self.qualities[i]] <= self.totals[self.qualities[i]]:
                list(self.quality_meters.values())[i].configure(amountused = self.current_totals[self.qualities[i]])
                self.root.after(1, self.meters_enter_animation)

    """
    def side_bar_enter(self):
        self.side_menu_x += 20
        self.main_view_x += 20
        if self.side_menu_x <= 0 and self.main_view_x <= 300:
            self.navigation_bar.place(x=self.side_menu_x)
            self.main_view['container'].place(x=self.main_view_x)
            self.root.after(10, self.side_bar_enter)
    """


    def create_quality_meters(self):
        container = ttk.Frame(self)
        container.pack(side=TOP)

        members = self.group['Members']
        qualities = self.group['GroupQualities']

        meter1 = self.create_meter(container, self.totals[qualities[0]], text = qualities[0])#get_group_quality_average(members, qualities[0])
        meter2 = self.create_meter(container, self.totals[qualities[1]], text = qualities[1])#get_group_quality_average(members, qualities[1])
        meter3 = self.create_meter(container, self.totals[qualities[2]], text = qualities[2])#get_group_quality_average(members, qualities[2])

        return {qualities[0]: meter1, qualities[1]: meter2, qualities[2]: meter3}

    #Create meter
    def create_meter(self, parent, percentage, text = "group percentage"):
        meter = ttk.Meter(
            master = parent,
            metersize=150,
            padding=10,
            amounttotal=100,
            amountused = percentage,
            metertype=FULL,
            subtext=text,
            interactive= False
        )
        meter.pack(side=LEFT)
        return meter
    
    def create_table(self):
        qualities = self.group['GroupQualities']
        headers = [
            {"text": "ID", "stretch":False, "width":40},
            {"text": "Name", "stretch": True},
            {"text": qualities[0], "stretch": True},
            {"text": qualities[1], "stretch": True},
            {"text": qualities[2], "stretch": True}
        ]
        table = Tableview(
            master=self,
            coldata= headers,
            rowdata= self.data,
            paginated=True,
            searchable=True,#Searchbar
            bootstyle=PRIMARY,
            stripecolor=('grey', None)
        )

        table.pack(fill=BOTH, expand=YES, padx=10, pady=10, side=BOTTOM)
        table.view.bind("<Double-1>", self.row_selected)

        return table
    
    def row_selected(self, event) -> None:
        selected = self.table.view.selection()
        record = self.table.iidmap.get(selected[0]).values
        print(f"selected: {record}")

class ViewStudent(ttk.Toplevel):
    def __init__(self, id):
        pass


class NewGroupTab(ttk.Frame):
    def __init__(self, parent, class_id):
        super().__init__(parent)
        placeholder = ttk.Label(self, text="Create a new group here", width = 50)
        placeholder.pack(fill=X, pady=10)
        self.pack()

        self.parent = parent
        self.class_id = class_id

        self.group_name = ttk.StringVar()
        self.group_members = []
        self.student_selections = {}#Dictionary of 1's and 0's

        self.first_quality = ttk.StringVar(value="first quality")
        self.second_quality = ttk.StringVar(value="second quality")
        self.third_quality = ttk.StringVar(value="third quality")
        
        self.create_form_entry("Group Name", self.group_name)

        self.create_quality_select("Select First Quality:",self.first_quality)
        self.create_quality_select("Select Second Quality:",self.second_quality)
        self.create_quality_select("Select Third Quality:",self.third_quality)

        self.create_student_list()

        self.create_submit_button()
    
    def create_form_entry(self, label, variable):
        form_field_container = ttk.Frame(self)
        form_field_container.pack(fill=X, expand=YES, pady=5)

        form_field_label = ttk.Label(master=form_field_container, text = label, width=15)
        form_field_label.pack(side = LEFT, padx = 12)

        form_input = ttk.Entry(master=form_field_container, textvariable=variable)
        form_input.pack(side=LEFT, padx=20, fill=X, expand=YES)

        add_regex_validation(form_input, r'^[a-zA-Z0-9_]*$')

        return form_input
    
    def create_quality_select(self, label, var):
        field_container = ttk.Frame(self)
        field_container.pack(fill=X, expand=YES, pady=5)

        field_label = ttk.Label(master=field_container, text = label, width=15)
        field_label.pack(side = LEFT, padx = 12)

        menu_select = ttk.Menubutton(master = field_container, bootstyle='outline info', textvariable=var)
        menu_select.pack(side=RIGHT, fill=X, expand=YES, padx=20)

        inside_menu=ttk.Menu(menu_select)
        for quality in qualities_options:
            inside_menu.add_radiobutton(label=quality, 
                                        variable=var, 
                                        command=self.update_quality_menus)
        menu_select['menu'] = inside_menu

    def create_submit_button(self):
        submit_button = ttk.Button(self, text="Create New Group", bootstyle = 'outline success', command=self.create_new_group)
        submit_button.pack(padx=50, fill=X, expand=YES, pady=5)

    def create_student_list(self):
        student_scroll_frame = ScrolledFrame(self, autohide=False, bootstyle='primary')
        student_scroll_frame.pack(pady=15, padx=30, fill=BOTH, expand=YES)

        for student in student_database:
            current_student = student_database[student]

            container = ttk.Frame(student_scroll_frame)
            container.pack(fill=X, expand=YES, pady=5)

            label = ttk.Label(master=container, text = current_student['Name'], width=15)
            label.pack(side = LEFT, padx=12)

            new_var = ttk.IntVar()
            toggle_button = ttk.Checkbutton(master=container, 
                                            bootstyle = 'info-round_toggle', 
                                            variable = new_var, onvalue=1, offvalue=0, 
                                            command=lambda x = current_student: self.student_selected(x))
            toggle_button.pack(side=RIGHT, padx=25)
            
            self.student_selections[current_student['ID']] = new_var

    def student_selected(self, student):
        add = self.student_selections[student['ID']].get()
        if add:
            self.group_members.append(student['ID'])
        else:
            self.group_members.remove(student['ID'])
            
    def update_quality_menus(self):##Debugging method
        print(f"\nGroup Name: {self.group_name.get()}\nfirst quality: {self.first_quality.get()}\nsecond quality: {self.second_quality.get()}\nthird quality: {self.third_quality.get()}")

    def create_new_group(self):## on button pressed, pass parameters to create_group() from backend
        group_name = self.group_name.get()
        group_qualities = [self.first_quality.get(), self.second_quality.get(), self.third_quality.get()]

        error = ""

        if not group_name:
            error = "Must input a group name"
        elif ((group_qualities[0] in qualities_options) and (group_qualities[1] in qualities_options) and (group_qualities[2] in qualities_options)) == False:
            error = "Must input qualities for each group"
        elif group_qualities[0] == group_qualities[1] or group_qualities[2] == group_qualities[0] or group_qualities[1] == group_qualities[2]:
            error = "Must input DIFFERENT qualities for each group"
        elif self.group_members == []:
            error = "Must select students"

        if error:
            toast = ToastNotification(
                title="Error",
                message=error,
                duration = 3000
            )
            toast.show_toast()
            return
        else:
            create_group(group_name=group_name, group_members=self.group_members, group_qualities=group_qualities, class_id=self.class_id)
            #Refresh Notebook
            self.parent.refresh_groups()
            toast = ToastNotification(
                title="Success",
                message=f"You have successfully added new group {group_name}",
                duration = 3000
            )
            toast.show_toast()
