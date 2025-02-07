from tkinter import ttk
from .constants import Constants

class StyleManager:
    @staticmethod
    def configure_styles():
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('.', 
                      background=Constants.BG_COLOR,
                      foreground=Constants.TEXT_COLOR,
                      font=(Constants.FONT_NAME, Constants.BASE_FONT_SIZE))
        
        style.configure('TEntry',
                      padding=5,
                      borderwidth=2,
                      relief="solid",
                      background=Constants.ENTRY_COLOR,
                      fieldbackground="white",
                      foreground="black")
        
        style.configure('Custom.TFrame', 
                      background=Constants.SECTION_BG)