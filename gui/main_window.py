import sys
import threading
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QListWidget, QPushButton, QHBoxLayout, QMessageBox, QFormLayout, QLineEdit, QSpinBox
)

from PyQt6.QtWidgets import QInputDialog
from browser.profile_manager import load_profiles, delete_profile, create_profile, update_profile
from browser.launcher import launch_browser
from gui.profile_dialog import ProfileDialog
from gui.config_window import ConfigWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AbdullahBot")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.drivers = []

        self.profile_list = QListWidget()
        self.profile_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.layout.addWidget(self.profile_list)

        # Automation Panel
        self.automation_form = QFormLayout()
        self.target_url_input = QLineEdit()
        self.num_threads_input = QSpinBox()
        self.num_threads_input.setRange(1, 10)
        self.num_threads_input.setValue(1)
        self.start_automation_btn = QPushButton("Start Automation")

        self.automation_form.addRow("Target URL:", self.target_url_input)
        self.automation_form.addRow("Number of Threads:", self.num_threads_input)
        self.automation_form.addRow(self.start_automation_btn)
        self.layout.addLayout(self.automation_form)

        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)

        self.create_btn = QPushButton("Create New Profile")
        self.launch_btn = QPushButton("Launch Selected Profile")
        self.configure_btn = QPushButton("Configure Selected Profile")
        self.delete_btn = QPushButton("Delete Selected Profile")

        self.button_layout.addWidget(self.create_btn)
        self.button_layout.addWidget(self.launch_btn)
        self.button_layout.addWidget(self.configure_btn)
        self.button_layout.addWidget(self.delete_btn)

        self.create_btn.clicked.connect(self.create_new_profile)
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

    def launch_selected_profile(self):
        profile_name = self.get_selected_profile_name()
        if profile_name:
            profiles = load_profiles()
            profile = next((p for p in profiles if p["name"] == profile_name), None)
            if profile:
                try:
                    driver = launch_browser(profile)
                    self.drivers.append(driver)  # Keep reference
                    QMessageBox.information(self, "Success", f"Launched browser for profile '{profile_name}'.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to launch browser: {e}")

    def configure_selected_profile(self):
        profile_name = self.get_selected_profile_name()
        if profile_name:
            profiles = load_profiles()
            profile = next((p for p in profiles if p["name"] == profile_name), None)
            if profile:
                dialog = ConfigWindow(profile, self)
                if dialog.exec():
                    updated_profile = dialog.get_profile()
                    update_profile(updated_profile)
                    QMessageBox.information(self, "Success", "Profile updated successfully.")

    def delete_selected_profile(self):
        profile_name = self.get_selected_profile_name()
        if profile_name:
            reply = QMessageBox.question(
                self, "Confirm Delete",
                f"Are you sure you want to delete profile '{profile_name}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                delete_profile(profile_name)
                self.load_profiles_to_list()

    def load_profiles_to_list(self):
        self.profile_list.clear()
        profiles = load_profiles()
        for profile in profiles:
            self.profile_list.addItem(profile["name"])

    def start_automation(self):
        target_url = self.target_url_input.text()
        if not target_url:
            QMessageBox.warning(self, "Warning", "Please enter a target URL.")
            return

        selected_profile_names = self.get_selected_profile_names()
        if not selected_profile_names:
            return

        num_threads = self.num_threads_input.value()

        profiles = load_profiles()
        profiles_to_launch = [p for p in profiles if p["name"] in selected_profile_names]

        for i in range(0, len(profiles_to_launch), num_threads):
            batch = profiles_to_launch[i:i+num_threads]
            threads = []
            for profile in batch:
                thread = threading.Thread(target=self.launch_browser_thread, args=(profile, target_url))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join() # This will run batches sequentially, can be improved later

    def launch_browser_thread(self, profile, url):
        try:
            driver = launch_browser(profile, start_url=url)
            self.drivers.append(driver)
        except Exception as e:
            # Since this is in a thread, we can't show a QMessageBox easily.
            # Print the error to the console for now.
            print(f"Error launching profile {profile['name']}: {e}")

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
