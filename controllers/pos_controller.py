"""
Main controller for the POS application
Handles business logic and coordinates between models and views
"""

import os
from datetime import datetime
from typing import List

from models.transaction import Transaction, Receipt, ServiceType
from models.config import PriceConfig


class POSController:
    """Main controller for POS operations"""
    
    def __init__(self):
        self.config = PriceConfig()
        self.current_receipt = Receipt()
        self.receipt_history = []
    
    def add_transaction(self, service_type: ServiceType, pages: int, 
                       is_colored: bool = False, has_images: bool = False) -> Transaction:
        """Add a new transaction to the current receipt"""
        transaction = Transaction(service_type, pages, is_colored, has_images)
        transaction.calculate_subtotal(self.config)
        self.current_receipt.add_transaction(transaction)
        return transaction
    
    def remove_transaction(self, index: int) -> bool:
        """Remove a transaction from the current receipt"""
        try:
            self.current_receipt.remove_transaction(index)
            return True
        except IndexError:
            return False
    
    def clear_current_receipt(self):
        """Clear all transactions from current receipt"""
        self.current_receipt = Receipt()
    
    def get_current_transactions(self) -> List[Transaction]:
        """Get all transactions in the current receipt"""
        return self.current_receipt.transactions
    
    def get_current_total(self) -> float:
        """Get the total amount for current receipt"""
        return self.current_receipt.calculate_total()
    
    def generate_receipt(self) -> str:
        """Generate and save the current receipt"""
        if not self.current_receipt.transactions:
            raise ValueError("No transactions to generate receipt for")
        
        # Ensure receipts directory exists
        os.makedirs("receipts", exist_ok=True)
        
        # Generate receipt content
        receipt_content = self.current_receipt.generate_receipt_text()
          # Save to file
        filename = os.path.join("receipts", self.current_receipt.get_receipt_filename())
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(receipt_content)
        
        # Add to history
        self.receipt_history.append(self.current_receipt)
        
        # Reset current receipt
        self.current_receipt = Receipt()
        
        return filename
    
    def update_pricing(self, service: str, monochrome_price: float, 
                      colored_price: float, image_surcharge: float):
        """Update pricing for a service"""
        self.config.set_monochrome_price(service, monochrome_price)
        self.config.set_colored_price(service, colored_price)
        self.config.set_image_surcharge(service, image_surcharge)
        self.config.save_config()
    
    def get_pricing_info(self, service: str) -> dict:
        """Get pricing information for a service"""
        return {
            'monochrome': self.config.get_monochrome_price(service),
            'colored': self.config.get_colored_price(service),
            'image_surcharge': self.config.get_image_surcharge(service)
        }
    
    def get_all_pricing(self) -> dict:
        """Get all pricing information"""
        return self.config.get_all_prices()
    
    def recalculate_current_transactions(self):
        """Recalculate all transactions in current receipt with updated prices"""
        for transaction in self.current_receipt.transactions:
            transaction.calculate_subtotal(self.config)
        self.current_receipt.calculate_total()
    
    def get_receipt_history(self) -> List[Receipt]:
        """Get history of generated receipts"""
        return self.receipt_history
    
    def get_transaction_preview(self, service_type: ServiceType, pages: int,
                              is_colored: bool = False, has_images: bool = False) -> dict:
        """Get a preview of transaction cost without adding to receipt"""
        temp_transaction = Transaction(service_type, pages, is_colored, has_images)
        subtotal = temp_transaction.calculate_subtotal(self.config)
        
        service_name = service_type.value.lower()
        base_price = (self.config.get_colored_price(service_name) 
                     if is_colored else self.config.get_monochrome_price(service_name))
        
        preview = {
            'pages': pages,
            'base_price': base_price,
            'base_total': base_price * pages,
            'is_colored': is_colored,
            'has_images': has_images,
            'image_surcharge': 0.0,
            'image_total': 0.0,
            'subtotal': subtotal
        }
        
        if has_images:
            preview['image_surcharge'] = self.config.get_image_surcharge(service_name)
            preview['image_total'] = preview['image_surcharge'] * pages
        
        return preview
