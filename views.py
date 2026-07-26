import customtkinter as ctk
from tkcalendar import Calendar
from datetime import datetime

class CalendarView(ctk.CTk):
    def __init__(self, categories, animal_list, initial_color):
        super().__init__()

        self.withdraw()
        self.title("Goat Care Calendar")
        self.after(0, lambda:self.wm_state('zoomed'))


        self.on_add_animal_callback = None
        self.on_remove_animal_callback = None
        self.on_add_category_callback = None
        self.on_schedule_animal_callback = None
        self.on_gestation_animal_callback = None
        self.on_delete_task_callback = None
        self.on_color_pick_callback = None
        self.on_animal_changed_callback = None
        self.on_theme_toggle_callback = None

        self.current_color = initial_color
        self.setup_layout(categories, animal_list)

    def setup_layout(self, categories, animal_list):
        """Creates a Google Material 3-column layout: Left input, Center Calendar, Right Google Tasks panel."""
        # Configure layout split: Left Input (300px), Center Calendar (Weight 3), Right Tasks (320px)
        self.grid_columnconfigure(0, weight=0, minsize=310)  # Left Inputs
        self.grid_columnconfigure(1, weight=3, minsize=400)  # Center Google Calendar
        self.grid_columnconfigure(2, weight=0, minsize=330)  # Right Google Tasks panel
        self.grid_rowconfigure(0, weight=1)

        # Set main window background color to clean Google White
        self.configure(fg_color=("#ffffff", "#1a1a1a"))

        # ------------------ 1. LEFT SIDEBAR (Google Creation Panel) ------------------
        self.sidebar = ctk.CTkScrollableFrame(self, corner_radius=0, label_text="Goat Care Creator")
        self.sidebar.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        # Profile Dropdown
        self.animal_lbl = ctk.CTkLabel(self.sidebar, text="Select Animal Profile:", text_color="#5f6368",
                                       font=ctk.CTkFont(size=11, weight="bold"))
        self.animal_lbl.pack(pady=(15, 2), padx=15, anchor="w")

        self.animal_dropdown = ctk.CTkOptionMenu(self.sidebar, values=animal_list,
                                                 command=self._internal_animal_selected,
                                                 fg_color="#ffffff", text_color="#3c4043", button_color="#dadce0",
                                                 button_hover_color="#babeec")
        self.animal_dropdown.pack(pady=5, padx=15, fill="x")

        # New Profile Name input field
        self.new_animal_entry = ctk.CTkEntry(self.sidebar, placeholder_text="New animal name...",
                                             fg_color="#ffffff", border_color="#dadce0", text_color="#3c4043")
        self.new_animal_entry.pack(pady=5, padx=15, fill="x")

        # Color picker row
        self.color_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.color_frame.pack(pady=5, padx=15, fill="x")

        self.color_preview = ctk.CTkLabel(self.color_frame, text="", width=18, height=18,
                                          fg_color=self.current_color, corner_radius=9)  # Round dot
        self.color_preview.pack(side="left", padx=(0, 10))

        self.color_btn = ctk.CTkButton(self.color_frame, text="🎨 Choose Color", width=100,
                                       command=self._internal_choose_color,
                                       fg_color="#ffffff", text_color="#1a73e8", border_width=1, border_color="#dadce0",
                                       hover_color="#f1f3f4")
        self.color_btn.pack(side="left", fill="x", expand=True)

        self.add_animal_btn = ctk.CTkButton(self.sidebar, text="➕ Save Profile", font=ctk.CTkFont(weight="bold"),
                                            fg_color="#1a73e8", text_color="#ffffff", hover_color="#1557b0",
                                            command=self._internal_add_animal)
        self.add_animal_btn.pack(pady=5, padx=15, fill="x")

        self.remove_animal_btn = ctk.CTkButton(self.sidebar, text="🗑️ Remove Profile",
                                               fg_color="transparent", text_color="#d93025", hover_color="#fce8e6",
                                               command=self._internal_remove_animal)
        self.remove_animal_btn.pack(pady=(0, 15), padx=15, fill="x")

        # Categories selector
        self.dropdown_label = ctk.CTkLabel(self.sidebar, text="Task Category:", text_color="#5f6368",
                                           font=ctk.CTkFont(size=11, weight="bold"))
        self.dropdown_label.pack(pady=(15, 2), padx=15, anchor="w")

        self.need_dropdown = ctk.CTkOptionMenu(self.sidebar, values=categories, fg_color="#ffffff",
                                               text_color="#3c4043", button_color="#dadce0")
        self.need_dropdown.pack(pady=5, padx=15, fill="x")

        self.custom_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Create custom category...", fg_color="#ffffff",
                                         border_color="#dadce0", text_color="#3c4043")
        self.custom_entry.pack(pady=5, padx=15, fill="x")

        self.add_category_btn = ctk.CTkButton(self.sidebar, text="➕ Add Category",
                                              fg_color="#ffffff", text_color="#3c4043", border_width=1,
                                              border_color="#dadce0", hover_color="#f8f9fa",
                                              command=self._internal_add_category)
        self.add_category_btn.pack(pady=5, padx=15, fill="x")

        # Repeating setup frame layout
        self.repeat_frame = ctk.CTkFrame(self.sidebar, corner_radius=8, border_width=1, border_color="#dadce0",
                                         fg_color="#ffffff")
        self.repeat_frame.pack(pady=(15, 5), padx=15, fill="x")

        self.repeat_title = ctk.CTkLabel(self.repeat_frame, text="🔁 Repeat Options", text_color="#3c4043",
                                         font=ctk.CTkFont(size=12, weight="bold"))
        self.repeat_title.pack(pady=(5, 2))

        self.repeat_var = ctk.StringVar(value="off")
        self.repeat_checkbox = ctk.CTkCheckBox(self.repeat_frame, text="Repeat Task", text_color="#3c4043",
                                               variable=self.repeat_var, onvalue="on", offvalue="off",
                                               command=self.toggle_repeat_fields)
        self.repeat_checkbox.pack(pady=5, padx=10, anchor="w")

        self.repeat_inputs_frame = ctk.CTkFrame(self.repeat_frame, fg_color="transparent")

        self.freq_lbl = ctk.CTkLabel(self.repeat_inputs_frame, text="Frequency:", text_color="#5f6368")
        self.freq_lbl.pack(pady=2, padx=10, anchor="w")

        self.repeat_freq_dropdown = ctk.CTkOptionMenu(self.repeat_inputs_frame,
                                                      values=["Daily (Every Day)", "Weekly (Every Week)", "Monthly",
                                                              "Yearly"], fg_color="#ffffff", text_color="#3c4043",
                                                      button_color="#dadce0")
        self.repeat_freq_dropdown.pack(pady=2, padx=10, fill="x")

        self.duration_lbl = ctk.CTkLabel(self.repeat_inputs_frame, text="Repeat Count:", text_color="#5f6368")
        self.duration_lbl.pack(pady=2, padx=10, anchor="w")

        self.repeat_count_entry = ctk.CTkEntry(self.repeat_inputs_frame, placeholder_text="e.g. 7", fg_color="#ffffff",
                                               border_color="#dadce0", text_color="#3c4043")
        self.repeat_count_entry.pack(pady=(2, 8), padx=10, fill="x")

        self.add_btn = ctk.CTkButton(self.sidebar, text="🗓️ Schedule Task", fg_color="#1a73e8", text_color="#ffffff",
                                     hover_color="#1557b0", font=ctk.CTkFont(weight="bold"),
                                     command=self._internal_schedule_task)
        self.add_btn.pack(pady=(15, 10), padx=15, fill="x")

        # Gestation automation block
        self.gest_frame = ctk.CTkFrame(self.sidebar, corner_radius=8, border_width=1, border_color="#dadce0",
                                       fg_color="#ffffff")
        self.gest_frame.pack(pady=(15, 15), padx=15, fill="x")

        self.gest_lbl = ctk.CTkLabel(self.gest_frame, text="Goat Gestation Tracker", text_color="#3c4043",
                                     font=ctk.CTkFont(size=12, weight="bold"))
        self.gest_lbl.pack(pady=5)

        self.gest_btn = ctk.CTkButton(self.gest_frame, text="Calculate Due Date",
                                      fg_color="#7427cc", text_color="#ffffff", hover_color="#5b1eb0",
                                      command=self._internal_gestation_clicked)
        self.gest_btn.pack(pady=(2, 10), padx=10, fill="x")

        # ------------------ THEME MODE TOGGLE SWITCH ------------------
        self.theme_switch = ctk.CTkSwitch(self.sidebar, text="🌙 Dark Mode", command=self._internal_toggle_theme)
        self.theme_switch.pack(pady=(20, 10), padx=15, fill="x")

        if ctk.get_appearance_mode() == "Dark":
            self.theme_switch.select()

        # ------------------ 2. CENTER PANEL (Wide Canvas Google Calendar Grid) ------------------
        self.main_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.main_panel.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_panel.grid_rowconfigure(0, weight=1)
        self.main_panel.grid_columnconfigure(0, weight=1)

        is_dark = ctk.get_appearance_mode() == "Dark"
        cal_bg = "#2b2b2b" if is_dark else "#ffffff"
        cal_fg = "white" if is_dark else "#3c4043"
        cal_headers = "#202020" if is_dark else "#f0f0f0"
        cal_normal = "#1e1e1e" if is_dark else "#ffffff"

        # Google stylized Calendar Integration
        self.cal = Calendar(self.main_panel, selectmode='day', date_pattern='yyyy-mm-dd',
                            font="Arial 18 bold", firstweekday="sunday", showweeknumbers=False,
                            background=cal_bg, foreground=cal_fg, borderwidth=0,
                            headersbackground=cal_headers, headersforeground=cal_fg,
                            selectbackground="#1f6aa5", selectforeground="white",
                            normalbackground=cal_normal, normalforeground=cal_fg,
                            weekendbackground=cal_normal, weekendforeground="#ff7675")
        self.cal.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # ------------------ 3. RIGHT SIDEBAR (Google Tasks-style Dashboard) ------------------
        self.agenda_frame = ctk.CTkScrollableFrame(self, corner_radius=0, label_text="My Google Tasks",
                                                    border_width=1, border_color="#dadce0")
        self.agenda_frame.grid(row=0, column=2, padx=0, pady=0, sticky="nsew")

    def toggle_repeat_fields(self):
        """Toggles layout inputs on checkbox click."""
        if self.repeat_var.get() == "on":
            self.repeat_inputs_frame.pack(fill="x", before=self.repeat_checkbox)
        else:
            self.repeat_inputs_frame.pack_forget()

        # ------------------ INTERFACE ACTIONS (Relaying clicks to controller) ------------------

    def _internal_choose_color(self):
        from tkinter import colorchooser
        color_code = colorchooser.askcolor(title="Choose Animal Color")
        if color_code and self.on_color_pick_callback:
            self.on_color_pick_callback(color_code)

    def _internal_animal_selected(self, choice):
        if self.on_animal_changed_callback:
            self.on_animal_changed_callback(choice)

    def _internal_add_animal(self):
        if self.on_add_animal_callback:
            self.on_add_animal_callback()

    def _internal_remove_animal(self):
        if self.on_remove_animal_callback:
            self.on_remove_animal_callback()

    def _internal_add_category(self):
        if self.on_add_category_callback:
            self.on_add_category_callback()

    def _internal_schedule_task(self):
        if self.on_schedule_task_callback:
            self.on_schedule_task_callback()

    def _internal_gestation_clicked(self):
        if self.on_gestation_callback:
            self.on_gestation_callback()

        # ------------------ REFRESH / RENDERING PIPELINES ------------------

    def update_color_preview(self, hex_color):
        """Changes the sidebar preview circle color safely."""
        self.current_color = hex_color
        self.color_preview.configure(fg_color=hex_color)

    def render_agenda_view(self, selected_date, all_tasks, animal_colors):
        """Builds and displays tasks using a clean, minimalist Goat Tasks checkrow style."""
        for widget in self.agenda_frame.winfo_children():
            widget.destroy()

        date_obj = datetime.strptime(selected_date, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%B %d, %Y")

        if all_tasks:
            # Main Header Counter
            self.agenda_frame.configure(label_text=f"Tasks for {formatted_date} ({len(all_tasks)})")

            # Re-group task rows by animal names
            grouped_tasks = {}
            for original_index, item in enumerate(all_tasks):
                animal_name = item['animal']
                if animal_name not in grouped_tasks:
                    grouped_tasks[animal_name] = []
                grouped_tasks[animal_name].append((original_index, item))

            # Draw Material-style grouped list rows
            for animal_name, task_list in grouped_tasks.items():
                dot_color = animal_colors.get(animal_name, "#7f8c8d")

                # Goat Tasks category title block (borderless, clean white background)
                group_container = ctk.CTkFrame(self.agenda_frame, fg_color="transparent")
                group_container.pack(fill="x", padx=12, pady=(10, 2))

                # Small color chip badge next to animal header
                color_dot = ctk.CTkLabel(group_container, text="", width=10, height=10, fg_color=dot_color, corner_radius=5)
                color_dot.pack(side="left", padx=(2, 6))

                animal_title = ctk.CTkLabel(group_container, text=animal_name,
                                            font=ctk.CTkFont(size=13, weight="bold"), text_color="#3c4043", anchor="w")
                animal_title.pack(side="left", fill="x", expand=True)

                # Print clean, minimalist check-rows under the animal header
                for original_index, item in task_list:
                    task_row = ctk.CTkFrame(self.agenda_frame, fg_color="transparent")
                    task_row.pack(fill="x", padx=20, pady=2)

                    # Styled text label representing the needed care task
                    label = ctk.CTkLabel(task_row, text=f"○  {item['need']}",
                                         anchor="w", text_color="#5f6368", font=ctk.CTkFont(size=13))
                    label.pack(side="left", fill="x", expand=True)

                    # Deletion button restyled to look like a small hover action icon
                    del_btn = ctk.CTkButton(task_row, text="✕", width=20, height=20,
                                            fg_color="transparent", text_color="#70757a", hover_color="#f1f3f4",
                                            font=ctk.CTkFont(size=11),
                                            command=lambda i=original_index: self.on_delete_task_callback(i) if self.on_delete_task_callback else None)
                    del_btn.pack(side="right", padx=2)
        else:
            self.agenda_frame.configure(label_text="My Goat Tasks")
            no_tasks_lbl = ctk.CTkLabel(self.agenda_frame, text="All caught up!\nNo tasks scheduled for today.",
                                        text_color="#70757a", font=ctk.CTkFont(size=12))
            no_tasks_lbl.pack(pady=40, padx=20)

    def render_calendar_highlights(self, active_dates):
        """Wipes highlight layers and recolors squares with tasks active."""
        self.cal.calevent_remove('all')
        for date_str in active_dates:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                self.cal.calevent_create(date_obj, 'has_task', 'reminder')
            except ValueError:
                continue

        self.cal.tag_config('reminder', background='#2980b9', foreground='white')

    def _internal_toggle_theme(self):
        if self.on_theme_toggle_callback:
            self.on_theme_toggle_callback(self.theme_switch.get())