"""UI module for PyFishstrap"""

from PyQt6.QtWidgets import QApplication, QMessageBox, QDialog, QMainWindow
from PyQt6.QtCore import Qt, QObject, pyqtSignal
from PyQt6.QtGui import QIcon, QFont, QPalette, QColor

from .frontend import Frontend
from .main_window import MainWindow
from .dialogs import (
    BootstrapperDialog,
    ClassicFluentDialog,
    FluentDialog,
    TerminalDialog,
    ByfronDialog,
    TwentyFiveDialog,
    LegacyDialog2008,
    LegacyDialog2011,
    VistaDialog,
    CustomDialog,
    MessageBox,
    ExceptionDialog,
    SettingsDialog,
    FastFlagsEditorDialog,
    LanguageSelectorDialog,
    InstallerDialog,
)

# Global QApplication instance
_qapp = None


def get_qapplication() -> QApplication:
    """Get or create the global QApplication instance"""
    global _qapp
    if _qapp is None:
        _qapp = QApplication([])
    return _qapp


def run_application():
    """Run the PyQt application"""
    app = get_qapplication()
    
    # Set application metadata
    from ..paths import Paths
    app.setApplicationName(Paths.PROJECT_NAME)
    app.setOrganizationName(Paths.PROJECT_OWNER)
    
    # Set style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Execute application
    sys.exit(app.exec())


# Import sys for exit
import sys
