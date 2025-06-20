"""
Transaction model for the POS system
Handles individual service transactions
"""

from enum import Enum
from datetime import datetime
from typing import List


class ServiceType(Enum):
    PRINT = "Print"
    PHOTOCOPY = "Photocopy"
    SCAN = "Scan"


class Transaction:
    """Represents a single service transaction"""
    
    def __init__(self, service_type: ServiceType, pages: int, is_colored: bool = False, has_images: bool = False):
        self.service_type = service_type
        self.pages = pages
        self.is_colored = is_colored
        self.has_images = has_images
        self.timestamp = datetime.now()
        self.subtotal = 0.0
    
    def calculate_subtotal(self, config):
        """Calculate subtotal based on current pricing configuration"""
        service_name = self.service_type.value.lower()
        
        # Base price per page
        if self.is_colored:
            base_price = config.get_colored_price(service_name)
        else:
            base_price = config.get_monochrome_price(service_name)
        
        # Calculate base cost
        self.subtotal = base_price * self.pages
        
        # Add image surcharge if applicable
        if self.has_images:
            image_surcharge = config.get_image_surcharge(service_name)
            self.subtotal += image_surcharge * self.pages
        
        return self.subtotal
    
    def to_string(self):
        """Convert transaction to string format for display"""
        color_str = "Colored" if self.is_colored else "Monochrome"
        images_str = " (with images)" if self.has_images else ""
        return f"{self.service_type.value} - {self.pages} pages - {color_str}{images_str}: ₱{self.subtotal:.2f}"


class Receipt:
    """Represents a complete receipt with multiple transactions"""
    
    def __init__(self):
        self.transactions: List[Transaction] = []
        self.timestamp = datetime.now()
        self.total = 0.0
    
    def add_transaction(self, transaction: Transaction):
        """Add a transaction to the receipt"""
        self.transactions.append(transaction)
        self.calculate_total()
    
    def remove_transaction(self, index: int):
        """Remove a transaction by index"""
        if 0 <= index < len(self.transactions):
            self.transactions.pop(index)
            self.calculate_total()
    
    def calculate_total(self):
        """Calculate total amount for all transactions"""
        self.total = sum(transaction.subtotal for transaction in self.transactions)
        return self.total
    
    def get_receipt_filename(self):
        """Generate filename for receipt export"""
        timestamp_str = self.timestamp.strftime("%m-%d-%Y_%H-%M-%S")
        return f"Receipt_{timestamp_str}.txt"
    
    def generate_receipt_text(self):
        """Generate formatted receipt text"""
        receipt_text = []
        receipt_text.append("=" * 50)
        receipt_text.append("           PRINTING BUSINESS POS")
        receipt_text.append("=" * 50)
        receipt_text.append("")
        receipt_text.append(f"Date: {self.timestamp.strftime('%m/%d/%Y')}")
        receipt_text.append(f"Time: {self.timestamp.strftime('%I:%M:%S %p')}")
        receipt_text.append("")
        receipt_text.append("-" * 50)
        receipt_text.append("TRANSACTION DETAILS:")
        receipt_text.append("-" * 50)
        
        for i, transaction in enumerate(self.transactions, 1):
            receipt_text.append(f"{i}. {transaction.to_string()}")
        
        receipt_text.append("")
        receipt_text.append("-" * 50)
        receipt_text.append(f"TOTAL: ₱{self.total:.2f}")
        receipt_text.append("-" * 50)
        receipt_text.append("")
        receipt_text.append("Thank you for your business!")
        receipt_text.append("=" * 50)
        
        return "\n".join(receipt_text)
