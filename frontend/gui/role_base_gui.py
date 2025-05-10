import tkinter as tk
from tkinter import messagebox

# Dummy role-based access logic
roles = {
    "technician": {
        "can_install_frontend": True,
        "can_add_modules": True,
        "can_access_backend": False,
        "can_create_users": False
    },
    "department_officer": {
        "can_install_frontend": True,
        "can_access_backend": True,
        "can_modify_modules": False,
        "can_request_core_change": True,
        "can_create_technicians": True
    },
    "admin": {
        "full_access": True
    }
}

# Dummy credentials
credentials = {
    "tech123": "technician",
    "officer456": "department_officer",
    "admin789": "admin"
}

class StarSonPOSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("StarSon POS Access Panel")
        self.geometry("400x300")
        self.resizable(False, False)
        self.role = None
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.build_login()

    def build_login(self):
        tk.Label(self, text="StarSon POS Login", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Username").pack()
        tk.Entry(self, textvariable=self.username).pack()

        tk.Label(self, text="Password").pack()
        tk.Entry(self, textvariable=self.password, show="*").pack()

        tk.Button(self, text="Login", command=self.authenticate).pack(pady=10)

    def authenticate(self):
        user = self.username.get()
        if user in credentials:
            self.role = credentials[user]
            self.show_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    def show_dashboard(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text=f"Welcome, {self.role.capitalize()}!", font=("Arial", 14)).pack(pady=10)

        if self.role == "technician":
            tk.Button(self, text="Install Frontend", command=lambda: self.action("Installing Frontend")).pack()
            tk.Button(self, text="Add Modules", command=lambda: self.action("Adding Modules")).pack()
        elif self.role == "department_officer":
            tk.Button(self, text="Access Backend", command=lambda: self.action("Accessing Backend")).pack()
            tk.Button(self, text="Request Core Access", command=lambda: self.action("Request Sent")).pack()
            tk.Button(self, text="Create Technician Access", command=lambda: self.action("Creating Technician")).pack()
        elif self.role == "admin":
            tk.Button(self, text="Access Full System", command=lambda: self.action("Full Admin Access")).pack()
            tk.Button(self, text="Create Department Officer", command=lambda: self.action("Creating Officer")).pack()

        tk.Button(self, text="Logout", command=self.logout).pack(pady=20)

    def action(self, message):
        messagebox.showinfo("Action", message)

    def logout(self):
        self.username.set("")
        self.password.set("")
        self.role = None
        for widget in self.winfo_children():
            widget.destroy()
        self.build_login()

if __name__ == "__main__":
    app = StarSonPOSApp()
    app.mainloop()
