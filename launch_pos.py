"""
Simple launcher for the POS application with error handling
"""

import sys
import os
import traceback

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def launch_pos():
    """Launch the POS application"""
    try:
        print("Launching Printing Business POS System...")
        print("Loading modules...")
        
        # Import PyQt5 first
        from PyQt5.QtWidgets import QApplication
        print("✅ PyQt5 imported successfully")
        
        # Import our modules
        from views.main_window import MainWindow
        print("✅ Main window module imported")
        
        # Create application
        app = QApplication(sys.argv)
        app.setApplicationName("Printing Business POS")
        app.setOrganizationName("Printing Business")
        print("✅ Application created")
        
        # Create and show main window
        window = MainWindow()
        print("✅ Main window created")
        
        window.show()
        print("✅ Window displayed")
        print("🚀 Application started successfully!")
        
        # Run the application
        return app.exec_()
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install PyQt5")
        return 1
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(launch_pos())
