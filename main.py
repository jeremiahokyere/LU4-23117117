import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cijfer App")
        self.geometry("1000x700")
        self.configure(bg="#222")

if __name__ == "__main__":
    app = App()
    app.mainloop()