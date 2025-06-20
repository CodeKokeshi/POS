"""
Utility functions for the POS system
"""

import os
from datetime import datetime
from typing import List, Dict


def ensure_directory_exists(directory: str):
    """Ensure a directory exists, create if it doesn't"""
    if not os.path.exists(directory):
        os.makedirs(directory)


def format_currency(amount: float) -> str:
    """Format a float as currency string"""
    return f"₱{amount:.2f}"


def get_receipt_files() -> List[str]:
    """Get list of all receipt files"""
    receipts_dir = "receipts"
    if not os.path.exists(receipts_dir):
        return []
    
    files = []
    for filename in os.listdir(receipts_dir):
        if filename.startswith("Receipt_") and filename.endswith(".txt"):
            files.append(os.path.join(receipts_dir, filename))
    
    return sorted(files, reverse=True)  # Most recent first


def validate_pricing(price: float) -> bool:
    """Validate that a price is reasonable"""
    return 0.01 <= price <= 100.00


def get_service_display_name(service_type) -> str:
    """Get display name for service type"""
    from models.transaction import ServiceType
    
    if service_type == ServiceType.PRINT:
        return "Print Service"
    elif service_type == ServiceType.PHOTOCOPY:
        return "Photocopy Service"
    elif service_type == ServiceType.SCAN:
        return "Scan Service"
    else:
        return "Unknown Service"


def export_daily_summary(date: datetime = None) -> str:
    """Export a daily summary of transactions"""
    if date is None:
        date = datetime.now()
    
    date_str = date.strftime("%Y-%m-%d")
    summary_filename = f"daily_summary_{date_str}.txt"
    
    # This is a placeholder - in a real system you'd have a database
    # of transactions to summarize
    summary_content = f"""
DAILY SUMMARY - {date.strftime("%B %d, %Y")}
{'=' * 50}

Total Transactions: 0
Total Revenue: ₱0.00

Service Breakdown:
- Print Services: 0 transactions, ₱0.00
- Photocopy Services: 0 transactions, ₱0.00
- Scan Services: 0 transactions, ₱0.00

Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
    
    with open(summary_filename, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    return summary_filename


def backup_config():
    """Create a backup of the current configuration"""
    if os.path.exists("config.ini"):
        backup_filename = f"config_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ini"
        with open("config.ini", 'r', encoding='utf-8') as original:
            with open(backup_filename, 'w', encoding='utf-8') as backup:
                backup.write(original.read())
        
        return backup_filename
    return None
