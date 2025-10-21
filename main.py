from View.TableView import CoursesApp


# ------------------ Run ------------------

if __name__ == "__main__":
    # init_db()
    app = CoursesApp()
    app.load()
    app.view()
    app.mainloop()
