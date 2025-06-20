"""
Configuration management for the POS system
Handles pricing configuration using INI files
"""

import configparser
import os
from typing import Dict


class PriceConfig:
    """Manages pricing configuration for different services"""
    
    def __init__(self, config_file: str = "config.ini"):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_default_config()
        self.load_config()
    
    def load_default_config(self):
        """Load default pricing configuration (Philippine Pesos)"""
        self.config['PRINT'] = {
            'monochrome_price': '5.00',
            'colored_price': '8.00',
            'image_surcharge': '2.00'
        }
        
        self.config['PHOTOCOPY'] = {
            'monochrome_price': '3.00',
            'colored_price': '5.00',
            'image_surcharge': '2.00'
        }
        
        self.config['SCAN'] = {
            'monochrome_price': '2.00',
            'colored_price': '4.00',
            'image_surcharge': '2.00'
        }
    
    def load_config(self):
        """Load configuration from file if it exists"""
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
    
    def save_config(self):
        """Save current configuration to file"""
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
    
    def get_monochrome_price(self, service: str) -> float:
        """Get monochrome price for a service"""
        section = service.upper()
        return self.config.getfloat(section, 'monochrome_price', fallback=0.10)
    
    def get_colored_price(self, service: str) -> float:
        """Get colored price for a service"""
        section = service.upper()
        return self.config.getfloat(section, 'colored_price', fallback=0.25)
    
    def get_image_surcharge(self, service: str) -> float:
        """Get image surcharge for a service"""
        section = service.upper()
        return self.config.getfloat(section, 'image_surcharge', fallback=0.05)
    
    def set_monochrome_price(self, service: str, price: float):
        """Set monochrome price for a service"""
        section = service.upper()
        if section not in self.config:
            self.config[section] = {}
        self.config[section]['monochrome_price'] = str(price)
    
    def set_colored_price(self, service: str, price: float):
        """Set colored price for a service"""
        section = service.upper()
        if section not in self.config:
            self.config[section] = {}
        self.config[section]['colored_price'] = str(price)
    
    def set_image_surcharge(self, service: str, price: float):
        """Set image surcharge for a service"""
        section = service.upper()
        if section not in self.config:
            self.config[section] = {}
        self.config[section]['image_surcharge'] = str(price)
    
    def get_all_prices(self) -> Dict[str, Dict[str, float]]:
        """Get all pricing information as a dictionary"""
        prices = {}
        for service in ['print', 'photocopy', 'scan']:
            prices[service] = {
                'monochrome': self.get_monochrome_price(service),
                'colored': self.get_colored_price(service),
                'image_surcharge': self.get_image_surcharge(service)
            }
        return prices
