"""Exception dialog for PyFishstrap"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QFrame, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QFont, QTextCursor
from typing import Optional, List, Dict, Any
import sys
import traceback

from ...paths import Paths
from ..frontend import frontend


class ExceptionDialog(QDialog):
    """Dialog for displaying exceptions with full details"""
    
    def __init__(self, exception: Exception, parent=None):
        super().__init__(parent)
        
        self._exception = exception
        
        self.setWindowTitle(f"{Paths.PROJECT_NAME} - Error")
        self.setMinimumSize(600, 400)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        
        # Initialize UI
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Error icon and title
        error_layout = QHBoxLayout()
        
        # Icon
        icon_label = QLabel()
        icon_label.setPixmap(QIcon.fromTheme(QIcon.ThemeIcon.DialogError).pixmap(32, 32))
        error_layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel("An Error Occurred")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        error_layout.addWidget(title_label)
        
        error_layout.addStretch()
        layout.addLayout(error_layout)
        
        # Error message
        message_group = QGroupBox("Error Message")
        message_layout = QVBoxLayout(message_group)
        
        self.message_label = QLabel(str(self._exception))
        self.message_label.setWordWrap(True)
        self.message_label.setStyleSheet("font-size: 14px;")
        message_layout.addWidget(self.message_label)
        
        layout.addWidget(message_group)
        
        # Error details
        details_group = QGroupBox("Error Details")
        details_layout = QVBoxLayout(details_group)
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.details_text.setStyleSheet("""
            QTextEdit {
                font-family: 'Courier New', monospace;
                font-size: 12px;
                background-color: #f0f0f0;
                border: 1px solid #ccc;
            }
        """)
        
        # Get traceback
        exc_type, exc_value, exc_traceback = sys.exc_info()
        if exc_type and exc_value and exc_traceback:
            tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            tb_text = ''.join(tb_lines)
        else:
            tb_lines = traceback.format_exception(type(self._exception), self._exception, self._exception.__traceback__)
            tb_text = ''.join(tb_lines)
        
        self.details_text.setPlainText(tb_text)
        
        # Scroll to top
        cursor = self.details_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        self.details_text.setTextCursor(cursor)
        
        details_layout.addWidget(self.details_text)
        layout.addWidget(details_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Copy button
        self.copy_btn = QPushButton("Copy Details")
        self.copy_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditCopy))
        self.copy_btn.clicked.connect(self._copy_details)
        button_layout.addWidget(self.copy_btn)
        
        # Close button
        self.close_btn = QPushButton("Close")
        self.close_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.DialogClose))
        self.close_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)
    
    def _copy_details(self):
        """Copy error details to clipboard"""
        from PyQt6.QtGui import QGuiApplication
        
        # Get error details
        exc_type, exc_value, exc_traceback = sys.exc_info()
        if exc_type and exc_value and exc_traceback:
            tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            tb_text = ''.join(tb_lines)
        else:
            tb_lines = traceback.format_exception(type(self._exception), self._exception, self._exception.__traceback__)
            tb_text = ''.join(tb_lines)
        
        # Copy to clipboard
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(f"Error: {self._exception}\n\n{tb_text}")
        
        # Show confirmation
        frontend.show_message_box(
            "Error details copied to clipboard!",
            QMessageBox.Icon.Information,
            "Copied"
        )
    
    def closeEvent(self, event):
        """Handle close event"""
        event.accept()


# Import QMessageBox for the fromTheme method
from PyQt6.QtWidgets import QMessageBox
