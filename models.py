import json
import os
from datetime import datetime, timedelta

class CalendarModel:
    def __init__(self):
        self.DATA_FILE = "calendar_data.json"
        self.default_categories = ["Feeding", "Vet Checkup", "Medication", "Breeding"]
        self.categories = []
        self.animal_colors = {}
        self.events_db = {}

        self.load_data()

    # --- Loads data in ---- #
    def load_data(self):
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r") as f:
                    data = json.load(f)
                    if isinstance(data, dict) and "events" in data:
                        self.categories = data.get("categories", self.default_categories)
                        self.animal_colors = data.get("animal_colors", {})
                        self.events_db = data.get("events_db", {})
                        return
            except Exception as e:
                print(f"Error loading file, starting fresh: {e}")

        self.categories = list(self.default_categories)
        self.animal_colors = {}
        self.events_db = {}

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

    def add_animal_profile(self, name, color):
        if name and name != "No Animals Saved":
            self.animal_colors[name] = color
            self.save_data()
            return True
        return False

    def delete_animal_profile(self, name):
        if name in self.animal_colors:
            del self.animal_colors[name]

        for date_str in list(self.events_db.keys()):
            updated_tasks = [task for task in self.events_db[date_str] if task["animal"] != name]
            if updated_tasks:
                self.events_db[date_str] = updated_tasks
            else:
                del self.events_db[date_str]

        self.save_data()

    def add_custom_category(self, category_name):
        if category_name and category_name not in self.categories:
            self.categories.append(category_name)
            self.categories.sort()
            self.save_data()
            return True
        return False

    def add_event(self, date_str, animal, need, repeat_on, repeat_freq, repeat_count_str):
        if not animal or animal == "No Animals Saved" or not need:
            return False

        dates_to_schedule = [date_str]

        if repeat_on == ("on"):
            try:
                repeat_count = int(repeat_count_str) if repeat_count_str.isdigit() else 1
                if "Daily" in repeat_freq:
                    days_step = 1
                elif "Weekly" in repeat_freq:
                    days_step = 7
                elif "Monthly" in repeat_freq:
                    days_step = 30
                else:
                    days_step = 356

                base_date = datetime.strptime(date_str, "%Y-%m-%d")

                for i in range(1, repeat_count):
                    future_date = base_date + timedelta(days=i * days_step)
                    dates_to_schedule.append(future_date.strftime("%Y-%m-%d")
                                             )
            except Exception as e:
                print(f"Error calculating repeat count: {e}")

        for target_date in dates_to_schedule:
            if target_date not in self.events_db:
                self.events_db[target_date] = []
            self.events_db[target_date].append({"animal": animal, "need": need})

        self.save_data()
        return True

    def calculate_gestation(self, date_str, animal):
        if not animal or animal == "No Animals Saved":
            return False

        start_date = datetime.strptime(date_str, "%Y-%m-%d")
        due_date = start_date + timedelta(days=150)
        due_date_str = due_date.strftime("%Y-%m-%d")

        if date_str not in self.events_db:
            self.events_db[date_str] = []
        self.events_db[date_str].append({"animal": animal, "need": "Bred"})

        if due_date_str not in self.events_db:
            self.events_db[due_date_str] = []
        self.events_db[due_date_str].append({"animal": animal, "need": "Expecting kidding due date!"})

        self.save_data()
        return True

    def delete_event(self, date_str, task_index):
        if date_str in self.events_db:
            self.events_db[date_str].pop(task_index)
            if not self.events_db[date_str]:
                del self.events_db[date_str]
            self.save_data()
            return True
        return False