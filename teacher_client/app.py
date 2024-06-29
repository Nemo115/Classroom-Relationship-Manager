from frontend import *

"""
Run the application here.
test commit by lachie
"""

window_size = (1400, 1000)

if __name__ == "__main__":
    app = ttk.Window("Student Relationship Manager", "minty", resizable = (True, True))
    app.geometry(f'{window_size[0]}x{window_size[1]}')
    app.minsize(window_size[0], window_size[1])
    App(app)
    app.mainloop()