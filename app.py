import tkinter as tk
from tkinter import Menu, messagebox, ttk
from config.styles import StyleManager  
from config.constants import Constants  
from widgets.frames import (  
    ProjectInfoFrame, 
    OperationalLimitsFrame, 
    DispatchControlFrame,
    SystemConfigurationFrame,
    ActionFrame
)

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        
        self.canvas = tk.Canvas(self, bg=Constants.SECTION_BG, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        
        self.scrollable_frame = ttk.Frame(self.canvas, style='Custom.TFrame')
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        
        self.canvas.bind("<Configure>", self._on_canvas_configure)  
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def _on_canvas_configure(self, event):
        
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

class BatteryModelerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Battery System Modeler")
        self.geometry(Constants.WINDOW_SIZE)
        self.configure(bg=Constants.BG_COLOR)
        self.minsize(900, 600)
        StyleManager.configure_styles()
        self._setup_main_window()
        self._make_responsive()
        
    def _make_responsive(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
    def _setup_main_window(self):
        self.scroll_container = ScrollableFrame(self)
        self.scroll_container.pack(fill="both", expand=True, padx=5, pady=5)
        self._create_menu()
        self._create_header()
        self._create_main_content()
        
    def _create_header(self):
        header_frame = ttk.Frame(self.scroll_container.scrollable_frame, style='Custom.TFrame')
        header_frame.pack(fill='x', padx=10, pady=5)
        
        
        logo_image = tk.PhotoImage(file="imgs/image.png")  
        
        
        logo_image = logo_image.subsample(1, 1)  
        
        
        logo_label = ttk.Label(
            header_frame,
            image=logo_image,
            background=Constants.SECTION_BG  
        )
        logo_label.image = logo_image  
        logo_label.pack(side='left', padx=Constants.PAD_X, pady=Constants.PAD_Y)
        
    def _create_menu(self):
        menu_bar = Menu(self)
        
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self._on_open)
        file_menu.add_command(label="Save", command=self._on_save)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        about_menu = Menu(menu_bar, tearoff=0)
        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Documentation", command=self._show_docs)
        
        menu_bar.add_cascade(label="File", menu=file_menu)
        menu_bar.add_cascade(label="About", menu=about_menu)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        
        self.config(menu=menu_bar)
        
    def _create_main_content(self):

        self.action_frame = ActionFrame(self.scroll_container.scrollable_frame,padding=10)
        
        self.project_info_frame = ProjectInfoFrame(self.scroll_container.scrollable_frame, padding=10)
        self.project_info_frame.pack(fill='x', padx=10, pady=5, anchor='w')
        
        self.operational_limits_frame = OperationalLimitsFrame(self.scroll_container.scrollable_frame, padding=10,parent_frame=self.action_frame)
        self.operational_limits_frame.pack(fill='x', padx=10, pady=5, anchor='w')
        
        self.dispatch_control_frame = DispatchControlFrame(self.scroll_container.scrollable_frame, padding=10,parent_frame=self.action_frame)
        self.dispatch_control_frame.pack(fill='x', padx=10, pady=5, anchor='w')

        system_config_frame = SystemConfigurationFrame(self.scroll_container.scrollable_frame)
        system_config_frame.pack(fill='x', padx=10, pady=5, anchor='w')

        self.action_frame.pack(fill='x', padx=10, pady=5, anchor='w')

        self.action_frame.set_operational_limits_frame(self.operational_limits_frame)
        self.action_frame.set_dispatch_control_frame(self.dispatch_control_frame)
        
    def _on_open(self):
        messagebox.showinfo("Open", "Open functionality to be implemented")
    
    def _on_save(self):
        messagebox.showinfo("Save", "Save functionality to be implemented")
    
    def _show_docs(self):
        messagebox.showinfo("Documentation", "Documentation to be added")

if __name__ == "__main__":
    app = BatteryModelerApp()
    app.mainloop()