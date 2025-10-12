from View.Login import LoginViewController as Login


# ------------------ Run ------------------

if __name__ == "__main__":
    # init_db()
    app = Login.LoginView()
    app.view()
    app.mainloop()
