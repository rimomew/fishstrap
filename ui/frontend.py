"""Frontend utilities for PyFishstrap UI"""

from PyQt6.QtWidgets import QMessageBox, QDialog, QApplication
from PyQt6.QtCore import Qt, QObject, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap
from typing import Optional, List, Dict, Any, Callable
import sys
import traceback

from ..enums import Theme, BootstrapperStyle
from ..paths import Paths
from .. import App


class Frontend(QObject):
    """Frontend controller for UI operations"""
    
    # Signals
    show_message_signal = pyqtSignal(str, str, int)  # title, message, icon
    show_exception_signal = pyqtSignal(Exception)
    show_bootstrapper_signal = pyqtSignal(object)  # launch_mode
    show_settings_signal = pyqtSignal()
    show_menu_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self._current_dialog = None
        self._theme = Theme.SYSTEM
        self._style = BootstrapperStyle.CLASSIC
    
    @property
    def current_dialog(self):
        """Get the current dialog"""
        return self._current_dialog
    
    @current_dialog.setter
    def current_dialog(self, value):
        """Set the current dialog"""
        self._current_dialog = value
    
    @property
    def theme(self) -> Theme:
        """Get the current theme"""
        return self._theme
    
    @theme.setter
    def theme(self, value: Theme):
        """Set the current theme"""
        self._theme = value
        self._apply_theme()
    
    @property
    def style(self) -> BootstrapperStyle:
        """Get the current bootstrapper style"""
        return self._style
    
    @style.setter
    def style(self, value: BootstrapperStyle):
        """Set the current bootstrapper style"""
        self._style = value
    
    def _apply_theme(self):
        """Apply the current theme to the application"""
        app = QApplication.instance()
        if app is None:
            return
        
        palette = app.palette()
        
        if self._theme == Theme.DARK:
            # Dark theme
            palette.setColor(QPalette.ColorRole.Window, QColor(45, 45, 45))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 220, 220))
            palette.setColor(QPalette.ColorRole.Base, QColor(60, 60, 60))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(25, 25, 25))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(220, 220, 220))
            palette.setColor(QPalette.ColorRole.Text, QColor(220, 220, 220))
            palette.setColor(QPalette.ColorRole.Button, QColor(60, 60, 60))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(220, 220, 220))
            palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
        elif self._theme == Theme.LIGHT:
            # Light theme
            palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(30, 30, 30))
            palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(230, 230, 230))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(30, 30, 30))
            palette.setColor(QPalette.ColorRole.Text, QColor(30, 30, 30))
            palette.setColor(QPalette.ColorRole.Button, QColor(230, 230, 230))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(30, 30, 30))
            palette.setColor(QPalette.ColorRole.BrightText, QColor(0, 0, 0))
            palette.setColor(QPalette.ColorRole.Link, QColor(0, 120, 215))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        
        app.setPalette(palette)
    
    def initialize(self):
        """Initialize the frontend"""
        # Set default theme from settings
        if App.settings.loaded:
            theme_str = App.settings.prop.theme
            if theme_str == "Dark":
                self._theme = Theme.DARK
            elif theme_str == "Light":
                self._theme = Theme.LIGHT
        
        # Set default style from settings
        if App.settings.loaded:
            style_str = App.settings.prop.bootstrapperStyle
            style_map = {
                "Classic": BootstrapperStyle.CLASSIC,
                "Fluent": BootstrapperStyle.FLUENT,
                "Terminal": BootstrapperStyle.TERMINAL,
                "Byfron": BootstrapperStyle.BYFRON,
                "TwentyFive": BootstrapperStyle.TWENTY_FIVE,
                "Legacy2008": BootstrapperStyle.LEGACY_2008,
                "Legacy2011": BootstrapperStyle.LEGACY_2011,
                "Vista": BootstrapperStyle.VISTA,
                "Custom": BootstrapperStyle.CUSTOM,
            }
            if style_str in style_map:
                self._style = style_map[style_str]
        
        self._apply_theme()
    
    def show_message_box(self, message: str, icon: int = QMessageBox.Icon.Information, 
                        title: str = "PyFishstrap", buttons: int = QMessageBox.StandardButton.Ok,
                        default_button: int = QMessageBox.StandardButton.Ok) -> int:
        """Show a message box and return the result"""
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(buttons)
        msg_box.setDefaultButton(default_button)
        msg_box.setIcon(icon)
        
        # Apply theme
        if self._theme == Theme.DARK:
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #2d2d2d;
                    color: #dcdcdc;
                }
                QMessageBox QLabel {
                    color: #dcdcdc;
                }
                QMessageBox QPushButton {
                    background-color: #3c3c3c;
                    color: #dcdcdc;
                    border: 1px solid #555;
                }
                QMessageBox QPushButton:hover {
                    background-color: #4a4a4a;
                }
            """)
        
        return msg_box.exec()
    
    def show_exception_dialog(self, exception: Exception):
        """Show an exception dialog with full details"""
        from .dialogs.exception_dialog import ExceptionDialog
        
        dialog = ExceptionDialog(exception)
        dialog.exec()
    
    def show_bootstrapper(self, launch_mode):
        """Show the bootstrapper dialog for the given launch mode"""
        from .dialogs.bootstrapper_dialog import BootstrapperDialog
        
        # Create dialog based on style
        dialog = BootstrapperDialog(launch_mode)
        dialog.exec()
    
    def show_settings(self):
        """Show the settings dialog"""
        from .dialogs.settings_dialog import SettingsDialog
        
        dialog = SettingsDialog()
        dialog.exec()
    
    def show_menu(self):
        """Show the main menu"""
        from .main_window import MainWindow
        
        # Check if main window already exists
        for widget in QApplication.instance().topLevelWidgets():
            if isinstance(widget, MainWindow):
                widget.show()
                widget.raise_()
                widget.activateWindow()
                return
        
        # Create new main window
        window = MainWindow()
        window.show()
    
    def show_language_selector(self):
        """Show the language selector dialog"""
        from .dialogs.language_selector import LanguageSelectorDialog
        
        dialog = LanguageSelectorDialog()
        return dialog.exec()
    
    def show_installer(self):
        """Show the installer dialog"""
        from .dialogs.installer_dialog import InstallerDialog
        
        dialog = InstallerDialog()
        return dialog.exec()


# Global frontend instance
frontend = Frontend()
