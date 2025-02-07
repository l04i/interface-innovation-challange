from datetime import datetime, timedelta
import re
from tkinter import ttk,Tk 
import customtkinter as ctk
import tkinter as tk
from .base import BaseFrame  
from config.constants import Constants 
import time
import threading
from PIL import Image, ImageTk

class ProjectInfoFrame(BaseFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._create_section_header("Project Info")
        
    def _create_widgets(self):
        self._create_project_name_field()
        self._create_file_name_field()
        
    def _create_project_name_field(self):
        lbl = ttk.Label(self, text=" 💡 Project Name:", style='Section.TLabel', 
                       font=Constants.LABEL_FONT, background=Constants.SECTION_BG)
        lbl.grid(row=1, column=0, padx=(Constants.PAD_X, 0), pady=Constants.PAD_Y, sticky='w')
        
        self.project_name_entry = ctk.CTkEntry(
            self, width=Constants.ENTRY_WIDTH * 7,
            font=(Constants.FONT_NAME, Constants.BASE_FONT_SIZE),
            fg_color=Constants.FIELD_COLOR,
            border_color=Constants.BORDER_COLOR,
            bg_color=Constants.SECTION_BG,
            text_color="black",
            placeholder_text="e.g., Solar Farm Alpha, Wind Project Delta",
            corner_radius=10
        )
        self.project_name_entry.grid(row=1, column=1, padx=(0, 0),
                                   pady=Constants.PAD_Y, ipady=3, sticky='ew')
        
    def _create_file_name_field(self):
        lbl = ttk.Label(self, text="  📁 File Name:", style='Section.TLabel',
                       font=Constants.LABEL_FONT, background=Constants.SECTION_BG)
        lbl.grid(row=1, column=2, padx=(Constants.PAD_X, 0), pady=Constants.PAD_Y, sticky='w')
        
        self.file_name_entry = ctk.CTkEntry(
            self, width=Constants.ENTRY_WIDTH * 7,
            font=(Constants.FONT_NAME, Constants.BASE_FONT_SIZE),
            fg_color=Constants.FIELD_COLOR,
            border_color=Constants.BORDER_COLOR,
            bg_color=Constants.SECTION_BG,
            text_color="black",
        placeholder_text= "e.g., data_2024-01-15.csv",
            corner_radius=10,
        )
        self.file_name_entry.grid(row=1, column=3, padx=(0, 0),
                                pady=Constants.PAD_Y, ipady=3, sticky='ew')

class OperationalLimitsFrame(BaseFrame):
    def __init__(self, master, parent_frame, **kwargs):
        super().__init__(master, **kwargs)
        self._create_section_header("Operational Limits")
        self.parent_frame = parent_frame
        self._create_widgets()

    def _create_widgets(self):
        self._create_max_soc_field()
        self._create_min_soc_field()

    def _create_max_soc_field(self):
        self.max_soc_var = ctk.StringVar()
        self.initial_soc_var = ctk.StringVar()

        fields = [
            ("Max SoC:", self.max_soc_var, 2),
            ("Initial SoC:", self.initial_soc_var, 3)
        ]

        for label_text, var, row in fields:
            self._create_entry_field(label_text, row, 0, 1, var)
            var.trace_add('write', self._validate_numeric_input)
            var.trace_add('write', self._validate_initial_soc)
            var.trace_add('write', self._notify_parent)

    def _create_min_soc_field(self):
        self.min_soc_var = ctk.StringVar()
        self._create_entry_field("Min SoC:", 1, 0, 1, self.min_soc_var)
        self.min_soc_var.trace_add('write', self._validate_numeric_input)
        self.min_soc_var.trace_add('write', self._validate_initial_soc)
        self.min_soc_var.trace_add('write', self._notify_parent)

    def _create_entry_field(self, label_text, row, col, span, var):
        """Creates an entry field with a placeholder and numeric validation."""
        placeholder_texts = {
            "Min SoC:": "Minimum State of Charge (0-100)%",
            "Initial SoC:": "Starting State of Charge (0-100)%",
            "Max SoC:": "Maximum State of Charge (0-100)%"
        }

        placeholder_text = placeholder_texts.get(label_text, "")

        lbl = ttk.Label(self, text=label_text, style='Section.TLabel',
                        font=Constants.LABEL_FONT, background=Constants.SECTION_BG)
        lbl.grid(row=row, column=col, padx=(Constants.PAD_X, 0), pady=Constants.PAD_Y, sticky='w')

        entry = ctk.CTkEntry(
            self, width=Constants.ENTRY_WIDTH / 10,
            font=(Constants.FONT_NAME, Constants.BASE_FONT_SIZE),
            fg_color=Constants.FIELD_COLOR,
            border_color=Constants.BORDER_COLOR,
            text_color="black",
            bg_color=Constants.SECTION_BG,
            placeholder_text=placeholder_text,
            textvariable=var,
            corner_radius=10
        )
        entry.grid(row=row, column=col + span, padx=(30),
                   pady=Constants.PAD_Y, ipady=3, sticky='ew')

        
        if label_text == "Initial SoC:":
            self.initial_soc_entry = entry

        return entry

    def _validate_numeric_input(self, *args):
        """Ensure only numeric input (integers or floats) is entered."""
        for var in [self.min_soc_var, self.max_soc_var, self.initial_soc_var]:
            value = var.get()

        
            if not re.fullmatch(r"^\d*\.?\d*$", value) and value != "":
                var.set(re.sub(r"[^0-9.]", "", value))  

        
            if value.count('.') > 1:
                var.set(value[:value.rfind('.')])  


    def _validate_initial_soc(self, *args):
        """Ensure Initial SoC is within the Min/Max SoC range."""
        try:
            min_soc = float(self.min_soc_var.get()) if self.min_soc_var.get() else 0
            max_soc = float(self.max_soc_var.get()) if self.max_soc_var.get() else 100
            initial_soc = float(self.initial_soc_var.get()) if self.initial_soc_var.get() else None

            if initial_soc is None:
                return  

            if min_soc <= initial_soc <= max_soc:
                self.initial_soc_entry.configure(border_color=Constants.BORDER_COLOR)  
                return True
            else:
                self.initial_soc_entry.configure(border_color="red") 
                return False 
        except ValueError:
            pass  

    def _notify_parent(self, *args):
        """Notify the parent frame when values change."""
        if self.parent_frame and hasattr(self.parent_frame, '_update_run_button'):
            self.parent_frame._update_run_button()



class DispatchControlFrame(BaseFrame):
    def __init__(self, master, parent_frame, **kwargs):
        self.entries = []  
        self.labels = []   
        self.dropdowns = []  
        super().__init__(master, **kwargs)
        self.parent_frame = parent_frame
        self._create_section_header("Dispatch Control")
        self._create_widgets()

    def _create_widgets(self):
        self._create_daily_soc_steer_fields()

    def _create_daily_soc_steer_fields(self):
        self.soc_steer_var = ctk.BooleanVar() 
        self.soc_steer_var.trace_add('write', self._update_fields_state)
         

        chk_soc_steer = ctk.CTkCheckBox(
            self, text="Daily State of Charge Steer",
            variable=self.soc_steer_var,
            font=(Constants.FONT_NAME, Constants.LABEL_FONT[1]),
            fg_color="white",
            bg_color=Constants.SECTION_BG,
            border_color=Constants.BORDER_COLOR,
            text_color=Constants.TEXT_COLOR,
            hover_color="white",
            corner_radius=7,
            checkmark_color=Constants.ACCENT_COLOR,
            checkbox_height=20, checkbox_width=20
        )
        chk_soc_steer.grid(row=1, column=0, columnspan=2, padx=(0, 0),
                           pady=Constants.PAD_Y, sticky='w')

        fields = [
            ("Start Time:", 2),
            ("SoC Target:", 4),
            ("End Time:", 3),
            ("Power Setpoint:", 5)
        ]

        for label_text, row in fields:
            if label_text in ["Start Time:", "End Time:"]:
                
                dropdown = self._create_dropdown_field(label_text, row, 0, 1)
                if label_text == "Start Time:":
                    self.start_time_dropdown = dropdown
                    dropdown.configure(command=self._update_end_time_options)  
                else:
                    self.end_time_dropdown = dropdown
                    dropdown.configure(command=self._validate_end_time)  
            else:
                
                entry = self._create_entry_field(label_text, row, 0, 1)
                entry.bind('<KeyRelease>', self._notify_parent)

        
        self._update_fields_state()



    def _create_dropdown_field(self, label_text, row, col, span):
        lbl = ttk.Label(self, text=label_text, style='Section.TLabel',
                        font=Constants.LABEL_FONT, background=Constants.SECTION_BG)
        lbl.grid(row=row, column=col, padx=(Constants.PAD_X, 0), pady=Constants.PAD_Y, sticky='w')

        
        if label_text == "Start Time:":
            time_options = self._generate_time_options("12:00 AM", "11:45 PM", 15)
        else:
            time_options = self._generate_time_options("12:15 AM", "11:59 PM", 15)

        dropdown = ctk.CTkComboBox(
            self, width=Constants.ENTRY_WIDTH / 10,
            font=(Constants.FONT_NAME, Constants.BASE_FONT_SIZE),
            fg_color=Constants.FIELD_COLOR,
            border_color=Constants.BORDER_COLOR,
            text_color="black",
            bg_color=Constants.SECTION_BG,
            corner_radius=10,
            state="readonly",
            values=time_options,
            dropdown_font=(Constants.FONT_NAME, Constants.BASE_FONT_SIZE - 2),  
            dropdown_hover_color=Constants.ACCENT_COLOR,  
            button_color=Constants.FIELD_COLOR_DISABLED,  

        )
        dropdown.grid(row=row, column=col + span, padx=(0, Constants.PAD_X * 2),
                      pady=Constants.PAD_Y, ipady=3, sticky='ew')

        
        if label_text == "Start Time:":
            dropdown.set("12:00 AM")  
        else:
            dropdown.set("12:15 AM")  

        
        self.dropdowns.append(dropdown)
        self.labels.append(lbl)

        return dropdown
    
    

    def _generate_time_options(self, start_time, end_time, interval_minutes):
        from datetime import datetime, timedelta

        start = datetime.strptime(start_time, "%I:%M %p")
        end = datetime.strptime(end_time, "%I:%M %p")
        current = start
        options = []

        while current <= end:
            options.append(current.strftime("%I:%M %p"))
            current += timedelta(minutes=interval_minutes)

        return options

    def _update_end_time_options(self, *args):
        """Update End Time dropdown options based on the selected Start Time."""
        start_time = self.start_time_dropdown.get()
        start_time_dt = datetime.strptime(start_time, "%I:%M %p")

        
        new_end_times = self._generate_time_options(
            (start_time_dt + timedelta(minutes=15)).strftime("%I:%M %p"),
            "11:59 PM",
            15
        )

        
        self.end_time_dropdown.configure(values=new_end_times)

        
        self._validate_end_time()

    def _validate_end_time(self, *args):
        """Validate that the End Time is after the Start Time."""
        start_time = self.start_time_dropdown.get()
        end_time = self.end_time_dropdown.get()

        start_time_dt = datetime.strptime(start_time, "%I:%M %p")
        end_time_dt = datetime.strptime(end_time, "%I:%M %p")

        if end_time_dt <= start_time_dt:
            
            next_valid_time = (start_time_dt + timedelta(minutes=15)).strftime("%I:%M %p")
            self.end_time_dropdown.set(next_valid_time)
            print("Error: End Time cannot precede Start Time. Resetting to the next valid time.")

    def _create_entry_field(self, label_text, row, col, span):
        placeholder_texts = {
        "SoC Target:": "Desired State of Charge (0-100)%",
        "Power Setpoint:": "Target power output in kilowatts"
    }
    
    
        placeholder_text = placeholder_texts.get(label_text, "")
        lbl = ttk.Label(self, text=label_text, style='Section.TLabel',
                        font=Constants.LABEL_FONT, background=Constants.SECTION_BG)
        lbl.grid(row=row, column=col, padx=(Constants.PAD_X, 0), pady=Constants.PAD_Y, sticky='w')

        entry = ctk.CTkEntry(
            self, width=Constants.ENTRY_WIDTH / 10,
            font=(Constants.FONT_NAME, Constants.BASE_FONT_SIZE),
            fg_color=Constants.FIELD_COLOR,
            border_color=Constants.BORDER_COLOR,
            text_color="black",
            bg_color=Constants.SECTION_BG,
            placeholder_text=placeholder_text,
            corner_radius=10
        )
        entry.grid(row=row, column=col + span, padx=(0, Constants.PAD_X * 2),
                   pady=Constants.PAD_Y, ipady=3, sticky='ew')

        
        self.entries.append(entry)
        self.labels.append(lbl)

        return entry

    def _update_fields_state(self, *args):
        enabled = self.soc_steer_var.get()

        
        label_color = Constants.TEXT_COLOR if enabled else Constants.TEXT_COLOR_DISABLED
        field_color = Constants.FIELD_COLOR if enabled else Constants.FIELD_COLOR_DISABLED

        
        for entry in self.entries:
            entry.configure(
                state='normal' if enabled else 'disabled',
                fg_color=field_color
            )

        
        for dropdown in self.dropdowns:
            dropdown.configure(state='normal' if enabled else 'disabled',fg_color=Constants.FIELD_COLOR if enabled else Constants.FIELD_COLOR_DISABLED )

        
        for label in self.labels:
            label.configure(foreground=label_color)

    def _notify_parent(self, *args):
        if self.parent_frame and hasattr(self.parent_frame, '_update_run_button'):
            self.parent_frame._update_run_button()




class SystemConfigurationFrame(BaseFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._create_widgets()
        self.thumbnail = None  
        self.full_image = None  

    def _create_widgets(self):
        
        self._create_section_header("System Configuration")

        
        self._create_thumbnail()


    def _create_thumbnail(self):
        """Add a thumbnail with an icon to the frame."""
        try:
            
            icon_image = Image.open("imgs/thumb.png").convert("RGBA")  
            icon_size = (50, 50)  
            icon_image.thumbnail(icon_size)

            
            self.thumbnail = ctk.CTkImage(
                light_image=icon_image,
                dark_image=icon_image,
                size=icon_size
                
            )

            
            self.thumbnail_label = ctk.CTkLabel(self, image=self.thumbnail, text="")
            self.thumbnail_label.grid(row=1, column=0, padx=Constants.PAD_X, pady=Constants.PAD_Y, sticky='w')

            
            self.thumbnail_label.bind("<Button-1>", self._open_full_image)
        except Exception as e:
            print(f"Error loading icon: {e}")

    def _open_full_image(self, event):
        """Open a popup to display the full-sized image fitting the window size."""
        try:
            
            image = Image.open("imgs/system.png")  
            width, height = image.size

            
            self.popup = tk.Toplevel(self)
            self.popup.title("Full Image")
            self.popup.geometry("800x600")  
            self.popup.resizable(True, True)

            
            resized_image = image.resize((800, 600), Image.ANTIALIAS)
            self.full_image = ImageTk.PhotoImage(resized_image)

            
            self.full_image_label = tk.Label(self.popup, image=self.full_image)
            self.full_image_label.pack(fill="both", expand=True, padx=10, pady=10)
        except Exception as e:
            print(f"Error opening full image: {e}")



class ActionFrame(BaseFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._create_widgets()
        self.operational_limits_frame = None
        self.dispatch_control_frame = None

    def _create_widgets(self):
        self._create_run_button()
        self._create_gen_report_button()
        self._create_gen_csvs_button()
        self._create_pilot_viewer_button()

    def _create_run_button(self):
        self.run_button = ctk.CTkButton(
            self, text="Run",
            font=(Constants.FONT_NAME, Constants.BASE_FONT_SIZE),
            fg_color=Constants.FIELD_COLOR_DISABLED,
            text_color=Constants.TEXT_COLOR,
            bg_color=Constants.SECTION_BG,
            corner_radius=7,
            hover=False,
            command=self._run_process  
        )
        self.run_button.grid(row=0, column=0, padx=Constants.PAD_X, pady=Constants.PAD_Y, sticky='ew',)

    def _create_gen_report_button(self):
        self.gen_report_button = ctk.CTkButton(
            self, text="Gen Report",
            font=(Constants.FONT_NAME, Constants.BASE_FONT_SIZE),
            fg_color=Constants.FIELD_COLOR_DISABLED,
            bg_color=Constants.SECTION_BG,
            text_color=Constants.TEXT_COLOR,
            corner_radius=7,
            hover=False,
            state='disabled'  
        )
        self.gen_report_button.grid(row=0, column=1, padx=Constants.PAD_X, pady=Constants.PAD_Y, sticky='ew')

    def _create_gen_csvs_button(self):
        self.gen_csvs_button = ctk.CTkButton(
            self, text="Gen CSVs",
            font=(Constants.FONT_NAME, Constants.BASE_FONT_SIZE),
            fg_color=Constants.FIELD_COLOR_DISABLED,
            text_color=Constants.TEXT_COLOR,
            bg_color=Constants.SECTION_BG,
            corner_radius=7,
            hover=False,
            state='disabled'  
        )
        self.gen_csvs_button.grid(row=0, column=2, padx=Constants.PAD_X, pady=Constants.PAD_Y, sticky='ew')

    def _create_pilot_viewer_button(self):
        self.pilot_viewer_button = ctk.CTkButton(
            self, text="Pilot Viewer",
            font=(Constants.FONT_NAME, Constants.BASE_FONT_SIZE),
            fg_color=Constants.FIELD_COLOR_DISABLED,
            bg_color=Constants.SECTION_BG,
            text_color=Constants.TEXT_COLOR,
            corner_radius=7,
            hover=False,
            state='disabled'  
        )
        self.pilot_viewer_button.grid(row=0, column=3, padx=Constants.PAD_X, pady=Constants.PAD_Y, sticky='ew')

    def set_operational_limits_frame(self, frame):
        self.operational_limits_frame = frame

    def set_dispatch_control_frame(self, frame):
        self.dispatch_control_frame = frame

    def _validate_fields(self):
        if not self.operational_limits_frame or not self.dispatch_control_frame:
            return False

        
        operational_fields = [
            self.operational_limits_frame.max_soc_var,
            self.operational_limits_frame.min_soc_var,
            self.operational_limits_frame.initial_soc_var
        ]

        for field in operational_fields:
            if not field.get():
                return False
            
        if not self.operational_limits_frame._validate_initial_soc():
            return False

        
        if self.dispatch_control_frame.soc_steer_var.get():
            dispatch_fields = [
                entry.get() for entry in self.dispatch_control_frame.entries
            ]
            dispatch_fields.pop(0)
            dispatch_fields.pop(0)
            print(dispatch_fields)
            for field in dispatch_fields:
                if not field:
                    return False

        return True

    def _update_run_button(self):
        if self._validate_fields():
            self.run_button.configure(state='normal', fg_color=Constants.ACCENT_COLOR, hover=True, hover_color=Constants.ACCENT_COLOR, bg_color=Constants.SECTION_BG)
        else:
            self.run_button.configure(state='disabled', fg_color=Constants.FIELD_COLOR_DISABLED)

    def _run_process(self):
        """Simulate the run process and show a success popup."""
        
        self.run_button.configure(state='disabled')

        
        self.progress_bar = ctk.CTkProgressBar(self, mode='indeterminate',fg_color=Constants.ACCENT_COLOR,progress_color=Constants.TEXT_COLOR)
        self.progress_bar.grid(row=1, column=0, columnspan=4, padx=Constants.PAD_X, pady=Constants.PAD_Y, sticky='ew')
        self.progress_bar.start()

        
        threading.Thread(target=self._simulate_process, daemon=True).start()

    def _simulate_process(self):
        """Simulate a process with a delay and show the success popup."""
        time.sleep(3)  

        
        self.progress_bar.stop()
        self.progress_bar.grid_forget()

        
        self._show_success_popup()

        
        self.gen_report_button.configure(state='normal', fg_color=Constants.ACCENT_COLOR, hover=True, hover_color=Constants.ACCENT_COLOR)
        self.gen_csvs_button.configure(state='normal', fg_color=Constants.ACCENT_COLOR, hover=True, hover_color=Constants.ACCENT_COLOR)
        self.pilot_viewer_button.configure(state='normal', fg_color=Constants.ACCENT_COLOR, hover=True, hover_color=Constants.ACCENT_COLOR)

        
        self.run_button.configure(state='normal')

    def _show_success_popup(self):
        
        popup = tk.Toplevel(self)
        popup.title("Run Successful")
        popup.geometry("300x200")
        popup.resizable(False, False)

        
        success_label = tk.Label(
            popup, text="Run Successful!",
            font=(Constants.FONT_NAME, Constants.BASE_FONT_SIZE + 4),
            fg=Constants.ACCENT_COLOR
        )
        success_label.pack(pady=20)

        
        try:
            image = Image.open("imgs/success.png")  
            image = image.resize((50, 50), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            image_label = tk.Label(popup, image=photo)
            image_label.image = photo  
            image_label.pack(pady=10)
        except Exception as e:
            print(f"Error loading image: {e}")

        
        close_button = ctk.CTkButton(
            popup, text="Close",
            command=popup.destroy,
            height= 30,
            font=(Constants.FONT_NAME, Constants.BASE_FONT_SIZE),
            fg_color=Constants.ACCENT_COLOR,
            bg_color="white",
            text_color=Constants.TEXT_COLOR,
            corner_radius=7,
            hover=False,
          
        )

        close_button.pack(pady=10)