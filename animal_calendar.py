import customtkinter as ctk
from tkcalendar import Calendar
from datetime import datetime

# ----- save info --------- #
import json
import os

# --- for color chooser module --- #
from tkinter import colorchooser


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AnimalCalendar(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Goat Care Calendar")
        self.after(0, lambda: self.wm_state('zoomed'))

        self.DATA_FILE = "calendar_data.json"

        self.events_db = self.load_data()

        self.setup_layout()

    def setup_layout(self):
        self.grid_columnconfigure(0, weight=1, minsize=300)
        self.grid_columnconfigure(1, weight=2, minsize=550)
        self.grid_rowconfigure(0, weight=1)

        # -------- Left Sidebar for data entry ---------------- #
        self.sidebar = ctk.CTkFrame(self, corner_radius=15)
        self.sidebar.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        self.sidebar.label = ctk.CTkLabel(self.sidebar, text=" Add Care Schedule", font=ctk.CTkFont(size=18, weight="bold"))
        self.sidebar.label.pack(pady=15, padx=10)

        # ----- Animal Selection Dropdown ---- #
        self.animal_lbl = ctk.CTkLabel(self.sidebar, text="Select Animal:", font=ctk.CTkFont(size=12))
        self.animal_lbl.pack(pady=(10, 2), padx=15, anchor="w")

        animal_list = list(self.animal_colors.keys()) if self.animal_colors else ["No Animals Saved"]

        self.animal_dropdown = ctk.CTkOptionMenu(self.sidebar, values=animal_list, command=self.on_animal_selected)
        self.animal_dropdown.pack(pady=5, padx=15, fill="x")

        self.current_color = "#1f6aa5"
        if self.animal_colors:
            self.current_color = self.animal_colors[animal_list[0]]

        # ---- Add New Animal Interface ---------- #
        self.new_animal_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Type a new animal name...")
        self.new_animal_entry.pack(pady=(15, 5), padx=15, fill="x")

        self.color_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.color_frame.pack(pady=5, padx=15, fill="x")

        self.color_preview = ctk.CTkLabel(self.color_frame, text="", width=20, height=20,
                                          fg_color=self.current_color, corner_radius=5)
        self.color_preview.pack(side="left", padx=(0, 10))

        self.color_btn = ctk.CTkButton(self.color_frame, text="Pick a color",
                                       width=100, command=self.choose_color)
        self.color_btn.pack(side="left", fill="x", expand=True)

        self.add_animal_btn = ctk.CTkButton(self.sidebar, text="➕ Add New Animal Profile",
                                            fg_color="#27ae60", hover_color="#2ecc71",
                                            command=self.add_custom_animal)
        self.add_animal_btn.pack(pady=(2, 15), padx=15, fill="x")

        # --- Remove Animal Button ---- #
        self.remove_animal_btn = ctk.CTkButton(self.sidebar, text=" Remove Selected Profile",
                                               fg_color="#c0392b", hover_color="#e74c3c",
                                               command=self.delete_custom_animal)
        self.remove_animal_btn.pack(pady=(2, 10), padx=15, fill="x")



        # ----- drop down menu --------- #
        self.dropdown_label = ctk.CTkLabel(self.sidebar, text="Select Task Category:", font=ctk.CTkFont(size=12))
        self.dropdown_label.pack(pady=(10, 2), padx=15, anchor="w")

        self.menu_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.menu_frame.pack(pady=5, padx=15, fill="x")
        self.menu_frame.grid_columnconfigure(0, weight=1)

        self.need_dropdown = ctk.CTkOptionMenu(self.menu_frame, values=self.categories)
        self.need_dropdown.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        self.custom_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Type a new category here...")
        self.custom_entry.pack(pady=5, padx=15, fill="x")

        self.add_category_btn = ctk.CTkButton(self.sidebar, text="➕ Add to My Drop-down List",
                                              fg_color="#27ae60", hover_color="#2ecc71",
                                              command=self.add_custom_category)
        self.add_category_btn.pack(pady=(2, 10), padx=15, fill="x")

        self.add_btn = ctk.CTkButton(self.sidebar, text="Schedule Task", command=self.add_event, font=ctk.CTkFont(weight="bold"))
        self.add_btn.pack(pady=20, padx=15, fill="x")

        # ------- Repeating Task Widget ----- #
        self.repeat_frame = ctk.CTkFrame(self.sidebar, corner_radius=10, border_width=1, border_color="#34495e")
        self.repeat_frame.pack(pady=(15, 5), padx=15, fill="x")

        self.repeat_title = ctk.CTkLabel(self.repeat_frame, text="Repeat Options", font=ctk.CTkFont(size=12, weight="bold"))
        self.repeat_title.pack(pady=(5, 2))

        self.repeat_var = ctk.StringVar(value="off")
        self.repeat_checkbox = ctk.CTkCheckBox(self.repeat_frame, text="Enable Recurring Task",
                                               variable=self.repeat_var, onvalue="on", offvalue="off",
                                               command=self.toggle_repeat_fields)
        self.repeat_checkbox.pack(pady=5, padx=10, anchor="w")

        self.repeat_inputs_frame = ctk.CTkFrame(self.repeat_frame, fg_color="transparent")

        self.freq_lbl = ctk.CTkLabel(self.repeat_inputs_frame, text="Frequency:")
        self.freq_lbl.pack(pady=2, padx=10, anchor="w")

        self.repeat_freq_dropdown = ctk.CTkOptionMenu(self.repeat_inputs_frame, values=["Daily", "Weekly", "Monthly", "Yearly"])
        self.repeat_freq_dropdown.pack(pady=2, padx=10, fill="x")

        self.repeat_count_entry = ctk.CTkEntry(self.repeat_inputs_frame, placeholder_text="e.g. 7 (for a week of meds)")
        self.repeat_count_entry.pack(pady=(2, 8), padx=10, fill="x")

        # ------ Gestation Calculator ------- #
        self.gest_frame = ctk.CTkFrame(self.sidebar, corner_radius=10, border_width=1, border_color="#34495e")
        self.gest_frame.pack(pady=(10, 15), padx=15, fill="x")

        self.gest_lbl = ctk.CTkLabel(self.gest_frame, text="Goat Gestation Calculator", font=ctk.CTkFont(size=12, weight="bold"))
        self.gest_lbl.pack(pady=(5, 2))

        self.gest_btn = ctk.CTkButton(self.gest_frame, text="Calculate & Add Due Date(+150 Days)",
                                      fg_color="#8e44ad", hover_color="#9b59b6",
                                      command=self.calculate_gestation)
        self.gest_btn.pack(pady=(2, 10), padx=10, fill="x")

        # -------- Right Panel for Calendar and Displays ---------- #
        self.main_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.main_panel.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")
        self.main_panel.grid_rowconfigure(0, weight=3)
        self.main_panel.grid_rowconfigure(1, weight=1)
        self.main_panel.grid_columnconfigure(0, weight=1)

        self.cal = Calendar(self.main_panel, selectmode='day', date_pattern='yyyy-mm-dd',
                            font="Arial 18 bold", firstweekday="sunday",
                            background="#1f232a", foreground="white",
                            headersbackground="#2f3640", headersforeground="white",
                            selectbackground="#1f6aa5", selectforeground="white")
        self.cal.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.cal.bind("<<CalendarSelected>>", self.update_agenda_view)
        self.cal.bind("<<CalendarMonthChanged>>", lambda event: self.highlight_event_dates())

        self.agenda_frame=ctk.CTkScrollableFrame(self.main_panel, label_text="Scheduled Care Tasks")
        self.agenda_frame.grid(row=1, column=0,padx=5, pady=15, sticky="nsew")

        self.update_agenda_view()
        self.highlight_event_dates()

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose Animal Color")
        if color_code[1]:
            self.current_color = color_code[1]
            self.color_preview.configure(fg_color=self.current_color)

    def on_animal_selected(self, selected_animal):
        if selected_animal in self.animal_colors:
            self.current_color = self.animal_colors[selected_animal]
            self.color_preview.configure(fg_color=self.current_color)

    def add_custom_animal(self):
        new_name = self.new_animal_entry.get().strip()

        if new_name and new_name != "No Animals Saved":
            self.animal_colors[new_name] = self.current_color

            sorted_animals = sorted(list(self.animal_colors.keys()))

            self.animal_dropdown.configure(values=sorted_animals)
            self.animal_dropdown.set(new_name)

            self.new_animal_entry.delete(0, 'end')
            self.save_data()

    def delete_custom_animal(self):
        selected_animal = self.animal_dropdown.get()

        if selected_animal and selected_animal != "No Animals Saved":
            if selected_animal in self.animal_colors:
                del self.animal_colors[selected_animal]

        # ---- deletes events connected to that animal ---- #
            for date_str in list(self.events_db.keys()):
                updated_tasks = [task for task in self.events_db[date_str] if task["animal"] != selected_animal]

                if updated_tasks:
                    self.events_db[date_str] = updated_tasks
                else:
                    del self.events_db[date_str]

        remaining_animals = sorted(list(self.animal_colors.keys()))

        if remaining_animals:
            self.animal_dropdown.configure(values=remaining_animals)
            self.animal_dropdown.set(remaining_animals[0])
            self.on_animal_selected(remaining_animals[0])
        else:
            self.animal_dropdown.configure(values=["No Animals Saved"])
            self.animal_dropdown.set("No Animals Saved")
            self.current_color = "#1f6aa5"
            self.color_preview.configure(fg_color=self.current_color)

            self.save_data()
            self.update_agenda_view()
            self.highlight_event_dates()

    def add_custom_category(self):
        new_cat = self.custom_entry.get().strip()

        if new_cat and new_cat not in self.categories:
            self.categories.append(new_cat)
            self.categories.sort()

            self.need_dropdown.configure(values = self.categories)
            self.need_dropdown.set(new_cat)

            self.custom_entry.delete(0, 'end')
            self.save_data()

    def add_event(self):
        from datetime import timedelta

        selected_date_str = self.cal.get_date()
        animal = self.animal_dropdown.get()
        need = self.need_dropdown.get()

        if not animal or animal == "No Animals Saved" or not need:
            return

        dates_to_schedule = [selected_date_str]

        if self.repeat_var.get() == "on":
            try:
                raw_count = self.repeat_count_entry.get().strip()
                repeat_count = int(raw_count) if raw_count.isdigit() else 1

                freq_choice = self.repeat_freq_dropdown.get()
                if "Daily" in freq_choice:
                    days_steps = 1
                elif "Weekly" in freq_choice:
                    days_steps = 7
                elif "Monthly" in freq_choice:
                    days_steps = 30
                else:
                    days_steps = 365

                base_date= datetime.strptime(selected_date_str, "%Y-%m-%d")

                for i in range(1, repeat_count):
                    future_date = base_date + timedelta(days=i * days_steps)
                    dates_to_schedule.append(future_date.strftime("%Y-%m-%d"))

            except Exception as e:
                print(f"Error calculating repeat dates: {e}")

        for target_date in dates_to_schedule:
            if target_date not in self.events_db:
                self.events_db[target_date] = []
            self.events_db[target_date].append({"animal": animal, "need": need})

        self.save_data()
        self.update_agenda_view()
        self.highlight_event_dates()

        self.repeat_var.set("off")
        self.repeat_count_entry.delete(0, 'end')
        self.toggle_repeat_fields()

    # --- Gestation Calulations ----- #
    def calculate_gestation(self):
        from datetime import timedelta

        selected_date_str = self.cal.get_date()
        animal = self.animal_dropdown.get()

        if not animal or animal == "No Animals Saved":
            return

        start_date = datetime.strptime(selected_date_str, "%Y-%m-%d")

        due_date = start_date + timedelta(days=150)
        due_date_str = due_date.strftime("%Y-%m-%d")

        if selected_date_str not in self.events_db:
            self.events_db[selected_date_str] = []
        self.events_db[selected_date_str].append({"animal": animal, "need": "Bred"})

        if due_date not in self.events_db:
            self.events_db[due_date_str] = []
        self.events_db[due_date_str].append({"animal": animal, "need": "Expected Kidding Due Date!"})

        self.save_data()
        self.update_agenda_view()
        self.highlight_event_dates()

    def update_agenda_view(self, event=None):
        selected_date = self.cal.get_date()

        for widget in self.agenda_frame.winfo_children():
            widget.destroy()

        date_obj = datetime.strptime(selected_date, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%B %d, %Y")

        if selected_date in self.events_db and self.events_db[selected_date]:
            all_tasks = self.events_db[selected_date]
            task_count = len(all_tasks)
            self.agenda_frame.configure(label_text=f"Tasks for {formatted_date} ({task_count} Task(s) Scheduled)")

            grouped_tasks = {}
            for original_index, item in enumerate(all_tasks):
                animal_name = item['animal']
                if animal_name not in grouped_tasks:
                    grouped_tasks[animal_name] = []
                grouped_tasks[animal_name].append((original_index, item))

            for animal_name, task_list in grouped_tasks.items():
                dot_color = self.animal_colors.get(animal_name, "#7f8c8d")

                animal_card = ctk.CTkFrame(self.agenda_frame, fg_color="#2c3e50", corner_radius=8)
                animal_card.pack(fill="x", padx=10, pady=6)

                header_row = ctk.CTkFrame(animal_card, fg_color="transparent")
                header_row.pack(fill="x", padx=10, pady=(8, 4))

                color_dot = ctk.CTkLabel(header_row, text="", width=14, height=14,
                                         fg_color=dot_color, corner_radius=7)
                color_dot.pack(side="left", padx=(0, 8))

                animal_title = ctk.CTkLabel(header_row, text=animal_name,
                                            font=ctk.CTkFont(size=15, weight="bold"), anchor="w")
                animal_title.pack(side="left", fill="x", expand=True)

                for original_index, item in task_list:
                    task_row = ctk.CTkFrame(animal_card, fg_color="transparent")
                    task_row.pack(fill="x", padx=15, pady=3)

                    label = ctk.CTkLabel(task_row, text=f"• {item['need']}",
                                         anchor="w", font=ctk.CTkFont(size=13))
                    label.pack(side="left", fill="x", expand=True)

                    del_btn = ctk.CTkButton(task_row, text="X", width=25, height=20,
                                            fg_color="#c0392b", hover_color="#e74c3c",
                                            font=ctk.CTkFont(size=10),
                                            command=lambda i=original_index: self.delete_event(i))
                    del_btn.pack(side="right", padx=5)

        else:
            self.agenda_frame.configure(label_text=f"Tasks for {formatted_date} (0 Tasks)")
            no_tasks_lbl = ctk.CTkLabel(self.agenda_frame, text="No tasks scheduled for today.", text_color="gray")
            no_tasks_lbl.pack(pady=15)

# ------ delete button for tasks that aren't needed ----- #
    def delete_event(self, task_index):
        selected_date = self.cal.get_date()

        if selected_date in self.events_db:
            self.events_db[selected_date].pop(task_index)

            if not self.events_db[selected_date]:
                del self.events_db[selected_date]

            self.save_data()

            self.update_agenda_view()
            self.highlight_event_dates()

# ---- highlights events on calendar ---- #
    def highlight_event_dates(self):
        self.cal.calevent_remove('all')

        for date_str, tasks in self.events_db.items():
            if not tasks:
                continue

            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")

                task_count = len(tasks)
                animal_names = ", ".join(set(item['animal'] for item in tasks))
                hover_text = f"{task_count} Task(s): {animal_names}"

                self.cal.calevent_create(date_obj, hover_text, 'reminder')
            except ValueError:
                continue

        self.cal.tag_config('reminder', background='#2980b9', foreground='white')

    def toggle_repeat_fields(self):
        if self.repeat_var.get() == "on":
            self.repeat_inputs_frame.pack(fill="x", before=self.repeat_checkbox)
        else:
            self.repeat_inputs_frame.pack_forget()

# --------- save/load function -----------#
    def save_data(self):
        try:
            payload = {
                "events": self.events_db,
                "categories": self.categories,
                "animal_colors": self.animal_colors
            }
            with open(self.DATA_FILE, "w") as f:
                json.dump(payload, f, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    def load_data(self):
        default_categories = ["Feeding", "Vet Checkup", "Medication", "Breeding"]

        self.animal_colors = {}

        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r") as f:
                    data = json.load(f)

                    if isinstance(data, dict) and "events" in data:
                        self.categories = data.get("categories", default_categories)
                        self.animal_colors = data.get("animal_colors", {})
                        return data["events"]
                    else:
                        self.categories = default_categories
                        return data

            except Exception as e:
                print(f"Error loading data, starting fresh: {e}")
                self.categories = default_categories
                return {}

        self.categories = default_categories
        return {}

if __name__ == "__main__":
    app = AnimalCalendar()
    app.mainloop()