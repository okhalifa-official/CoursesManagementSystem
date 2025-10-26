"""
This is the main entry point for the Courses Management System app.
It initializes the Tkinter window and loads the main view.
"""

from View.TableView import CoursesApp


# ------------------ Run ------------------

if __name__ == "__main__":
    # init_db()
    app = CoursesApp()
    app.load()
    app.view()
    app.mainloop()
