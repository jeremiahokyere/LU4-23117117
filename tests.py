import unittest
from models import Student, Docent


#Basis info
class TestApplicatie(unittest.TestCase):
    def setUp(self):
        self.studenten = {
            "Mike Tyson": Student(
                gebruikersnaam="m.tyson",
                wachtwoord="jakepaul",
                voornaam="Mike",
                achternaam="Tyson",
                leeftijd=58
            )
        }
        self.docent = Docent(gebruikersnaam="docent", name="Chris Dina")

        self.studenten["Mike Tyson"].add_grade(
            subject="wiskunde",
            grade=6,
            date="05-08-2002",
            attempts=2,
            description="Goed gedaan!",
            docent="Chris Dina"
        )

    def test_student_overzicht_cijfers(self):
        """test of de student een overzicht van zijn cijfers per vak kan zien"""
        student = self.studenten["Mike Tyson"]
        cijfers = student.view_grades()
        self.assertGreater(len(cijfers), 0, "cijfers overzicht is leeg")
        self.assertEqual(cijfers[0]["subject"], "wiskunde", "vak komt niet overeen")
        self.assertEqual(cijfers[0]["grade"], 6, "cijfer komt niet overeen")

    def test_student_studiepunten(self):
        """test of de student behaalde studiepunten kan zien"""
        student = self.studenten["Mike Tyson"]
        behaalde_punten = student.calculate_study_points()
        self.assertEqual(behaalde_punten, 10, "behaalde studiepunten zijn incorrect")

    def test_student_openstaande_studiepunten(self):
        """test of de student openstaande studiepunten kan zien."""
        student = self.studenten["Mike Tyson"]
        behaalde_punten = student.calculate_study_points()
        openstaande_punten = 60 - behaalde_punten
        self.assertEqual(openstaande_punten, 50, "de openstaande studiepunten zijn incorrect")

    def test_student_feedback(self):
        """test of de student feedback op exames kan zien."""
        student = self.studenten["Mike Tyson"]
        cijfers = student.view_grades()
        self.assertIn("description", cijfers[0], "Geen feedback")
        self.assertEqual(cijfers[0]["description"], "Goed gedaan!", "Feedback is incorrect.")



if __name__ == "__main__":
    unittest.main()