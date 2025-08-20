from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QSpinBox, QFormLayout
)

class BulkCreateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Bulk Create Profiles")
        self.layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()

        self.prefix_input = QLineEdit("Profile-")
        self.count_input = QSpinBox()
        self.count_input.setRange(1, 1000)
        self.count_input.setValue(10)

        self.form_layout.addRow("Profile Name Prefix:", self.prefix_input)
        self.form_layout.addRow("Number of Profiles:", self.count_input)

        self.layout.addLayout(self.form_layout)

        self.ok_button = QPushButton("Create")
        self.cancel_button = QPushButton("Cancel")

        self.layout.addWidget(self.ok_button)
        self.layout.addWidget(self.cancel_button)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_values(self):
        return {
            "prefix": self.prefix_input.text(),
            "count": self.count_input.value()
        }
