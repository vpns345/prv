import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QListWidget, QPushButton, QHBoxLayout, QMessageBox
)

from PyQt6.QtWidgets import QInputDialog
from browser.profile_manager import load_profiles, delete_profile, create_profile, update_profile
from browser.launcher import launch_browser
from gui.profile_dialog import ProfileDialog
from gui.config_window import ConfigWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Anti-Detect Browser")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.drivers = []

        self.profile_list = QListWidget()
        self.layout.addWidget(self.profile_list)

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

        self.load_profiles_to_list()

    def create_new_profile(self):
        dialog = ProfileDialog(self)
        if dialog.exec():
            profile_name = dialog.get_profile_name()
            if profile_name:
                try:
                    create_profile(profile_name)
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

    def get_selected_profile_name(self):
        selected_items = self.profile_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a profile.")
            return None
        return selected_items[0].text()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
