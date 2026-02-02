# app.py
import customtkinter as ctk
from db_manager import init_db
from ui_main import MainView
from ui_form_desarrollo import NuevoDesarrolloForm

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Control de Desarrollos")
        self.geometry("1000x700")

        init_db()  # Inicializa la base de datos

        self.main_view = MainView(self, self.open_new_form)
        self.main_view.pack(fill="both", expand=True)

    def open_new_form(self):
        form = NuevoDesarrolloForm(self, self.refresh_main_view)

    def refresh_main_view(self):
        self.main_view.destroy()
        self.main_view = MainView(self, self.open_new_form)
        self.main_view.pack(fill="both", expand=True)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()
