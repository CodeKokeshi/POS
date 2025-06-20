"""
Main window for the POS application
Contains the primary interface for managing transactions
"""

import sys
import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QListWidget, QLabel, QMessageBox,
                             QApplication, QFrame, QListWidgetItem)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

from models.transaction import Receipt, Transaction, ServiceType
from models.config import PriceConfig
from views.service_dialog import ServiceDialog
from views.pricing_dialog import PricingDialog
from views.receipt_viewer import ReceiptViewerDialog


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.config = PriceConfig()
        self.current_receipt = Receipt()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Printing Business POS System")
        self.setGeometry(100, 100, 800, 600)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Title
        title_label = QLabel("Printing Business POS System")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        main_layout.addWidget(title_label)
        
        # Content layout (horizontal)
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)
        
        # Left panel - Service buttons
        left_panel = self.create_service_panel()
        content_layout.addWidget(left_panel, 1)
        
        # Right panel - Transaction list and total
        right_panel = self.create_transaction_panel()
        content_layout.addWidget(right_panel, 2)
        
        # Bottom panel - Action buttons
        bottom_panel = self.create_action_panel()
        main_layout.addWidget(bottom_panel)
        
        # Apply styles
        self.apply_styles()
        
    def create_service_panel(self):
        """Create the service selection panel"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.StyledPanel)
        layout = QVBoxLayout()
        
        # Service buttons
        services_label = QLabel("Services")
        services_label.setFont(QFont("Arial", 14, QFont.Bold))
        services_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(services_label)
        
        self.print_btn = QPushButton("Print Service")
        self.print_btn.clicked.connect(lambda: self.add_service(ServiceType.PRINT))
        layout.addWidget(self.print_btn)
        
        self.photocopy_btn = QPushButton("Photocopy Service")
        self.photocopy_btn.clicked.connect(lambda: self.add_service(ServiceType.PHOTOCOPY))
        layout.addWidget(self.photocopy_btn)
        
        self.scan_btn = QPushButton("Scan Service")
        self.scan_btn.clicked.connect(lambda: self.add_service(ServiceType.SCAN))
        layout.addWidget(self.scan_btn)
        
        layout.addStretch()
        
        # Configuration button
        self.config_btn = QPushButton("Configure Pricing")
        self.config_btn.clicked.connect(self.open_pricing_dialog)
        layout.addWidget(self.config_btn)
        
        panel.setLayout(layout)
        return panel
    
    def create_transaction_panel(self):
        """Create the transaction list panel"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.StyledPanel)
        layout = QVBoxLayout()
        
        # Transaction list
        transactions_label = QLabel("Current Transactions")
        transactions_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(transactions_label)
        
        self.transaction_list = QListWidget()
        self.transaction_list.setSelectionMode(QListWidget.SingleSelection)
        layout.addWidget(self.transaction_list)
        
        # Remove transaction button
        self.remove_btn = QPushButton("Remove Selected")
        self.remove_btn.clicked.connect(self.remove_transaction)
        self.remove_btn.setEnabled(False)
        layout.addWidget(self.remove_btn)
        
        # Total display
        self.total_label = QLabel("Total: ₱0.00")
        self.total_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.total_label.setAlignment(Qt.AlignCenter)
        self.total_label.setStyleSheet("color: #2E8B57; background-color: #F0F8FF; padding: 10px; border: 2px solid #2E8B57; border-radius: 5px;")
        layout.addWidget(self.total_label)
        
        # Connect selection change
        self.transaction_list.itemSelectionChanged.connect(self.on_selection_changed)
        
        panel.setLayout(layout)
        return panel
    
    def create_action_panel(self):
        """Create the action buttons panel"""
        panel = QFrame()
        layout = QHBoxLayout()
        
        # Clear all button
        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.clicked.connect(self.clear_all_transactions)
        layout.addWidget(self.clear_btn)
        
        # Receipt Viewer button
        self.receipt_viewer_btn = QPushButton("Receipt Viewer")
        self.receipt_viewer_btn.clicked.connect(self.open_receipt_viewer)
        self.receipt_viewer_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
                color: #666666;
            }
        """)
        layout.addWidget(self.receipt_viewer_btn)
        
        layout.addStretch()
        
        # Generate receipt button
        self.receipt_btn = QPushButton("Generate Receipt")
        self.receipt_btn.clicked.connect(self.generate_receipt)
        self.receipt_btn.setEnabled(False)
        layout.addWidget(self.receipt_btn)
        
        panel.setLayout(layout)
        return panel
    
    def apply_styles(self):
        """Apply custom styles to the interface"""
        # Service buttons
        service_style = """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 15px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """
        
        self.print_btn.setStyleSheet(service_style)
        self.photocopy_btn.setStyleSheet(service_style)
        self.scan_btn.setStyleSheet(service_style)
        
        # Config button
        self.config_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px;
                font-size: 12px;
                border-radius: 5px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        
        # Action buttons
        action_style = """
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
                color: #666666;
            }
        """
        
        self.clear_btn.setStyleSheet(action_style)
        self.receipt_btn.setStyleSheet(action_style.replace("#FF9800", "#4CAF50").replace("#F57C00", "#45a049"))
        self.remove_btn.setStyleSheet(action_style.replace("#FF9800", "#f44336").replace("#F57C00", "#d32f2f"))
    
    def add_service(self, service_type: ServiceType):
        """Open dialog to add a new service"""
        dialog = ServiceDialog(service_type, self.config, self)
        if dialog.exec_() == ServiceDialog.Accepted:
            transaction = dialog.get_transaction()
            self.current_receipt.add_transaction(transaction)
            self.update_transaction_list()
            self.update_total()
    
    def remove_transaction(self):
        """Remove selected transaction"""
        current_row = self.transaction_list.currentRow()
        if current_row >= 0:
            self.current_receipt.remove_transaction(current_row)
            self.update_transaction_list()
            self.update_total()
    
    def clear_all_transactions(self):
        """Clear all transactions"""
        if self.current_receipt.transactions:
            reply = QMessageBox.question(self, 'Clear All', 
                                       'Are you sure you want to clear all transactions?',
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.current_receipt = Receipt()
                self.update_transaction_list()
                self.update_total()
    
    def update_transaction_list(self):
        """Update the transaction list display"""
        self.transaction_list.clear()
        for transaction in self.current_receipt.transactions:
            item = QListWidgetItem(transaction.to_string())
            self.transaction_list.addItem(item)
        
        # Enable/disable buttons based on transaction count
        has_transactions = len(self.current_receipt.transactions) > 0
        self.receipt_btn.setEnabled(has_transactions)
        self.clear_btn.setEnabled(has_transactions)
    
    def update_total(self):
        """Update the total display"""
        total = self.current_receipt.calculate_total()
        self.total_label.setText(f"Total: ₱{total:.2f}")
    
    def on_selection_changed(self):
        """Handle transaction list selection change"""
        has_selection = self.transaction_list.currentItem() is not None
        self.remove_btn.setEnabled(has_selection)
    
    def open_pricing_dialog(self):
        """Open the pricing configuration dialog"""
        dialog = PricingDialog(self.config, self)
        if dialog.exec_() == PricingDialog.Accepted:
            # Recalculate all transaction totals with new prices
            for transaction in self.current_receipt.transactions:
                transaction.calculate_subtotal(self.config)
            self.update_transaction_list()
            self.update_total()
    
    def open_receipt_viewer(self):
        dialog = ReceiptViewerDialog(parent=self)
        dialog.exec_()
    
    def generate_receipt(self):
        """Generate and save receipt"""
        if not self.current_receipt.transactions:
            QMessageBox.warning(self, "No Transactions", "Please add at least one transaction before generating a receipt.")
            return
        
        try:
            # Ensure receipts directory exists
            os.makedirs("receipts", exist_ok=True)
            
            # Generate receipt content
            receipt_content = self.current_receipt.generate_receipt_text()
              # Save to file
            filename = os.path.join("receipts", self.current_receipt.get_receipt_filename())
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(receipt_content)
            
            # Show success message
            QMessageBox.information(self, "Receipt Generated", 
                                  f"Receipt saved successfully as:\n{filename}\n\nTotal: ₱{self.current_receipt.total:.2f}")
            
            # Reset for next transaction
            self.current_receipt = Receipt()
            self.update_transaction_list()
            self.update_total()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate receipt:\n{str(e)}")


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Printing Business POS")
    app.setOrganizationName("Printing Business")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
