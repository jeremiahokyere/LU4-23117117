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

        student_names = [f"{s.voornaam} {s.achternaam}" for s in self.studenten.values()]
        self.student_selection = ttk.Combobox(self, values=student_names, state="readonly")
        self.student_selection.pack(pady=10)
        self.student_selection.bind("<<ComboboxSelected>>", self.load_student_grades)

        self.grades_frame = tk.Frame(self, bg="#222")
        self.grades_frame.pack(pady=10, fill="both", expand=True)

        tk.Button(self, text="Nieuwe Examen", command=self.add_new_grade, bg="#444", fg="white").pack(pady=10)
        tk.Button(self, text="Log uit",command=lambda: self.master.switch_frame(LoginPage, self.studenten, self.master.docenten), bg="#444",fg="white").pack(pady=10)

    def load_student_grades(self, _):
        self.grades_frame.destroy()
        self.grades_frame = tk.Frame(self, bg="#222")
        self.grades_frame.pack(pady=10, fill="both", expand=True)

        selected_student_name = self.student_selection.get()
        self.selected_student = next((s for s in self.studenten.values() if f"{s.voornaam} {s.achternaam}" == selected_student_name), None)

        if not self.selected_student:
            return
        for grade in self.selected_student.grades:
            frame = tk.Frame(self.grades_frame, bg="#333", bd=2, relief="solid", padx=10, pady=10)
            frame.pack(pady=5, fill="x")
            tk.Label(frame, text=f"{grade['subject']} - {grade['grade']}", font=("Arial", 14), fg="white", bg="#333").pack()
            tk.Button(frame, text="Bewerk", command=lambda g=grade: self.edit_grade(g), bg="#555", fg="white").pack(side="right", padx=5)
            tk.Button(frame, text="Verwijder", command=lambda g=grade: self.delete_grade(g), bg="#555", fg="white").pack(side="right")

    def add_new_grade(self):
        if not self.selected_student:
            messagebox.showerror("Error", "Selecteer eerst een student")
            return
        self.grade_form_popup()
