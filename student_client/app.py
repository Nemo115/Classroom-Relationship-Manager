from frontend import *

"""
Run the application here.
"""

window_size = (1200, 1000)

if __name__ == "__main__":
    app = ttk.Window("Student Client", "sandstone", resizable = (True, True))
    app.geometry(f'{window_size[0]}x{window_size[1]}')
    app.minsize(window_size[0], window_size[1])
    app.iconbitmap('student_client/assets/icon.ico')
    App(app)
    app.mainloop()