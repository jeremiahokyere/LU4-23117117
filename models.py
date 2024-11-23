import csv

class Student:
    def __init__(self, gebruikersnaam, wachtwoord, voornaam, achternaam, leeftijd):
        """student class en alle attributen"""
        self.gebruikersnaam = gebruikersnaam
        self.wachtwoord = wachtwoord
        self.voornaam = voornaam
        self.achternaam = achternaam
        self.leeftijd = leeftijd
        self.grades = []

    def add_grade(self, subject, grade, date, attempts, description, docent):
        status = "Behaald" if grade >= 5.5 else "Niet behaald"
        self.grades.append({
            "subject": subject,
            "grade": grade,
            "date": date,
            "attempts": attempts,
            "status": status,
            "description": description,
            "docent": docent
        })

    def view_grades(self):
        return self.grades

    def calculate_study_points(self):
        return sum(10 for grade in self.grades if grade["grade"] >= 5.5)

class Docent:
    def __init__(self, gebruikersnaam, name):
        "Docenten class en de attributen"
        self.gebruikersnaam = gebruikersnaam
        self.name = name

#laden van studenten
def load_studenten(file_path):
    studenten = {}
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                student = Student(
                    gebruikersnaam=row["gebruikersnaam"],
                    wachtwoord=row["wachtwoord"],
                    voornaam=row["voornaam"],
                    achternaam=row["achternaam"],
                    leeftijd=int(row["leeftijd"])
                )
                studenten[row["gebruikersnaam"]] = student
    except FileNotFoundError:
        print(f"Bestand {file_path} begin met een nieuwe database")
    return studenten