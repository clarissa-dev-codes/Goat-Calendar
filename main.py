from models import CalendarModel
from views import CalendarView

class CalendarController:
    def __init__(self):
        self.model = CalendarModel()

        animal_list = list(self.model.animal_colors.key()) if self.model.animal_colors else ["No Animals Saved"]
        initial_color = "#1f6aa5"
        if self.model.animal_colors:
            initial_color = self.model.animal_colors[animal_list[0]]

        self.view = CalendarView(self.model.categories, animal_list, initial_color)

        self.view.on_color_pick_callback = self.handle_color_pick
        self.view.on_animal_changed_callback = self.handle_animal_changed
        self.view.on_add_animal_callback = self.handle_add_animal
        self.view.on_remove_animal_callback = self.handle_remove_animal
        self.view.on_add_category_callback = self.handle_add_category
        self.view.on_schedule_task_callback = self.handle_schedule_task
        self.view.on_gestation_callback = self.handle_gestation_calculation
        self.view.on_delete_task_callback = self.handle_delete_task

        self.view.cal.bind("<<CalendarSelected>>", lambda e: self.refresh_agenda())
        self.view.cal.bind("<<CalendarMonthChanged>>", lambda e: self.view.render_calendar_highlights(self.model.events_db.keys()))
        self.refresh_agenda()
        self.view.render_calendar_highlights(self.model.events_db.keys())


    # ---- Event Handlers ---- #
    def handle_color_pick(self, color_code):
        self.view.upate_color_preview(color_code)

    def handle_animal_changed(self, selected_animal):
        if selected_animal in self.model.animal_colors:
            color = self.model.animal_colors[selected_animal]
            self.view.update_color_preview(color)

    def handle_add_animal(self):
        name = self.view.new_animal_entry.get().strip()
        color = self.view.current_color

        if self.model.add_animal_profile(name, color):
            sorted_animals = sorted(list(self.model.animal_colors.keys()))
            self.view.animal_dropdown.configure(values=sorted_animals)
            self.view.animal_dropdown.set(name)
            self.view.new_animal_entry.delete(0, "end")

    def handle_remove_animal(self):
        selected_animal = self.view.animal_dropdown.get()
        if selected_animal and selected_animal != "No Animals Saved":
            self.model.delete_animal_profile(selected_animal)

        remaining = sorted(list(self.model.animal_colors.keys()))
        if remaining:
            self.view.animal_dropdown.configure(values=remaining)
            self.view.animal_dropdown.set(remaining[0])
            self.handle_animal_changed(remaining[0])
        else:
            self.view.animal_dropdown.configure(values=["No Animals Saved"])
            self.view.animal_dropdown.set("No Animals Saved")
            self.view.update_color_preview("#1f6aa5")

        self.refresh_agenda()
        self.view.render_calendar_highlights(self.model.events_db.keys())

    def handle_add_category(self):
        new_animal = self.view.custom_entry.get().strip()
        if self.model.add_custom_category(new_animal):
            self.view.need_dropdown.configure(values=self.model.categories)
            self.view.need_dropdown.set(new_animal)
            self.view.custom_entry.delete(0, "end")

    def handle_schedule_task(self):
        date_str = self.view.cal.get_date()
        animal = self.view.animal_dropdown.get()
        need = self.view.need_dropdown.get()
        repeat_on = self.view.repeat_var.get()
        repeat_freq = self.view.repeat_freq_dropdown.get()
        repeat_count = self.view.repeat_count_entry.get().strip()

        if self.model.add_event(date_str, animal, need, repeat_on, repeat_freq, repeat_count):
            self.refresh_agenda()
            self.view.render_calendar_highlights(self.model.events_db.keys())

            self.view.repeat_var.set("off")
            self.view.repeat_count_entry.delete(0, "end")
            self.view.toggle_repeat_fields()

    def handle_gestation_calculation(self):
        date_str = self.view.cal.get_date()
        animal = self.view.animal_dropdown.get()

        if self.model.calculate_gestation(date_str, animal):
            self.refresh_agenda()
            self.view.render_calendar_highlights(self.model.events_db.keys())

    def handle_delete_task(self, task_index):
        date_str = self.view.cal.get_date()
        if self.model.delete_event(date_str, task_index):
            self.refresh_agenda()
            self.view.render_calendar_highlights(self.model.events_db.keys())

    def refresh_agenda(self):
        date_str = self.view.cal.get_date()
        day_tasks = self.model.events_db.get(date_str, [])
        self.view.render_agenda_view(date_str, day_tasks, self.model.animal_colors)


if __name__ == "__main__":
    app_controller = CalendarController()
    app_controller.view.mainloop()