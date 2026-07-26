import customtkinter as ctk
from tkcalendar import Calendar
from datetime import datetime

class CalendarView(ctk.CTk):
    def __init__(self, categories, animal_list, initial_color):
        super().__init__()

        self.title("Goat Care Calendar")
        self.after(0, lambda: self.wm_state('zoomed'))

        self.on_add_animal_callback = None
        self.on_remove_animal_callback = None
        self.on_add_category_callback = None
        self.on_schedule_animal_callback = None
        self.on_gestation_animal_callback = None
        self.on_delete_task_callback = None
        self.on_color_pick_callback = None
        self.on_animal_changed_callback = None

        self.current_color = initial_color
        self.setup_layout(categories, animal_list)


    def setup_layout(self, categories, animal_list):
        self.grid_columnconfigure(0, weight=1, minsize=320)
        self.grid_columnconfigure(1, weight=2, minsize=550)
        self.grid_rowconfigure(0, weight=1)

        # ---- Left Sidebar ------ #
        self.sidebar = ctk.CTkScrollableFrame(self, corner_radius=15, label_text="Management Dashboard")
        self.sidebar.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        # ---- Animal Selection Dropdown ---- #
        self.animal_lbl = ctk.CTkLabel(self.sidebar, text="Select Animal Profile:", font=ctk.CTkFont(size=12, weight="bold"))
        self.animal_lbl.pack(pady=(10, 2), padx=15, anchor="w")

        self.animal_dropdown = ctk.CTkOptionMenu(self.sidebar, values=animal_list, command=self._internal_animal_selected)
        self.animal_dropdown.pack(pady=5, padx=15, fill="x")

        # ---- Add & Remove Animal ---- #
        self.new_animal_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Type new animal name...")
        self.new_animal_entry.pack(pady=(10, 5), padx=15, fill="x")

        self.color_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.color_frame.pack(pady=5, padx=15, fill="x")

        self.color_preview = ctk.CTkLabel(self.color_frame, text="", width=20, height=20,
                                          fg_color=self.current_color, corner_radius=5)
        self.color_preview.pack(side="left", padx=(0, 10))

        self.color_btn = ctk.CTkButton(self.color_frame, text="Pick Color", width=100, command=self._internal_choose_color)
        self.color_btn.pack(side="left", fill="x", expand=True)

        self.add_animal_btn = ctk.CTkButton(self.sidebar, text="➕ Save New Animal Profile",
                                            fg_color="#27ae60", hover_color="#2ecc71",
                                            command=self._internal_add_animal)
        self.add_animal_btn.pack(pady=5, padx=15, fill="x")

        self.remove_animal_btn = ctk.CTkButton(self.sidebar, text="Remove Selected Profile",
                                               fg_color="#c0392b", hover_color="#e74c3c",
                                               command=self._internal_remove_animal)
        self.remove_animal_btn.pack(pady=(0, 15), padx=15, fill="x")

        # ---- Need & Task Selection ---- #
        self.dropdown_label = ctk.CTkLabel(self.sidebar, text="Select Task Category:", font=ctk.CTkFont(size=12, weight="bold"))
        self.dropdown_label.pack(pady=(15, 2), padx=15, anchor="w")

        self.need_dropdown = ctk.CTkOptionMenu(self.sidebar, values=categories)
        self.need_dropdown.pack(pady=5, padx=15, anchor="w")

        self.custom_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Type new category name...")
        self.custom_entry.pack(pady=5, padx=15, fill="x")

        self.add_category_btn = ctk.CTkButton(self.sidebar, text="➕ Add to Task Drop-down",
                                              fg_color="#27ae60", hover_color="#2ecc71",
                                              command=self._internal_add_category)
        self.add_category_btn.pack(pady=5, padx=15, fill="x")

        # ---- Repeating Task Widget ---- #
        self.repeat_frame = ctk.CTkFrame(self.sidebar, corner_radius=10, border_width=1, border_color="#34495e")
        self.repeat_frame.pack(pady=(15, 5), padx=15, fill="x")

        self.repeat_title = ctk.CTkLabel(self.repeat_frame, text="Repeat Options", font=ctk.CTkFont(size=12, weight="bold"))
        self.repeat_title.pack(pady=(5, 2))

        self.repeat_var = ctk.StringVar(value="off")
        self.repeat_checkbox = ctk.CTkCheckBox(self.repeat_frame, text="Enable Recurring Task",
                                               variable=self.repeat_var, onvalue="on", offvalue="off",
                                               command=self.toggle_repeat_fields)
        self.repeat_checkbox.pack(pady=5, padx=15, anchor="w")

        self.repeat_inputs_frame = ctk.CTkFrame(self.repeat_frame, fg_color="transparent")

        self.freq_lbl = ctk.CTkLabel(self.repeat_inputs_frame, text="Frequency:")
        self.freq_lbl.pack(pady=2, padx=10, anchor="w")

        self.repeat_freq_dropdown = ctk.CTkOptionMenu(self.repeat_inputs_frame,
                                                      values=["Daily (Every Day)", "Weekly (Every Week)", "Monthly",
                                                              "Yearly"])
        self.repeat_freq_dropdown.pack(pady=2, padx=10, fill="x")

        self.duration_lbl = ctk.CTkLabel(self.repeat_inputs_frame, text="How many times to repeat?:")
        self.duration_lbl.pack(pady=2, padx=10, anchor="w")

        self.repeat_count_entry = ctk.CTkEntry(self.repeat_inputs_frame, placeholder_text="e.g. 7 (for a week of meds)")
        self.repeat_count_entry.pack(pady=(2, 8), padx=10, fill="x")

        self.add_btn = ctk.CTkButton(self.sidebar, text="🗓️ Schedule Task on Selected Date",
                                     command=self._internal_schedule_task, font=ctk.CTkFont(weight="bold"))
        self.add_btn.pack(pady=(15, 15), padx=15, fill="x")

        # ------------------ GESTATION CALCULATOR WIDGET ------------------
        self.gest_frame = ctk.CTkFrame(self.sidebar, corner_radius=10, border_width=1, border_color="#34495e")
        self.gest_frame.pack(pady=(20, 10), padx=15, fill="x")

        self.gest_lbl = ctk.CTkLabel(self.gest_frame, text="Goat Gestation Auto-Scheduler",
                                     font=ctk.CTkFont(size=13, weight="bold"))
        self.gest_lbl.pack(pady=5)

        self.gest_btn = ctk.CTkButton(self.gest_frame, text="Calculate & Add Due Date (+150 Days)",
                                      fg_color="#8e44ad", hover_color="#9b59b6",
                                      command=self._internal_gestation_clicked)
        self.gest_btn.pack(pady=(5, 10), padx=10, fill="x")

        # ------------------ RIGHT PANEL (Calendar & Display) ------------------
        self.main_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.main_panel.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")
        self.main_panel.grid_rowconfigure(0, weight=3)
        self.main_panel.grid_rowconfigure(1, weight=1)
        self.main_panel.grid_columnconfigure(0, weight=1)

        # Calendar Widget Integration
        self.cal = Calendar(self.main_panel, selectmode='day', date_pattern='yyyy-mm-dd',
                            font="Arial 18 bold", firstweekday="sunday", showweeknumbers=False,
                            background="#1f232a", foreground="white",
                            headersbackground="#2f3640", headersforeground="white",
                            selectbackground="#1f6aa5", selectforeground="white")
        self.cal.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Daily Tasks Agenda View Box
        self.agenda_frame = ctk.CTkScrollableFrame(self.main_panel, label_text="Scheduled Care Tasks")
        self.agenda_frame.grid(row=1, column=0, padx=5, pady=15, sticky="nsew")

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
        """Builds and displays tasks grouped under styled animal card widgets."""
        for widget in self.agenda_frame.winfo_children():
            widget.destroy()

        # --- MOVE THESE TWO LINES UP HERE (Above the 'if') ---
        date_obj = datetime.strptime(selected_date, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%B %d, %Y")

        if all_tasks:
            self.agenda_frame.configure(label_text=f"Tasks for {formatted_date} ({len(all_tasks)} Task(s) Scheduled)")

            # Group tasks by animal name mapping indices
            grouped_tasks = {}
            for original_index, item in enumerate(all_tasks):
                animal_name = item['animal']
                if animal_name not in grouped_tasks:
                    grouped_tasks[animal_name] = []
                grouped_tasks[animal_name].append((original_index, item))

            # Build Card Containers
            for animal_name, task_list in grouped_tasks.items():
                dot_color = animal_colors.get(animal_name, "#7f8c8d")

                animal_card = ctk.CTkFrame(self.agenda_frame, fg_color="#2c3e50", corner_radius=8)
                animal_card.pack(fill="x", padx=10, pady=6)

                header_row = ctk.CTkFrame(animal_card, fg_color="transparent")
                header_row.pack(fill="x", padx=10, pady=(8, 4))

                color_dot = ctk.CTkLabel(header_row, text="", width=14, height=14, fg_color=dot_color, corner_radius=7)
                color_dot.pack(side="left", padx=(0, 8))

                animal_title = ctk.CTkLabel(header_row, text=animal_name, font=ctk.CTkFont(size=15, weight="bold"),
                                            anchor="w")
                animal_title.pack(side="left", fill="x", expand=True)

                for original_index, item in task_list:
                    task_row = ctk.CTkFrame(animal_card, fg_color="transparent")
                    task_row.pack(fill="x", padx=15, pady=3)

                    label = ctk.CTkLabel(task_row, text=f"• {item['need']}", anchor="w", font=ctk.CTkFont(size=13))
                    label.pack(side="left", fill="x", expand=True)

                    del_btn = ctk.CTkButton(task_row, text="✕", width=25, height=20,
                                            fg_color="#c0392b", hover_color="#e74c3c", font=ctk.CTkFont(size=10),
                                            command=lambda i=original_index: self.on_delete_task_callback(
                                                i) if self.on_delete_task_callback else None)
                    del_btn.pack(side="right", padx=5)
        else:
            # Now 'formatted_date' works perfectly down here too!
            self.agenda_frame.configure(label_text=f"Tasks for {formatted_date} (0 Tasks)")
            no_tasks_lbl = ctk.CTkLabel(self.agenda_frame, text="No tasks scheduled for this day.", text_color="gray")
            no_tasks_lbl.pack(pady=15)

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