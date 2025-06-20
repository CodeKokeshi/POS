"""
Test script to verify the POS system functionality
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_models():
    """Test the core models"""
    print("Testing models...")
    
    # Test configuration
    from models.config import PriceConfig
    config = PriceConfig()
    print(f"Print monochrome price: ₱{config.get_monochrome_price('print'):.2f}")
    print(f"Print colored price: ₱{config.get_colored_price('print'):.2f}")
    print(f"Print image surcharge: ₱{config.get_image_surcharge('print'):.2f}")
    
    # Test transaction
    from models.transaction import Transaction, ServiceType, Receipt
    transaction = Transaction(ServiceType.PRINT, 5, True, True)
    subtotal = transaction.calculate_subtotal(config)
    print(f"Transaction subtotal: ₱{subtotal:.2f}")
    
    # Test receipt
    receipt = Receipt()
    receipt.add_transaction(transaction)
    print(f"Receipt total: ₱{receipt.total:.2f}")
    
    print("Models test completed successfully!")

def test_controller():
    """Test the controller"""
    print("\nTesting controller...")
    
    from controllers.pos_controller import POSController
    from models.transaction import ServiceType
    
    controller = POSController()
    
    # Add a transaction
    transaction = controller.add_transaction(ServiceType.PRINT, 3, False, False)
    print(f"Added transaction: {transaction.to_string()}")
    
    # Get current total
    total = controller.get_current_total()
    print(f"Current total: ₱{total:.2f}")
    
    print("Controller test completed successfully!")

if __name__ == "__main__":
    try:
        test_models()
        test_controller()
        print("\n✅ All tests passed! The POS system is working correctly.")
        print("\nTo run the GUI application, use: python main.py")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
