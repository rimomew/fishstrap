"""Installer dialog for PyFishstrap"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar,
    QPushButton, QFrame, QGroupBox, QLineEdit, QFileDialog,
    QComboBox, QCheckBox, QTextEdit
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QIcon, QFont
from typing import Optional, List, Dict, Any
from pathlib import Path

from ...enums import Theme
from ...paths import Paths
from ... import App
from ..frontend import frontend


class InstallerDialog(QDialog):
    """Installer dialog for PyFishstrap"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self._install_path: Optional[Path] = None
        self._is_installing = False
        self._progress = 0
        self._progress_max = 10000
        
        self.setWindowTitle(f"{Paths.PROJECT_NAME} - Installer")
        self.setMinimumSize(500, 400)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        
        # Initialize UI
        self._init_ui()
        
        # Connect signals
        self._connect_signals()
    
    def _init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Create stack widget for different pages
        self._create_welcome_page(layout)
    
    def _create_welcome_page(self, layout):
        """Create the welcome page"""
        # Title
        title_label = QLabel(f"{Paths.PROJECT_NAME} Installer")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(
            f"Welcome to the {Paths.PROJECT_NAME} installer!\n\n"
            f"This will install {Paths.PROJECT_NAME} on your system. "
            f"You can customize the installation options below."
        )
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Installation options group
        options_group = QGroupBox("Installation Options")
        options_layout = QVBoxLayout(options_group)
        
        # Install location
        location_layout = QHBoxLayout()
        
        self.location_edit = QLineEdit()
        self.location_edit.setPlaceholderText("Installation directory...")
        location_layout.addWidget(self.location_edit)
        
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self._browse_location)
        location_layout.addWidget(self.browse_btn)
        
        options_layout.addLayout(location_layout)
        
        # Create start menu shortcuts
        self.start_menu_check = QCheckBox("Create Start Menu shortcuts")
        self.start_menu_check.setChecked(True)
        options_layout.addWidget(self.start_menu_check)
        
        # Create desktop shortcut
        self.desktop_check = QCheckBox("Create Desktop shortcut")
        self.desktop_check.setChecked(True)
        options_layout.addWidget(self.desktop_check)
        
        layout.addWidget(options_group)
        
        # Progress group (hidden initially)
        self.progress_group = QGroupBox("Installation Progress")
        self.progress_group.setVisible(False)
        progress_layout = QVBoxLayout(self.progress_group)
        
        self.progress_label = QLabel("Initializing...")
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        progress_layout.addWidget(self.progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, self._progress_max)
        self.progress_bar.setValue(self._progress)
        self.progress_bar.setTextVisible(True)
        progress_layout.addWidget(self.progress_bar)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        progress_layout.addWidget(self.log_text)
        
        layout.addWidget(self.progress_group)
        
        # Buttons
        self._create_buttons(layout)
    
    def _create_buttons(self, layout):
        """Create the button layout"""
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Back button (hidden initially)
        self.back_btn = QPushButton("Back")
        self.back_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoPrevious))
        self.back_btn.setVisible(False)
        self.back_btn.clicked.connect(self._go_back)
        button_layout.addWidget(self.back_btn)
        
        # Next/Install button
        self.next_btn = QPushButton("Install")
        self.next_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoNext))
        self.next_btn.clicked.connect(self._install)
        button_layout.addWidget(self.next_btn)
        
        # Cancel button
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.DialogCancel))
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
    
    def _connect_signals(self):
        """Connect signals to slots"""
        pass
    
    def _browse_location(self):
        """Browse for installation location"""
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Select Installation Directory",
            str(Paths.get_local_app_data())
        )
        
        if dir_path:
            self.location_edit.setText(dir_path)
    
    def _install(self):
        """Start the installation process"""
        # Get installation path
        install_path = self.location_edit.text().strip()
        
        if not install_path:
            # Use default path
            install_path = str(Paths.get_local_app_data() / Paths.PROJECT_NAME)
            self.location_edit.setText(install_path)
        
        self._install_path = Path(install_path)
        
        # Check if path is valid
        try:
            self._install_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            frontend.show_message_box(
                f"Error creating installation directory: {e}",
                QMessageBox.Icon.Critical,
                "Installation Error"
            )
            return
        
        # Show progress
        self.progress_group.setVisible(True)
        self.back_btn.setVisible(True)
        self.next_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)
        
        # Start installation
        self._is_installing = True
        self._progress = 0
        self._log("Starting installation...")
        
        # Start timer for progress
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_progress)
        self._timer.start(50)
    
    def _update_progress(self):
        """Update installation progress"""
        if not self._is_installing:
            return
        
        # Increment progress
        self._progress += 200
        if self._progress > self._progress_max:
            self._progress = self._progress_max
        
        # Update UI
        self.progress_bar.setValue(self._progress)
        
        # Update status
        if self._progress < self._progress_max * 0.3:
            self._update_status("Creating directories...")
        elif self._progress < self._progress_max * 0.6:
            self._update_status("Copying files...")
        elif self._progress < self._progress_max * 0.8:
            self._update_status("Creating shortcuts...")
        else:
            self._update_status("Finalizing...")
        
        # Check if done
        if self._progress >= self._progress_max:
            self._timer.stop()
            self._complete_installation()
    
    def _update_status(self, status: str):
        """Update the status text"""
        self._status = status
        self.progress_label.setText(status)
    
    def _log(self, message: str):
        """Add a message to the log"""
        self.log_text.append(message)
    
    def _complete_installation(self):
        """Complete the installation process"""
        self._is_installing = False
        self._update_status("Installation complete!")
        self._log("Installation finished successfully!")
        
        # In real implementation, perform actual installation
        # For now, just show completion message
        
        # Enable buttons
        self.next_btn.setEnabled(True)
        self.cancel_btn.setEnabled(True)
        self.next_btn.setText("Finish")
        self.next_btn.disconnect()
        self.next_btn.clicked.connect(self.accept)
    
    def _go_back(self):
        """Go back to the previous page"""
        if self._is_installing:
            # Cancel installation
            self._is_installing = False
            if self._timer and self._timer.isActive():
                self._timer.stop()
        
        self.progress_group.setVisible(False)
        self.back_btn.setVisible(False)
        self.next_btn.setEnabled(True)
        self.cancel_btn.setEnabled(True)
        self.next_btn.setText("Install")
        self.next_btn.disconnect()
        self.next_btn.clicked.connect(self._install)
    
    def closeEvent(self, event):
        """Handle close event"""
        if self._is_installing:
            result = frontend.show_message_box(
                "Are you sure you want to cancel the installation?",
                QMessageBox.Icon.Question,
                "Cancel Installation",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if result == QMessageBox.StandardButton.Yes:
                self._is_installing = False
                if self._timer and self._timer.isActive():
                    self._timer.stop()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


# Import QMessageBox
from PyQt6.QtWidgets import QMessageBox
