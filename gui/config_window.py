import json
import random
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel,
    QFormLayout, QSpinBox, QCheckBox, QHBoxLayout, QMessageBox, QComboBox
)
from utils import get_geo_from_proxy, test_proxy
from engine.profile_manager import generate_fingerprint


class ConfigWindow(QDialog):
    def __init__(self, profile, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Configure Profile: {profile['name']}")
        self.profile = profile

        with open("fingerprint_data.json", "r") as f:
            self.fingerprints_data = json.load(f)

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
        self.user_agent_combo.currentTextChanged.connect(self.on_user_agent_changed)

        self.screen_width_input = QSpinBox()
        self.screen_width_input.setRange(320, 3840)
        self.screen_width_input.setValue(self.profile.get("screen_width", 1920))
        self.screen_height_input = QSpinBox()
        self.screen_height_input.setRange(600, 2160)
        self.screen_height_input.setValue(self.profile.get("screen_height", 1080))

        self.timezone_input = QLineEdit(self.profile.get("timezone", ""))
        self.latitude_input = QLineEdit(str(self.profile.get("latitude", "")))
        self.longitude_input = QLineEdit(str(self.profile.get("longitude", "")))

        self.proxy_protocol_combo = QComboBox()
        self.proxy_protocol_combo.addItems(["HTTP", "SOCKS5"])
        self.proxy_protocol_combo.setCurrentText(self.profile.get("proxy_protocol", "HTTP"))

        self.proxy_input = QLineEdit(self.profile.get("proxy", ""))
        self.fetch_geo_btn = QPushButton("Fetch from Proxy")
        self.test_proxy_btn = QPushButton("Test Proxy")

        self.proxy_layout = QHBoxLayout()
        self.proxy_layout.addWidget(self.proxy_protocol_combo)
        self.proxy_layout.addWidget(self.proxy_input)
        self.proxy_layout.addWidget(self.fetch_geo_btn)
        self.proxy_layout.addWidget(self.test_proxy_btn)

        self.webrtc_checkbox = QCheckBox("Disable WebRTC")
        self.webrtc_checkbox.setChecked(self.profile.get("disable_webrtc", True))

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
        self.test_proxy_btn.clicked.connect(self.test_proxy_connection)

        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        self.refresh_fingerprint_btn = QPushButton("Refresh Fingerprint")

        self.button_box = QHBoxLayout()
        self.button_box.addWidget(self.refresh_fingerprint_btn)
        self.button_box.addStretch()
        self.button_box.addWidget(self.save_button)
        self.button_box.addWidget(self.cancel_button)
        self.layout.addLayout(self.button_box)

        self.refresh_fingerprint_btn.clicked.connect(self.refresh_fingerprint)
        self.save_button.clicked.connect(self.save_config)
        self.cancel_button.clicked.connect(self.reject)

    def populate_user_agents(self):
        self.user_agent_combo.clear()
        profile_type = self.profile.get("profile_type", "Desktop")

        self.compatible_fingerprints = [fp for fp in self.fingerprints_data if fp["profile_type"] == profile_type]
        ua_list = [fp["user_agent"] for fp in self.compatible_fingerprints]

        self.user_agent_combo.addItems(ua_list)

        current_ua = self.profile.get("user_agent")
        if current_ua in ua_list:
            self.user_agent_combo.setCurrentText(current_ua)
        elif ua_list:
            self.user_agent_combo.setCurrentIndex(0)

    def on_user_agent_changed(self, user_agent):
        # Find the corresponding fingerprint and update screen resolution
        for fp in self.compatible_fingerprints:
            if fp["user_agent"] == user_agent:
                self.screen_width_input.setValue(fp["screen_width"])
                self.screen_height_input.setValue(fp["screen_height"])
                break

    def randomize_user_agent(self):
        if self.user_agent_combo.count() > 0:
            index = random.randint(0, self.user_agent_combo.count() - 1)
            self.user_agent_combo.setCurrentIndex(index)

    def save_config(self):
        # Find the full fingerprint details for the selected User-Agent
        selected_ua = self.user_agent_combo.currentText()
        selected_fp = next((fp for fp in self.compatible_fingerprints if fp["user_agent"] == selected_ua), None)

        if selected_fp:
            self.profile["fingerprint"].update(selected_fp)
            self.profile.update(selected_fp)

        self.profile["screen_width"] = self.screen_width_input.value()
        self.profile["screen_height"] = self.screen_height_input.value()
        self.profile["timezone"] = self.timezone_input.text()
        self.profile["latitude"] = self.latitude_input.text()
        self.profile["longitude"] = self.longitude_input.text()
        self.profile["proxy"] = self.proxy_input.text()
        self.profile["proxy_protocol"] = self.proxy_protocol_combo.currentText()
        self.profile["disable_webrtc"] = self.webrtc_checkbox.isChecked()
        self.accept()

    def fetch_geo_data(self):
        proxy_str = self.proxy_input.text()
        protocol = self.proxy_protocol_combo.currentText()
        if not proxy_str:
            QMessageBox.warning(self, "Warning", "Please enter a proxy string.")
            return
        try:
            geo_data = get_geo_from_proxy(proxy_str, protocol)
            if geo_data:
                self.timezone_input.setText(geo_data.get("timezone", ""))
                self.latitude_input.setText(str(geo_data.get("latitude", "")))
                self.longitude_input.setText(str(geo_data.get("longitude", "")))
                QMessageBox.information(self, "Success", "Geolocation data fetched and populated.")
            else:
                QMessageBox.warning(self, "Warning", "Could not fetch geolocation data.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def test_proxy_connection(self):
        proxy_str = self.proxy_input.text()
        protocol = self.proxy_protocol_combo.currentText()
        if not proxy_str:
            QMessageBox.warning(self, "Warning", "Please enter a proxy string.")
            return
        success, message = test_proxy(proxy_str, protocol)
        if success:
            QMessageBox.information(self, "Proxy Test Success", message)
        else:
            QMessageBox.critical(self, "Proxy Test Failed", message)

    def refresh_fingerprint(self):
        new_fingerprint = generate_fingerprint(self.profile.get("profile_type", "Desktop"))
        self.profile["fingerprint"] = new_fingerprint
        self.profile.update(new_fingerprint)

        # Update UI fields
        self.populate_user_agents() # This will re-populate and select the new UA
        self.screen_width_input.setValue(self.profile["screen_width"])
        self.screen_height_input.setValue(self.profile["screen_height"])
        QMessageBox.information(self, "Success", "Fingerprint has been refreshed.")

    def get_profile(self):
        return self.profile
