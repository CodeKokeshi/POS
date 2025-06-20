"""
Receipt Viewer Dialog
Allows users to browse and view generated receipts
"""

import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QTextEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class ReceiptViewerDialog(QDialog):
    def __init__(self, receipts_dir="receipts", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Receipt Viewer")
        self.setMinimumSize(600, 500)
        self.receipts_dir = receipts_dir
        self.init_ui()
        self.load_receipts()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel("View Generated Receipts")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        h_layout = QHBoxLayout()
        self.receipt_list = QListWidget()
        self.receipt_list.setMinimumWidth(220)
        self.receipt_list.setFont(QFont("Arial", 11))
        self.receipt_list.setStyleSheet("background-color: #F0F8FF; border: 2px solid #2E8B57; border-radius: 5px; padding: 5px;")
        self.receipt_list.currentItemChanged.connect(self.display_receipt)
        h_layout.addWidget(self.receipt_list)

        self.text_view = QTextEdit()
        self.text_view.setReadOnly(True)
        self.text_view.setFont(QFont("Consolas", 11))
        self.text_view.setStyleSheet("background-color: #FFFFFF; border: 2px solid #2E8B57; border-radius: 5px; padding: 10px;")
        h_layout.addWidget(self.text_view)

        layout.addLayout(h_layout)

        close_btn = QPushButton("Close")
        close_btn.setFont(QFont("Arial", 12, QFont.Bold))
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
                margin: 10px 0 0 0;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        layout.setAlignment(close_btn, Qt.AlignRight)

    def load_receipts(self):
        self.receipt_list.clear()
        if not os.path.exists(self.receipts_dir):
            return
        files = [f for f in os.listdir(self.receipts_dir) if f.startswith("Receipt_") and f.endswith(".txt")]
        files.sort(reverse=True)
        for f in files:
            self.receipt_list.addItem(f)
        if files:
            self.receipt_list.setCurrentRow(0)

    def display_receipt(self, current, previous):
        if not current:
            self.text_view.clear()
            return
        filename = os.path.join(self.receipts_dir, current.text())
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
            self.text_view.setPlainText(content)
        except Exception as e:
            self.text_view.setPlainText(f"Failed to load receipt:\n{e}")
