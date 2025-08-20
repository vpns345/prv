from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QTextEdit, QPushButton, QLabel
)

class BulkProxyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Bulk Assign Proxies")
        self.layout = QVBoxLayout(self)

        self.label = QLabel("Paste proxies below (one per line, e.g., host:port:user:pass):")
        self.layout.addWidget(self.label)

        self.proxy_input = QTextEdit()
        self.layout.addWidget(self.proxy_input)

        self.ok_button = QPushButton("Assign")
        self.cancel_button = QPushButton("Cancel")

        self.layout.addWidget(self.ok_button)
        self.layout.addWidget(self.cancel_button)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_proxies(self):
        proxies = self.proxy_input.toPlainText().strip().split('\n')
        return [p.strip() for p in proxies if p.strip()]
