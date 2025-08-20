from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel,
    QFormLayout, QSpinBox, QCheckBox
)


class ConfigWindow(QDialog):
    def __init__(self, profile, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Configure Profile: {profile['name']}")
        self.profile = profile

        self.layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()

        self.user_agent_input = QLineEdit(profile.get("user_agent", ""))
        self.screen_width_input = QSpinBox()
        self.screen_width_input.setRange(800, 3840)
        self.screen_width_input.setValue(profile.get("screen_width", 1920))
        self.screen_height_input = QSpinBox()
        self.screen_height_input.setRange(600, 2160)
        self.screen_height_input.setValue(profile.get("screen_height", 1080))
        self.timezone_input = QLineEdit(profile.get("timezone", ""))
        self.latitude_input = QLineEdit(str(profile.get("latitude", "")))
        self.longitude_input = QLineEdit(str(profile.get("longitude", "")))
        self.proxy_input = QLineEdit(profile.get("proxy", ""))
        self.webrtc_checkbox = QCheckBox("Disable WebRTC")
        self.webrtc_checkbox.setChecked(profile.get("disable_webrtc", True))

        self.form_layout.addRow("User-Agent:", self.user_agent_input)
        self.form_layout.addRow("Screen Width:", self.screen_width_input)
        self.form_layout.addRow("Screen Height:", self.screen_height_input)
        self.form_layout.addRow("Timezone ID:", self.timezone_input)
        self.form_layout.addRow("Latitude:", self.latitude_input)
        self.form_layout.addRow("Longitude:", self.longitude_input)
        self.form_layout.addRow("Proxy:", self.proxy_input)
        self.form_layout.addRow(self.webrtc_checkbox)

        self.layout.addLayout(self.form_layout)

        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.cancel_button)

        self.save_button.clicked.connect(self.save_config)
        self.cancel_button.clicked.connect(self.reject)

    def save_config(self):
        self.profile["user_agent"] = self.user_agent_input.text()
        self.profile["screen_width"] = self.screen_width_input.value()
        self.profile["screen_height"] = self.screen_height_input.value()
        self.profile["timezone"] = self.timezone_input.text()
        self.profile["latitude"] = self.latitude_input.text()
        self.profile["longitude"] = self.longitude_input.text()
        self.profile["proxy"] = self.proxy_input.text()
        self.profile["disable_webrtc"] = self.webrtc_checkbox.isChecked()
        self.accept()

    def get_profile(self):
        return self.profile
