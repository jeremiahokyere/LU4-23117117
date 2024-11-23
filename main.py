import tkinter as tk
from views import LoginPage
from models import load_studenten, Docent

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cijfer App")
        self.geometry("1000x700")
        self.configure(bg="#222")

        # Laad studenten en docenten
        self.studenten = load_studenten("studenten.csv")
        self.docenten = {
            "docent": Docent("docent", "Chris Dina"),
        }

        self.current_frame = None
        self.switch_frame(LoginPage, self.studenten, self.docenten)

    def switch_frame(self, frame_class, *args):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame_class(self, *args)
        self.current_frame.pack(expand=True, fill="both")

if __name__ == "__main__":
    app = App()
    app.mainloop()