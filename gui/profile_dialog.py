from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QComboBox


class ProfileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Profile")
        self.layout = QVBoxLayout(self)

        self.label = QLabel("Enter profile name:")
        self.layout.addWidget(self.label)

        self.profile_name_input = QLineEdit()
        self.layout.addWidget(self.profile_name_input)

        self.type_label = QLabel("Select profile type:")
        self.layout.addWidget(self.type_label)

        self.profile_type_combo = QComboBox()
        self.profile_type_combo.addItems(["Desktop", "Mobile"])
        self.layout.addWidget(self.profile_type_combo)

        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")

        self.layout.addWidget(self.ok_button)
        self.layout.addWidget(self.cancel_button)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_profile_name(self):
        return self.profile_name_input.text()

    def get_profile_type(self):
        return self.profile_type_combo.currentText()
