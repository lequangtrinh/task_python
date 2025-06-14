import tkinter as tk
from uis.application_ui import Application
import customtkinter as ctk
if __name__ == "__main__":
    root = ctk.CTk()
    app = Application(root)
    root.mainloop()