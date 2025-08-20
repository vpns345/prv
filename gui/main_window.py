import sys
import threading
import asyncio
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QListWidget, QPushButton, QHBoxLayout, QMessageBox, QFormLayout, QLineEdit, QSpinBox
)
from PyQt6.QtCore import pyqtSignal, QObject

from engine.profile_manager import load_profiles, delete_profile, create_profile, update_profile
from engine.launcher import launch_browser
from engine.async_manager import async_manager
from gui.profile_dialog import ProfileDialog
from gui.config_window import ConfigWindow
from gui.bulk_create_dialog import BulkCreateDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AbdullahBot")
        self.setGeometry(100, 100, 800, 600)
        self.async_manager = async_manager
        self.browsers = [] # This will store browser contexts

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.profile_list = QListWidget()
        self.profile_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.layout.addWidget(self.profile_list)

        # Automation Panel
        self.automation_form = QFormLayout()
        self.target_url_input = QLineEdit()
        self.num_threads_input = QSpinBox()
        self.num_threads_input.setRange(1, 1000) # Increased limit
        self.num_threads_input.setValue(3)
        self.start_automation_btn = QPushButton("Start Automation")

        self.automation_form.addRow("Target URL:", self.target_url_input)
        self.automation_form.addRow("Number of Threads:", self.num_threads_input)
        self.automation_form.addRow(self.start_automation_btn)
        self.layout.addLayout(self.automation_form)

        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)

        self.create_btn = QPushButton("Create New Profile")
        self.bulk_create_btn = QPushButton("Bulk Create Profiles")
        self.launch_btn = QPushButton("Launch Selected Profile")
        self.configure_btn = QPushButton("Configure Selected Profile")
        self.delete_btn = QPushButton("Delete Selected Profile")

        self.button_layout.addWidget(self.create_btn)
        self.button_layout.addWidget(self.bulk_create_btn)
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.launch_btn)
        self.button_layout.addWidget(self.configure_btn)
        self.button_layout.addWidget(self.delete_btn)

        self.create_btn.clicked.connect(self.create_new_profile)
        self.bulk_create_btn.clicked.connect(self.bulk_create_profiles)
        self.launch_btn.clicked.connect(self.launch_selected_profile)
        self.configure_btn.clicked.connect(self.configure_selected_profile)
        self.delete_btn.clicked.connect(self.delete_selected_profile)
        self.start_automation_btn.clicked.connect(self.start_automation)

        self.load_profiles_to_list()

    def create_new_profile(self):
        dialog = ProfileDialog(self)
        if dialog.exec():
            profile_name = dialog.get_profile_name()
            profile_type = dialog.get_profile_type()
            if profile_name:
                try:
                    create_profile(profile_name, profile_type)
                    self.load_profiles_to_list()
                except ValueError as e:
                    QMessageBox.warning(self, "Error", str(e))

    def bulk_create_profiles(self):
        dialog = BulkCreateDialog(self)
        if dialog.exec():
            values = dialog.get_values()
            prefix = values["prefix"]
            count = values["count"]

            for i in range(1, count + 1):
                profile_name = f"{prefix}{i}"
                try:
                    # For bulk creation, we'll default to Desktop profiles
                    create_profile(profile_name, "Desktop")
                except ValueError as e:
                    # Maybe show one big message at the end, for now, just print
                    print(f"Could not create profile {profile_name}: {e}")

            self.load_profiles_to_list()
            QMessageBox.information(self, "Success", f"{count} profiles created.")

    def launch_selected_profile(self):
        profile_name = self.get_selected_profile_name()
        if profile_name:
            profiles = load_profiles()
            profile = next((p for p in profiles if p["name"] == profile_name), None)
            if profile:
                self.launch_browser_task(profile)

    def start_automation(self):
        target_url = self.target_url_input.text()
        if not target_url:
            QMessageBox.warning(self, "Warning", "Please enter a target URL.")
            return
        selected_profile_names = self.get_selected_profile_names()
        if not selected_profile_names:
            return

        profiles = load_profiles()
        profiles_to_launch = [p for p in profiles if p["name"] in selected_profile_names]

        for profile in profiles_to_launch:
            # The threading is now handled by the async manager scheduler
            self.launch_browser_task(profile, target_url)

    def launch_browser_task(self, profile, url=None):
        future = self.async_manager.schedule(launch_browser(profile, start_url=url))
        future.add_done_callback(self.on_browser_launched)

    def on_browser_launched(self, future):
        try:
            browser_context, page = future.result()
            self.browsers.append(browser_context)
            # We can't easily show a success message for each one without being spammy.
            # A status bar or log would be better in a future version.
            print(f"Successfully launched browser for profile: {browser_context.options.get('user_data_dir')}")
        except Exception as e:
            # Still can't show a QMessageBox from a non-main thread easily.
            print(f"Error launching browser: {e}")

    def get_selected_profile_names(self):
        selected_items = self.profile_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select one or more profiles.")
            return []
        return [item.text() for item in selected_items]

    def get_selected_profile_name(self):
        selected_names = self.get_selected_profile_names()
        if not selected_names:
            return None
        if len(selected_names) > 1:
            QMessageBox.warning(self, "Warning", "Please select only one profile for this action.")
            return None
        return selected_names[0]

    def delete_selected_profile(self):
        profile_name = self.get_selected_profile_name()
        if profile_name:
            reply = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete profile '{profile_name}'?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                delete_profile(profile_name)
                self.load_profiles_to_list()

    def load_profiles_to_list(self):
        self.profile_list.clear()
        profiles = load_profiles()
        for profile in profiles:
            self.profile_list.addItem(profile["name"])

    def closeEvent(self, event):
        # Clean up resources
        for browser in self.browsers:
            self.async_manager.schedule(browser.close())
        self.async_manager.shutdown()
        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
