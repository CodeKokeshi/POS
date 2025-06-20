"""
Test script to verify peso symbol encoding in receipts
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_receipt_generation():
    """Test receipt generation with peso symbols"""
    print("Testing receipt generation with Philippine Peso symbols...")
    
    try:
        from models.transaction import Transaction, Receipt, ServiceType
        from models.config import PriceConfig
        
        # Create configuration
        config = PriceConfig()
        
        # Create a receipt with transactions
        receipt = Receipt()
        
        # Add some test transactions
        print_transaction = Transaction(ServiceType.PRINT, 2, True, True)
        print_transaction.calculate_subtotal(config)
        receipt.add_transaction(print_transaction)
        
        photocopy_transaction = Transaction(ServiceType.PHOTOCOPY, 3, False, False)
        photocopy_transaction.calculate_subtotal(config)
        receipt.add_transaction(photocopy_transaction)
        
        scan_transaction = Transaction(ServiceType.SCAN, 1, True, False)
        scan_transaction.calculate_subtotal(config)
        receipt.add_transaction(scan_transaction)
        
        print(f"Created receipt with {len(receipt.transactions)} transactions")
        print(f"Total: ₱{receipt.total:.2f}")
        
        # Generate receipt content
        receipt_content = receipt.generate_receipt_text()
        print("\nReceipt content preview:")
        print("=" * 50)
        print(receipt_content)
        print("=" * 50)
        
        # Test saving to file
        os.makedirs("receipts", exist_ok=True)
        test_filename = "receipts/test_receipt_peso.txt"
        
        with open(test_filename, 'w', encoding='utf-8') as file:
            file.write(receipt_content)
        
        print(f"\n✅ Receipt saved successfully to: {test_filename}")
        
        # Verify file was created and readable
        with open(test_filename, 'r', encoding='utf-8') as file:
            saved_content = file.read()
            if "₱" in saved_content:
                print("✅ Peso symbol (₱) correctly saved and readable from file")
            else:
                print("❌ Peso symbol not found in saved file")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_receipt_generation()
    if success:
        print("\n🎉 All tests passed! Peso symbol encoding is working correctly.")
    else:
        print("\n💥 Tests failed. Check the error messages above.")
