"""Custom message box for PyFishstrap"""

from PyQt6.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap
from typing import Optional, List, Dict, Any

from ...enums import Theme
from ...paths import Paths
from ..frontend import frontend


class MessageBox:
    """Custom message box with theming support"""
    
    @staticmethod
    def show(
        parent=None,
        title: str = "PyFishstrap",
        message: str = "",
        icon: QMessageBox.Icon = QMessageBox.Icon.Information,
        buttons: QMessageBox.StandardButton = QMessageBox.StandardButton.Ok,
        default_button: QMessageBox.StandardButton = QMessageBox.StandardButton.Ok
    ) -> QMessageBox.StandardButton:
        """Show a custom message box"""
        msg_box = QMessageBox(parent)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(buttons)
        msg_box.setDefaultButton(default_button)
        msg_box.setIcon(icon)
        
        # Apply theme
        if frontend.theme == Theme.DARK:
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
                    padding: 6px 12px;
                    border-radius: 4px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #4a4a4a;
                }
            """)
        elif frontend.theme == Theme.LIGHT:
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #f0f0f0;
                    color: #303030;
                }
                QMessageBox QLabel {
                    color: #303030;
                }
                QMessageBox QPushButton {
                    background-color: #e0e0e0;
                    color: #303030;
                    border: 1px solid #aaa;
                    padding: 6px 12px;
                    border-radius: 4px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #d0d0d0;
                }
            """)
        
        return msg_box.exec()
    
    @staticmethod
    def show_info(
        parent=None,
        title: str = "Information",
        message: str = "",
        buttons: QMessageBox.StandardButton = QMessageBox.StandardButton.Ok,
        default_button: QMessageBox.StandardButton = QMessageBox.StandardButton.Ok
    ) -> QMessageBox.StandardButton:
        """Show an information message box"""
        return MessageBox.show(parent, title, message, QMessageBox.Icon.Information, buttons, default_button)
    
    @staticmethod
    def show_warning(
        parent=None,
        title: str = "Warning",
        message: str = "",
        buttons: QMessageBox.StandardButton = QMessageBox.StandardButton.Ok,
        default_button: QMessageBox.StandardButton = QMessageBox.StandardButton.Ok
    ) -> QMessageBox.StandardButton:
        """Show a warning message box"""
        return MessageBox.show(parent, title, message, QMessageBox.Icon.Warning, buttons, default_button)
    
    @staticmethod
    def show_error(
        parent=None,
        title: str = "Error",
        message: str = "",
        buttons: QMessageBox.StandardButton = QMessageBox.StandardButton.Ok,
        default_button: QMessageBox.StandardButton = QMessageBox.StandardButton.Ok
    ) -> QMessageBox.StandardButton:
        """Show an error message box"""
        return MessageBox.show(parent, title, message, QMessageBox.Icon.Critical, buttons, default_button)
    
    @staticmethod
    def show_question(
        parent=None,
        title: str = "Question",
        message: str = "",
        buttons: QMessageBox.StandardButton = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        default_button: QMessageBox.StandardButton = QMessageBox.StandardButton.Yes
    ) -> QMessageBox.StandardButton:
        """Show a question message box"""
        return MessageBox.show(parent, title, message, QMessageBox.Icon.Question, buttons, default_button)
