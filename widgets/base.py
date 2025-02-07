from tkinter import ttk
from config.constants import Constants

class BaseFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, style='Custom.TFrame', **kwargs)
        self._create_widgets()
        self._configure_grid()
        
    def _create_widgets(self):
        raise NotImplementedError
    
    def _configure_grid(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=2)

    def _create_section_header(self, section_name):
        header_frame = ttk.Frame(self, style='Custom.TFrame')
        header_frame.grid(row=0, column=0, columnspan=4, sticky='ew', pady=(0, Constants.PAD_Y))
        
        section_label = ttk.Label(
            header_frame,
            text=section_name,
            font=Constants.TITLE_FONT,
            foreground=Constants.TEXT_COLOR,
            background=Constants.SECTION_BG,
            anchor="w"
        )
        section_label.pack(fill='x', pady=(Constants.PAD_Y, 0), padx=Constants.PAD_X)
        
        separator = ttk.Separator(header_frame, orient='horizontal')
        separator.pack(fill='x', pady=(Constants.PAD_Y, 0))