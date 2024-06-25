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
        
        
