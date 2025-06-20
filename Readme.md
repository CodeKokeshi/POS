# Printing Business POS System

A point-of-sale application for managing a printing business with features for printing, photocopying, and scanning services.

## Overview

This JavaFX-based application allows printing business operators to:
- Process different types of document services (Print, Photocopy, Scan)
- Configure pricing based on service type, color options, and image inclusion
- Generate and save transaction receipts
- Customize pricing for different services

## Features

### Service Management
- **Print Services**: Process print jobs with page count, color options, and image settings
- **Photocopy Services**: Track photocopy jobs with customizable pricing
- **Scan Services**: Manage document scanning with various options

### Pricing Configuration
- Customizable pricing for each service type
- Separate rates for monochrome and colored outputs
- Additional surcharge for images
- Persistent configuration using properties file

### Receipt Generation
- Detailed transaction summary
- Automatic price calculation based on current price configuration
- Receipt export as text file with date and time
- Support for multiple services in a single transaction

## Technical Details

- Built with **Java** and **JavaFX** for the user interface
- Uses **Maven** for dependency management
- MVC architecture with controller classes for each screen
- Properties-based configuration system for pricing

## Getting Started

1. Launch the application
2. Select a service type (Print, Photocopy, or Scan)
3. Enter transaction details (pages, color options, etc.)
4. Add more transactions if needed
5. Generate and save the receipt

## Configuration

Pricing can be customized through the application interface:
- Navigate to the landing page
- Click "Customize Pricing"
- Update prices for different service types
- Save changes (requires application restart)

## File Structure

- The application generates receipt files in the root directory
- Receipt names follow the format: `Receipt MM-DD-YYYY Time HH-MM-SS AM/PM.txt`
- Configuration is stored in `config.properties`