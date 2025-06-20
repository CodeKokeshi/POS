"""
Service dialog for entering transaction details
Allows users to input service parameters like pages, color options, etc.
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QSpinBox, QCheckBox, QPushButton, QFormLayout,
                             QFrame, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from models.transaction import Transaction, ServiceType


class ServiceDialog(QDialog):
    """Dialog for entering service transaction details"""
    
    def __init__(self, service_type: ServiceType, config, parent=None):
        super().__init__(parent)
        self.service_type = service_type
        self.config = config
        self.transaction = None
        self.init_ui()
        self.update_preview()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle(f"Add {self.service_type.value} Service")
        self.setModal(True)
        self.setFixedSize(450, 400)
        
        # Main layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Title
        title_label = QLabel(f"{self.service_type.value} Service")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title_label)
        
        # Service details form
        form_frame = QFrame()
        form_frame.setFrameStyle(QFrame.StyledPanel)
        form_layout = QFormLayout()
        
        # Page count
        self.pages_spinbox = QSpinBox()
        self.pages_spinbox.setMinimum(1)
        self.pages_spinbox.setMaximum(1000)
        self.pages_spinbox.setValue(1)
        self.pages_spinbox.valueChanged.connect(self.update_preview)
        form_layout.addRow("Number of Pages:", self.pages_spinbox)
        
        # Color option
        self.colored_checkbox = QCheckBox("Colored Output")
        self.colored_checkbox.stateChanged.connect(self.update_preview)
        form_layout.addRow("", self.colored_checkbox)
        
        # Images option
        self.images_checkbox = QCheckBox("Contains Images")
        self.images_checkbox.stateChanged.connect(self.update_preview)
        form_layout.addRow("", self.images_checkbox)
        
        form_frame.setLayout(form_layout)
        layout.addWidget(form_frame)
        
        # Price preview
        self.preview_frame = QFrame()
        self.preview_frame.setFrameStyle(QFrame.StyledPanel)
        preview_layout = QVBoxLayout()
        
        preview_title = QLabel("Price Preview")
        preview_title.setFont(QFont("Arial", 12, QFont.Bold))
        preview_title.setAlignment(Qt.AlignCenter)
        preview_layout.addWidget(preview_title)
        
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setFont(QFont("Arial", 10))
        self.preview_label.setStyleSheet("color: #2E8B57; padding: 10px;")
        self.preview_label.setWordWrap(True)
        preview_layout.addWidget(self.preview_label)
        
        self.preview_frame.setLayout(preview_layout)
        layout.addWidget(self.preview_frame)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        self.add_btn = QPushButton("Add Transaction")
        self.add_btn.clicked.connect(self.accept_transaction)
        self.add_btn.setDefault(True)
        button_layout.addWidget(self.add_btn)
        
        layout.addLayout(button_layout)
        
        # Apply styles
        self.apply_styles()
    
    def apply_styles(self):
        """Apply custom styles"""
        # Add button
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        # Cancel button
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        
        # Checkboxes
        checkbox_style = """
            QCheckBox {
                font-size: 12px;
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #cccccc;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #4CAF50;
                border-radius: 3px;
                background-color: #4CAF50;
            }
        """
        
        self.colored_checkbox.setStyleSheet(checkbox_style)
        self.images_checkbox.setStyleSheet(checkbox_style)
    
    def update_preview(self):
        """Update the price preview"""
        pages = self.pages_spinbox.value()
        is_colored = self.colored_checkbox.isChecked()
        has_images = self.images_checkbox.isChecked()
        
        # Create temporary transaction to calculate price
        temp_transaction = Transaction(self.service_type, pages, is_colored, has_images)
        subtotal = temp_transaction.calculate_subtotal(self.config)
          # Build preview text
        service_name = self.service_type.value.lower()
        base_price = self.config.get_colored_price(service_name) if is_colored else self.config.get_monochrome_price(service_name)
        
        preview_lines = []
        color_type = "Colored" if is_colored else "Mono"
        preview_lines.append(f"{pages} pages × ₱{base_price:.2f} ({color_type})")
        preview_lines.append(f"= ₱{base_price * pages:.2f}")
        
        if has_images:
            image_surcharge = self.config.get_image_surcharge(service_name)
            image_total = image_surcharge * pages
            preview_lines.append(f"Images: {pages} × ₱{image_surcharge:.2f} = ₱{image_total:.2f}")
        
        preview_lines.append("─" * 25)
        preview_lines.append(f"Total: ₱{subtotal:.2f}")
        
        self.preview_label.setText("\n".join(preview_lines))
    
    def accept_transaction(self):
        """Accept the transaction and close dialog"""
        pages = self.pages_spinbox.value()
        is_colored = self.colored_checkbox.isChecked()
        has_images = self.images_checkbox.isChecked()
        
        if pages <= 0:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number of pages.")
            return
        
        # Create transaction
        self.transaction = Transaction(self.service_type, pages, is_colored, has_images)
        self.transaction.calculate_subtotal(self.config)
        
        self.accept()
    
    def get_transaction(self):
        """Get the created transaction"""
        return self.transaction
