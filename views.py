import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

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
        total_points = self.student.calculate_study_points()
        remaining_points = 60 - total_points

        tk.Label(self, text=f"Welkom, {self.student.voornaam}!", font=("Arial", 20), fg="white", bg="#222").pack(pady=10)
        tk.Label(self, text=f"Studiepunten: {total_points}/60", font=("Arial", 16), fg="white", bg="#222").pack()
        tk.Label(self, text=f"Je hebt {remaining_points} meer studiepunten nodig om je propedeuse te halen.",
                 font=("Arial", 14), fg="white", bg="#222").pack(pady=10)

        tk.Label(self, text="Jou examen:", font=("Arial", 16), fg="white", bg="#222").pack()

        for grade in self.student.grades:
            frame = tk.Frame(self, bg="#333", bd=2, relief="solid", padx=10, pady=10)
            frame.pack(pady=5, fill="x")
            tk.Label(frame, text=f"{grade['subject']} - {grade['grade']}", font=("Arial", 14), fg="white",bg="#333").pack()
            frame.bind("<Button-1>", lambda e, g=grade: self.show_grade_details(g))

        tk.Button(self, text="Log uit",command=lambda: self.master.switch_frame(LoginPage, self.master.studenten, self.master.docenten),bg="#444", fg="white", font=("Arial", 12)).pack(pady=20)

    def show_grade_details(self, grade):
        messagebox.showinfo("Examen info",f"Toets: {grade['subject']}\nCijfer: {grade['grade']}\nDatum: {grade['date']}\nStatus: {grade['status']}\nPogingen: {grade['attempts']}\nFeedback: {grade['description']}\nDocent: {grade['docent']}")


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

    def edit_grade(self, grade):
        self.grade_form_popup(grade)

    def delete_grade(self, grade):
        self.selected_student.grades.remove(grade)
        self.load_student_grades(None)
        messagebox.showinfo("Gelukt!", "Examen Verwijderd")

    def grade_form_popup(self, grade=None):
        popup = tk.Toplevel(self)
        popup.title("Bewerk/Voeg examen toe")
        popup.geometry("400x500")
        popup.configure(bg="#222")

        tk.Label(popup, text=f"Student: {self.selected_student.voornaam} {self.selected_student.achternaam}", font=("Arial", 14), fg="white", bg="#222").pack(pady=10)

        tk.Label(popup, text="Toets:", font=("Arial", 12), fg="white", bg="#222").pack(pady=5)
        subject_entry = tk.Entry(popup, width=30)
        subject_entry.pack(pady=5)

        tk.Label(popup, text="Cijfer:", font=("Arial", 12), fg="white", bg="#222").pack(pady=5)
        grade_entry = tk.Entry(popup, width=10)
        grade_entry.pack(pady=5)

        tk.Label(popup, text="Datum:", font=("Arial", 12), fg="white", bg="#222").pack(pady=5)
        date_entry = tk.Entry(popup, width=15)
        date_entry.pack(pady=5)

        tk.Label(popup, text="Pogingen:", font=("Arial", 12), fg="white", bg="#222").pack(pady=5)
        attempts_entry = tk.Entry(popup, width=10)
        attempts_entry.pack(pady=5)

        description = tk.Text(popup,width=30, height=5)
        description.pack(pady=10)

        if grade:
            subject_entry.insert(0, grade["subject"])
            grade_entry.insert(0, grade["grade"])
            date_entry.insert(0, grade["date"])
            attempts_entry.insert(0, grade["attempts"])
            description.insert("1.0", grade["description"])

        def save():
            subject = subject_entry.get()
            try:
                grade_val = float(grade_entry.get())
                if not 0 <= grade_val <= 10:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Cijfer moet een getal zijn tussen de 1-10.")
                return

            try:
                datetime.strptime(date_entry.get(), "%d-%m-%Y")
            except ValueError:
                messagebox.showerror("Error", "Geen geldige datum input. gebruik dd-mm-yyyy.")
                return

            attempts = attempts_entry.get()
            if not attempts.isdigit() or int(attempts) <= 0:
                messagebox.showerror("Error", "Pogingen moeten een positieve integer zijn")
                return

            if grade:
                grade.update({
                    "subject": subject,
                    "grade": grade_val,
                    "date": date_entry.get(),
                    "attempts": int(attempts),
                    "description": description.get("1.0", "end").strip(),
                    "status": "Behaald" if grade_val >= 5.5 else "Niet behaald",
                })
            else:
                self.selected_student.add_grade(subject, grade_val, date_entry.get(), int(attempts), description.get("1.0", "end").strip(), self.docent_name)

            self.load_student_grades(None)
            popup.destroy()
            messagebox.showinfo("Gelukt!", "Toets Opgeslagen")

        tk.Button(popup, text="Opslaan", command=save, bg="#444", fg="white").pack(pady=10)
