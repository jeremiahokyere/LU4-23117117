import tkinter as tk
from tkinter import ttk, messagebox

class LoginPage(tk.Frame):
    def __init__(self, master, studenten, docenten):
        super().__init__(master, bg="#222")
        self.studenten = studenten
        self.docenten = docenten
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        login_frame = tk.Frame(self, bg="#222")
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(login_frame, text="Inloggen", font=("Arial", 20), fg="white",bg="#222").grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(login_frame, text="Gebruikersnaam:", font=("Arial", 14), fg="white",bg="#222").grid(row=1, column=0, sticky="e", padx=10)
        self.gebruikersnaam_entry = tk.Entry(login_frame, width=25)
        self.gebruikersnaam_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Label(login_frame, text="Wachtwoord:", font=("Arial", 14), fg="white",bg="#222").grid(row=2, column=0, sticky="e", padx=10)
        self.wachtwoord_entry = tk.Entry(login_frame, width=25, show="*")
        self.wachtwoord_entry.grid(row=2, column=1, padx=10, pady=5)
        tk.Button(login_frame, text="Login", command=self.login, bg="#444",fg="white").grid(row=3, column=0, columnspan=2, pady=10)

    def login(self):
        gebruikersnaam = self.gebruikersnaam_entry.get()
        wachtwoord = self.wachtwoord_entry.get()

        if (gebruikersnaam in self.studenten and
                self.studenten[gebruikersnaam].wachtwoord == wachtwoord):
            self.master.switch_frame(StudentDashboard, self.studenten[gebruikersnaam])
        elif (gebruikersnaam in self.docenten and gebruikersnaam in self.docenten and
              wachtwoord == "password1"):
            self.master.switch_frame(DocentDashboard, self.studenten,self.docenten[gebruikersnaam].name)
        else:
            messagebox.showerror("inloggen mislukt", "Onjusite gebruikersnaam of wachtwoord.")

class StudentDashboard(tk.Frame):
    def __init__(self, master, student):
        super().__init__(master, bg="#222")
        self.student = student
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text=f"Welkom, {self.student.voornaam}!", font=("Arial", 20), fg="white", bg="#222").pack(pady=10)


class DocentDashboard(tk.Frame):
    def __init__(self, master, studenten, docent_name):
        super().__init__(master, bg="#222")
        self.studenten = studenten
        self.docent_name = docent_name
        self.selected_student = None
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Docent Dashboard", font=("Arial", 20), fg="white", bg="#222").pack(pady=10)

