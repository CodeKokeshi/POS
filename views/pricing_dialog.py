"""
Pricing configuration dialog
Allows users to customize pricing for different services
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QDoubleSpinBox, QPushButton, QFormLayout,
                             QFrame, QTabWidget, QWidget, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class PricingDialog(QDialog):
    """Dialog for configuring service pricing"""
    
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.init_ui()
        self.load_current_prices()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Configure Pricing")
        self.setModal(True)
        self.setFixedSize(500, 400)
        
        # Main layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Title
        title_label = QLabel("Pricing Configuration")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title_label)
        
        # Tab widget for different services
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Create tabs for each service
        self.print_tab = self.create_service_tab("Print")
        self.photocopy_tab = self.create_service_tab("Photocopy")
        self.scan_tab = self.create_service_tab("Scan")
        
        self.tab_widget.addTab(self.print_tab, "Print Services")
        self.tab_widget.addTab(self.photocopy_tab, "Photocopy Services")
        self.tab_widget.addTab(self.scan_tab, "Scan Services")
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.reset_btn = QPushButton("Reset to Defaults")
        self.reset_btn.clicked.connect(self.reset_to_defaults)
        button_layout.addWidget(self.reset_btn)
        
        button_layout.addStretch()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        self.save_btn = QPushButton("Save Changes")
        self.save_btn.clicked.connect(self.save_changes)
        self.save_btn.setDefault(True)
        button_layout.addWidget(self.save_btn)
        
        layout.addLayout(button_layout)
        
        # Apply styles
        self.apply_styles()
    
    def create_service_tab(self, service_name):
        """Create a tab for service pricing configuration"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Service description
        desc_label = QLabel(f"Configure pricing for {service_name.lower()} services")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setFont(QFont("Arial", 12))
        layout.addWidget(desc_label)
        
        # Pricing form
        form_frame = QFrame()
        form_frame.setFrameStyle(QFrame.StyledPanel)
        form_layout = QFormLayout()
        
        # Monochrome price
        mono_spinbox = QDoubleSpinBox()
        mono_spinbox.setRange(0.01, 10.00)
        mono_spinbox.setSingleStep(0.01)
        mono_spinbox.setDecimals(2)
        mono_spinbox.setPrefix("₱")
        form_layout.addRow("Monochrome (per page):", mono_spinbox)
        
        # Colored price
        color_spinbox = QDoubleSpinBox()
        color_spinbox.setRange(0.01, 10.00)
        color_spinbox.setSingleStep(0.01)
        color_spinbox.setDecimals(2)
        color_spinbox.setPrefix("₱")
        form_layout.addRow("Colored (per page):", color_spinbox)
        
        # Image surcharge
        image_spinbox = QDoubleSpinBox()
        image_spinbox.setRange(0.00, 5.00)
        image_spinbox.setSingleStep(0.01)
        image_spinbox.setDecimals(2)
        image_spinbox.setPrefix("₱")
        form_layout.addRow("Image surcharge (per page):", image_spinbox)
        
        form_frame.setLayout(form_layout)
        layout.addWidget(form_frame)
        
        layout.addStretch()
        
        tab.setLayout(layout)
        
        # Store references to spinboxes
        setattr(self, f"{service_name.lower()}_mono_spinbox", mono_spinbox)
        setattr(self, f"{service_name.lower()}_color_spinbox", color_spinbox)
        setattr(self, f"{service_name.lower()}_image_spinbox", image_spinbox)
        
        return tab
    
    def apply_styles(self):
        """Apply custom styles"""
        # Save button
        self.save_btn.setStyleSheet("""
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
        
        # Reset button
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
    
    def load_current_prices(self):
        """Load current pricing configuration into the form"""
        services = ['print', 'photocopy', 'scan']
        
        for service in services:
            mono_spinbox = getattr(self, f"{service}_mono_spinbox")
            color_spinbox = getattr(self, f"{service}_color_spinbox")
            image_spinbox = getattr(self, f"{service}_image_spinbox")
            
            mono_spinbox.setValue(self.config.get_monochrome_price(service))
            color_spinbox.setValue(self.config.get_colored_price(service))
            image_spinbox.setValue(self.config.get_image_surcharge(service))
    
    def reset_to_defaults(self):
        """Reset all prices to default values"""
        reply = QMessageBox.question(self, 'Reset to Defaults', 
                                   'Are you sure you want to reset all prices to default values?',
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Default values
            defaults = {
                'print': {'mono': 0.10, 'color': 0.25, 'image': 0.05},
                'photocopy': {'mono': 0.08, 'color': 0.20, 'image': 0.03},
                'scan': {'mono': 0.15, 'color': 0.30, 'image': 0.10}
            }
            
            for service, prices in defaults.items():
                mono_spinbox = getattr(self, f"{service}_mono_spinbox")
                color_spinbox = getattr(self, f"{service}_color_spinbox")
                image_spinbox = getattr(self, f"{service}_image_spinbox")
                
                mono_spinbox.setValue(prices['mono'])
                color_spinbox.setValue(prices['color'])
                image_spinbox.setValue(prices['image'])
    
    def save_changes(self):
        """Save the pricing changes"""
        try:
            services = ['print', 'photocopy', 'scan']
            
            for service in services:
                mono_spinbox = getattr(self, f"{service}_mono_spinbox")
                color_spinbox = getattr(self, f"{service}_color_spinbox")
                image_spinbox = getattr(self, f"{service}_image_spinbox")
                
                self.config.set_monochrome_price(service, mono_spinbox.value())
                self.config.set_colored_price(service, color_spinbox.value())
                self.config.set_image_surcharge(service, image_spinbox.value())
            
            # Save to file
            self.config.save_config()
            
            QMessageBox.information(self, "Success", "Pricing configuration saved successfully!")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save pricing configuration:\n{str(e)}")
    
    def get_pricing_summary(self):
        """Get a summary of current pricing for display"""
        services = ['print', 'photocopy', 'scan']
        summary = []
        
        for service in services:
            mono_price = self.config.get_monochrome_price(service)
            color_price = self.config.get_colored_price(service)
            image_price = self.config.get_image_surcharge(service)
            
            summary.append(f"{service.title()}: Mono ₱{mono_price:.2f}, Color ₱{color_price:.2f}, Images +₱{image_price:.2f}")
        
        return "\n".join(summary)
