import json
import random
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel,
    QFormLayout, QSpinBox, QCheckBox, QHBoxLayout, QMessageBox, QComboBox
)
from utils import get_geo_from_proxy


with open("user_agents.json", "r") as f:
    USER_AGENTS = json.load(f)


class ConfigWindow(QDialog):
    def __init__(self, profile, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Configure Profile: {profile['name']}")
        self.profile = profile

        self.layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()

        # User Agent Widgets
        self.ua_label = QLabel("User-Agent:")
        self.user_agent_combo = QComboBox()
        self.randomize_ua_btn = QPushButton("Randomize")
        self.ua_layout = QHBoxLayout()
        self.ua_layout.addWidget(self.user_agent_combo)
        self.ua_layout.addWidget(self.randomize_ua_btn)
        self.populate_user_agents()
        self.randomize_ua_btn.clicked.connect(self.randomize_user_agent)

        self.screen_width_input = QSpinBox()
        self.screen_width_input.setRange(320, 3840)
        self.screen_width_input.setValue(profile.get("screen_width", 1920))
        self.screen_height_input = QSpinBox()
        self.screen_height_input.setRange(600, 2160)
        self.screen_height_input.setValue(profile.get("screen_height", 1080))
        self.timezone_input = QLineEdit(profile.get("timezone", ""))
        self.latitude_input = QLineEdit(str(profile.get("latitude", "")))
        self.longitude_input = QLineEdit(str(profile.get("longitude", "")))
        self.proxy_input = QLineEdit(profile.get("proxy", ""))
        self.fetch_geo_btn = QPushButton("Fetch from Proxy")
        self.proxy_layout = QHBoxLayout()
        self.proxy_layout.addWidget(self.proxy_input)
        self.proxy_layout.addWidget(self.fetch_geo_btn)

        self.webrtc_checkbox = QCheckBox("Disable WebRTC")
        self.webrtc_checkbox.setChecked(profile.get("disable_webrtc", True))

        self.form_layout.addRow(self.ua_label, self.ua_layout)
        self.form_layout.addRow("Screen Width:", self.screen_width_input)
        self.form_layout.addRow("Screen Height:", self.screen_height_input)
        self.form_layout.addRow("Timezone ID:", self.timezone_input)
        self.form_layout.addRow("Latitude:", self.latitude_input)
        self.form_layout.addRow("Longitude:", self.longitude_input)
        self.form_layout.addRow("Proxy:", self.proxy_layout)
        self.form_layout.addRow(self.webrtc_checkbox)

        self.layout.addLayout(self.form_layout)

        self.fetch_geo_btn.clicked.connect(self.fetch_geo_data)

        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.cancel_button)

        self.save_button.clicked.connect(self.save_config)
        self.cancel_button.clicked.connect(self.reject)

    def populate_user_agents(self):
        self.user_agent_combo.clear()
        profile_type = self.profile.get("profile_type", "Desktop").lower()

        ua_list = []
        if profile_type in USER_AGENTS:
            for platform in USER_AGENTS[profile_type]:
                ua_list.extend(USER_AGENTS[profile_type][platform])

        self.user_agent_combo.addItems(ua_list)

        current_ua = self.profile.get("user_agent")
        if current_ua and current_ua in ua_list:
            self.user_agent_combo.setCurrentText(current_ua)
        elif ua_list:
            self.user_agent_combo.setCurrentIndex(0)

    def randomize_user_agent(self):
        if self.user_agent_combo.count() > 0:
            index = random.randint(0, self.user_agent_combo.count() - 1)
            self.user_agent_combo.setCurrentIndex(index)

    def save_config(self):
        self.profile["user_agent"] = self.user_agent_combo.currentText()
        self.profile["screen_width"] = self.screen_width_input.value()
        self.profile["screen_height"] = self.screen_height_input.value()
        self.profile["timezone"] = self.timezone_input.text()
        self.profile["latitude"] = self.latitude_input.text()
        self.profile["longitude"] = self.longitude_input.text()
        self.profile["proxy"] = self.proxy_input.text()
        self.profile["disable_webrtc"] = self.webrtc_checkbox.isChecked()
        self.accept()

    def fetch_geo_data(self):
        proxy_str = self.proxy_input.text()
        if not proxy_str:
            QMessageBox.warning(self, "Warning", "Please enter a proxy string.")
            return

        try:
            geo_data = get_geo_from_proxy(proxy_str)
            if geo_data:
                self.timezone_input.setText(geo_data.get("timezone", ""))
                self.latitude_input.setText(str(geo_data.get("latitude", "")))
                self.longitude_input.setText(str(geo_data.get("longitude", "")))
                QMessageBox.information(self, "Success", "Geolocation data fetched and populated.")
            else:
                QMessageBox.warning(self, "Warning", "Could not fetch geolocation data.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def get_profile(self):
        return self.profile
