"""Language selector dialog for PyFishstrap"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QFrame, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QFont
from typing import Optional, List, Dict, Any

from ...paths import Paths
from ... import App
from ..frontend import frontend


class LanguageSelectorDialog(QDialog):
    """Dialog for selecting the application language"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle(f"{Paths.PROJECT_NAME} - Select Language")
        self.setMinimumSize(400, 200)
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        
        # Initialize UI
        self._init_ui()
        
        # Load current language
        self._load_language()
    
    def _init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title_label = QLabel("Select Language")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(
            "Please select your preferred language for the application."
        )
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Language selection
        language_group = QGroupBox("Available Languages")
        language_layout = QVBoxLayout(language_group)
        
        self.language_combo = QComboBox()
        self.language_combo.setIconSize(QSize(24, 24))
        
        # Add languages
        languages = [
            ("English (US)", "en-us", "🇺🇸"),
            ("English (UK)", "en-gb", "🇬🇧"),
            ("Spanish", "es", "🇪🇸"),
            ("French", "fr", "🇫🇷"),
            ("German", "de", "🇩🇪"),
            ("Italian", "it", "🇮🇹"),
            ("Portuguese", "pt", "🇵🇹"),
            ("Russian", "ru", "🇷🇺"),
            ("Chinese", "zh", "🇨🇳"),
            ("Japanese", "ja", "🇯🇵"),
            ("Korean", "ko", "🇰🇷"),
        ]
        
        for display_name, locale_code, flag_emoji in languages:
            self.language_combo.addItem(f"{flag_emoji} {display_name}", locale_code)
        
        language_layout.addWidget(self.language_combo)
        layout.addWidget(language_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # OK button
        self.ok_btn = QPushButton("OK")
        self.ok_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.DialogOk))
        self.ok_btn.clicked.connect(self._save_and_close)
        button_layout.addWidget(self.ok_btn)
        
        # Cancel button
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.DialogCancel))
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
    
    def _load_language(self):
        """Load the current language"""
        current_locale = App.settings.prop.locale
        
        # Find the index of the current locale
        for i in range(self.language_combo.count()):
            if self.language_combo.itemData(i) == current_locale:
                self.language_combo.setCurrentIndex(i)
                break
    
    def _save_and_close(self):
        """Save the selected language and close"""
        # Get selected locale
        locale = self.language_combo.currentData()
        
        # Update settings
        App.settings.prop.locale = locale
        App.settings.save()
        
        # Apply language (this would typically require a restart)
        # For now, just close the dialog
        self.accept()
    
    def closeEvent(self, event):
        """Handle close event"""
        event.accept()


# Fix import
from PyQt6.QtCore import QSize
