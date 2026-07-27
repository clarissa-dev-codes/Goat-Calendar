# Goat Care Scheduler

A professional, high-performance desktop scheduling application designed to streamline herd management, herd breeding timelines, and daily animal care tasks. Built using Python, CustomTkinter, and structured around the clean Model-View-Controller (MVC) software architecture pattern

---
## Key Features
- Modular Architecture: Fully refactored codebase using the MVC pattern to isolate business data logic from the presentation interface layer.
- Dynamic Repeating Tasks: Supports multi-interval recurring schedule algorithms (`Daily`, `Weekly`, `Monthly`, `Yearly`) to quickly log long-term cycles like medication runs or routine feeding operations.
- Goat Gestation Scheduler: Features an automated timeline calculation engine that accepts a baseline mating date and automatically schedules a kidding alert precisely 150 days into the future.
- Custom Profile Coding: Allows users to create personalized animal profiles and custom task categories linked to custom hex color indicators for fast daily filtering.
- Data Persistence Layer: Features automated data tracking mapping to a clean, lightweight local JSON repository file to preserve user configurations across sessions.

---
## Software Architecture Blueprint
The application shifts responsibilities across three independent file modules to ensure maximum maintainability and cleaner scalability options:
Project Root
┣ main.py       <-- The Controller: Orchestrates state updates and binds interface hooks.
┣ models.py     <-- The Model: Governs JSON reads/writes and date step calculations.
┣ views.py      <-- The View: Structures the CustomTkinter frames and layout parameters.
┗ README.md     <-- Documentation manual repository overview guide.

---
## Installation & Deployment
Follow these quick commands to spin up the desktop application container inside your local terminal workspace environment:
(Please note that this has only been tested and used on a Windows os)

1. **Clone the Repository:**
   ```bash
   git clone https://github.com
   cd goat-care-calendar
   ```

2. **Set Up a Virtual Environment (Recommended):**
   ```bash
   python -m venv .venv
   # Activate on Windows:
   .venv\Scripts\activate
   # Activate on Mac/Linux:
   source .venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install customtkinter tkcalendar
   ```

4. **Launch the Engine:**
   ```bash
   python main.py
   ```

   ---
   ## Future Enhancement Roadmap
   - Relational Engine Upgrade: Migrate data pipeline storage layers from a text-based JSON architecture to an embedded local SQLite database
   - Automated Push Notifications: Implement desktop popup reminders or SMTP email whenever a critical care task is due that day
