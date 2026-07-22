import customtkinter as ctk
from tkcalendar import Calendar
from datetime import datetime

# ----- save info --------- #
import json
import os


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

        self.animal_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Animal Name (e.g. Doug)")
        self.animal_entry.pack(pady=10, padx=15, fill="x")

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

        self.agenda_frame=ctk.CTkScrollableFrame(self.main_panel, label_text="Scheduled Care Tasks")
        self.agenda_frame.grid(row=1, column=0,padx=5, pady=15, sticky="nsew")

        self.update_agenda_view()

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
        selected_date = self.cal.get_date()
        animal = self.animal_entry.get().strip()
        need = self.need_dropdown.get()

        if animal and need:
            if selected_date not in self.events_db:
                self.events_db[selected_date] = []

            self.events_db[selected_date].append({"animal": animal, "need": need})

            self.save_data()

            self.animal_entry.delete(0, "end")
            self.need_entry.delete(0, "end")

            self.update_agenda_view()

    def update_agenda_view(self, event=None):
        selected_date = self.cal.get_date()

        for widget in self.agenda_frame.winfo_children():
            widget.destroy()

        date_obj = datetime.strptime(selected_date, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%B %d, %Y")
        self.agenda_frame.configure(label_text=f"Tasks for {formatted_date}")

        if selected_date in self.events_db and self.events_db[selected_date]:
            for index, item in enumerate(self.events_db[selected_date]):
                row_frame = ctk.CTkFrame(self.agenda_frame, fg_color="transparent")
                row_frame.pack(fill="x", padx=10, pady=4)

                task_text = f"{item['animal']}: {item['need']}"
                label = ctk.CTkLabel(self.agenda_frame, text=task_text, anchor="w", font=ctk.CTkFont(size=14))
                label.pack(fill="x", padx=10, pady=4)

                del_btn = ctk.CTkButton(row_frame, text="X", width=30, height=25,
                                        fg_color="#c0392b", hover_color="#e74c3c",
                                        command=lambda i = index: self.delete_event(i))
                del_btn.pack(side="right", padx=5)

        else:
            no_tasks_lbl = ctk.CTkLabel(self.agenda_frame, text="No tasks scheduled for the day.", text_color="gray")
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

# --------- save/load function -----------#
    def save_data(self):
        try:
            payload = {
                "events": self.events_db,
                "categories": self.categories
            }
            with open(self.DATA_FILE, "w") as f:
                json.dump(payload, f, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    def load_data(self):
        default_categories = ["Feeding", "Vet Checkup", "Medications", "Breeding"]

        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r") as f:
                    data = json.load(f)

                    if "events" in data and "categories" in data:
                        self.categories = data["categories"]
                        return data["events"]
                    else:
                        self.categories = default_categories
                        return data
            except Exception as e:
                print(f"Error loading data file, starting fresh: {e}")
                self.categories = default_categories
                return {}

        self.categories = default_categories
        return{}

if __name__ == "__main__":
    app = AnimalCalendar()
    app.mainloop()