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

    def test_docent_toets_invoeren(self):
        """test of de docent een toets kan invoeren."""
        student = self.studenten["Mike Tyson"]
        student.add_grade(
            subject="Engels",
            grade=8.0,
            date="02-01-2024",
            attempts=1,
            description="Top!",
            docent=self.docent.name
        )
        self.assertEqual(len(student.view_grades()), 2, "toets is niet toegevoegd")
        self.assertEqual(student.view_grades()[-1]["subject"], "Engels", "toets klopt niet")

    def test_docent_toets_wijzigen(self):
        """test of de docent een toets kan wijzigen"""
        student = self.studenten["Mike Tyson"]
        toets = student.view_grades()[0]
        toets["grade"] = 6.5
        toets["description"] = "kan beter"
        self.assertEqual(toets["grade"], 6.5, "cijfer is niet gewijzigd")
        self.assertEqual(toets["description"], "kan beter", "feedback is niet gewijzigd")

    def test_docent_toets_verwijderen(self):
        """test of de docent een toets kan verwijderen"""
        student = self.studenten["Mike Tyson"]
        cijfers = student.view_grades()
        del cijfers[0]
        self.assertEqual(len(student.view_grades()), 0, "Toets is niet verwijderd")

    def test_docent_overzicht_student_toetsen(self):
        """test of de docent een overzicht van toetsen van een student kan zien"""
        student = self.studenten["Mike Tyson"]
        toetsen = student.view_grades()
        self.assertEqual(len(toetsen), 1, "toetsen overzicht is leeg")
        self.assertEqual(toetsen[0]["subject"], "wiskunde", "toets overzicht is verkeerd")



if __name__ == "__main__":
    unittest.main()