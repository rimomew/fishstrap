"""Bootstrapper dialog for PyFishstrap"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar,
    QPushButton, QFrame, QGroupBox, QTextEdit, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QThread, QObject
from PyQt6.QtGui import QIcon, QPixmap, QFont
from typing import Optional, List, Dict, Any
import sys

from ...enums import LaunchMode, BootstrapperStyle, Theme
from ...paths import Paths
from ... import App
from ..frontend import frontend


class BootstrapperDialog(QDialog):
    """Base bootstrapper dialog"""
    
    def __init__(self, launch_mode: LaunchMode, parent=None):
        super().__init__(parent)
        
        self._launch_mode = launch_mode
        self._progress = 0
        self._progress_max = 10000
        self._status = "Initializing..."
        self._cancel_requested = False
        
        self.setWindowTitle(f"{Paths.PROJECT_NAME} - Bootstrapper")
        self.setMinimumSize(400, 300)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        
        # Initialize UI based on style
        self._init_ui()
        
        # Apply theme
        self._apply_theme()
        
        # Start bootstrapping
        self._start_bootstrapping()
    
    def _init_ui(self):
        """Initialize the UI based on the current style"""
        style = frontend.style
        
        if style == BootstrapperStyle.CLASSIC:
            self._init_classic_ui()
        elif style == BootstrapperStyle.FLUENT:
            self._init_fluent_ui()
        elif style == BootstrapperStyle.TERMINAL:
            self._init_terminal_ui()
        elif style == BootstrapperStyle.BYFRON:
            self._init_byfron_ui()
        elif style == BootstrapperStyle.TWENTY_FIVE:
            self._init_twenty_five_ui()
        elif style == BootstrapperStyle.LEGACY_2008:
            self._init_legacy_2008_ui()
        elif style == BootstrapperStyle.LEGACY_2011:
            self._init_legacy_2011_ui()
        elif style == BootstrapperStyle.VISTA:
            self._init_vista_ui()
        elif style == BootstrapperStyle.CUSTOM:
            self._init_custom_ui()
        else:
            # Default to classic
            self._init_classic_ui()
    
    def _init_classic_ui(self):
        """Initialize classic UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header_label = QLabel("Bootstrapper")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(header_label)
        
        # Status
        self.status_label = QLabel(self._status)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, self._progress_max)
        self.progress_bar.setValue(self._progress)
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)
        
        # Log
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        layout.addWidget(self.log_text)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self._cancel)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
    
    def _init_fluent_ui(self):
        """Initialize fluent UI"""
        self._init_classic_ui()
        
        # Apply fluent styling
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QProgressBar {
                border: 1px solid #444;
                border-radius: 4px;
                text-align: center;
                background-color: #333;
            }
            QProgressBar::chunk {
                background-color: #0078d7;
                border-radius: 3px;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #444;
            }
            QPushButton {
                background-color: #0078d7;
                color: #ffffff;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0091f7;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """)
    
    def _init_terminal_ui(self):
        """Initialize terminal UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # Terminal-like display
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            background-color: #000000;
            color: #00ff00;
            font-family: 'Courier New', monospace;
            font-size: 12px;
        """)
        layout.addWidget(self.log_text)
        
        # Status bar
        status_layout = QHBoxLayout()
        
        self.status_label = QLabel(self._status)
        self.status_label.setStyleSheet("color: #ffffff;")
        status_layout.addWidget(self.status_label)
        
        status_layout.addStretch()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self._cancel)
        status_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(status_layout)
        
        # Set window style
        self.setStyleSheet("""
            QDialog {
                background-color: #111111;
            }
            QPushButton {
                background-color: #333333;
                color: #ffffff;
                border: 1px solid #555;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """)
    
    def _init_byfron_ui(self):
        """Initialize Byfron-style UI"""
        self._init_classic_ui()
        
        # Apply Byfron styling
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
                color: #e0e0e0;
            }
            QLabel {
                color: #e0e0e0;
                font-size: 14px;
            }
            QProgressBar {
                border: 1px solid #333;
                border-radius: 5px;
                text-align: center;
                background-color: #2a2a2a;
            }
            QProgressBar::chunk {
                background-color: #ff6b35;
                border-radius: 4px;
            }
            QTextEdit {
                background-color: #252525;
                color: #e0e0e0;
                border: 1px solid #333;
                font-family: 'Segoe UI', sans-serif;
            }
            QPushButton {
                background-color: #ff6b35;
                color: #ffffff;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff8c55;
            }
        """)
    
    def _init_twenty_five_ui(self):
        """Initialize 2025-style UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Logo
        logo_frame = QFrame()
        logo_layout = QHBoxLayout(logo_frame)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        
        # Placeholder for logo
        logo_label = QLabel("25")
        logo_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ff6b35;")
        logo_layout.addWidget(logo_label)
        
        logo_layout.addStretch()
        
        # Title
        title_label = QLabel("Bootstrapper")
        title_label.setStyleSheet("font-size: 16px; color: #ffffff;")
        logo_layout.addWidget(title_label)
        
        layout.addWidget(logo_frame)
        
        # Status
        self.status_label = QLabel(self._status)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 14px; color: #e0e0e0;")
        layout.addWidget(self.status_label)
        
        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, self._progress_max)
        self.progress_bar.setValue(self._progress)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #333;
                border-radius: 4px;
                text-align: center;
                background-color: #2a2a2a;
                color: #ffffff;
            }
            QProgressBar::chunk {
                background-color: #ff6b35;
                border-radius: 3px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Log
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(100)
        self.log_text.setStyleSheet("""
            background-color: #1a1a1a;
            color: #e0e0e0;
            border: 1px solid #333;
            font-family: 'Segoe UI', sans-serif;
            font-size: 12px;
        """)
        layout.addWidget(self.log_text)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self._cancel)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: #ffffff;
                border: 1px solid #555;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        
        # Window styling
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
            }
        """)
    
    def _init_legacy_2008_ui(self):
        """Initialize legacy 2008 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # Header with old Roblox logo style
        header_frame = QFrame()
        header_frame.setFrameShape(QFrame.Shape.Panel)
        header_frame.setFrameShadow(QFrame.Shadow.Raised)
        header_layout = QHBoxLayout(header_frame)
        
        title_label = QLabel("Roblox Bootstrapper")
        title_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #ffffff;
            background-color: #0078d7;
            padding: 5px 10px;
        """)
        header_layout.addWidget(title_label)
        
        layout.addWidget(header_frame)
        
        # Status
        self.status_label = QLabel(self._status)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, self._progress_max)
        self.progress_bar.setValue(self._progress)
        layout.addWidget(self.progress_bar)
        
        # Log
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(100)
        layout.addWidget(self.log_text)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self._cancel)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        
        # Window styling
        self.setStyleSheet("""
            QDialog {
                background-color: #c0c0c0;
            }
            QLabel {
                color: #000000;
            }
            QProgressBar {
                border: 2px solid #808080;
                border-radius: 0px;
                text-align: center;
                background-color: #ffffff;
            }
            QProgressBar::chunk {
                background-color: #0078d7;
            }
            QTextEdit {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #808080;
            }
            QPushButton {
                background-color: #c0c0c0;
                color: #000000;
                border: 2px solid #808080;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #0078d7;
                color: #ffffff;
            }
        """)
    
    def _init_legacy_2011_ui(self):
        """Initialize legacy 2011 UI"""
        self._init_legacy_2008_ui()
        
        # Adjust styling for 2011
        self.setStyleSheet("""
            QDialog {
                background-color: #e0e0e0;
            }
            QLabel {
                color: #000000;
                font-size: 13px;
            }
            QProgressBar {
                border: 1px solid #a0a0a0;
                border-radius: 3px;
                text-align: center;
                background-color: #ffffff;
            }
            QProgressBar::chunk {
                background-color: #4a90d9;
                border-radius: 2px;
            }
            QTextEdit {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #a0a0a0;
                font-size: 12px;
            }
            QPushButton {
                background-color: #e0e0e0;
                color: #000000;
                border: 1px solid #a0a0a0;
                padding: 6px 12px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #4a90d9;
                color: #ffffff;
            }
        """)
    
    def _init_vista_ui(self):
        """Initialize Vista-style UI"""
        self._init_classic_ui()
        
        # Apply Vista styling
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #000000;
                font-size: 13px;
            }
            QProgressBar {
                border: 1px solid #808080;
                border-radius: 4px;
                text-align: center;
                background-color: #ffffff;
            }
            QProgressBar::chunk {
                background-color: #0078d7;
                border-radius: 3px;
            }
            QTextEdit {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #808080;
            }
            QPushButton {
                background-color: #f0f0f0;
                color: #000000;
                border: 1px solid #808080;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0078d7;
                color: #ffffff;
            }
        """)
    
    def _init_custom_ui(self):
        """Initialize custom UI"""
        # For custom UI, use the classic layout but allow customization
        self._init_classic_ui()
    
    def _apply_theme(self):
        """Apply the current theme"""
        if frontend.theme == Theme.DARK:
            # Dark theme adjustments
            pass
        elif frontend.theme == Theme.LIGHT:
            # Light theme adjustments
            pass
    
    def _start_bootstrapping(self):
        """Start the bootstrapping process"""
        # Update status
        self._update_status("Starting bootstrapper...")
        self._log("Bootstrapper initialized")
        
        # Use actual bootstrapping from the backend
        from ...bootstrapper import Bootstrapper
        from PyQt6.QtCore import QThread
        import asyncio
        
        # Create and start bootstrapper in a separate thread
        self._bootstrapper_thread = QThread()
        self._bootstrapper_worker = BootstrapperWorker(self._launch_mode)
        self._bootstrapper_worker.moveToThread(self._bootstrapper_thread)
        
        # Connect signals
        self._bootstrapper_worker.progress_updated.connect(self._update_progress_value)
        self._bootstrapper_worker.status_updated.connect(self._update_status)
        self._bootstrapper_worker.log_message.connect(self._log)
        self._bootstrapper_worker.finished.connect(self._bootstrapping_finished)
        self._bootstrapper_worker.error_occurred.connect(self._bootstrapping_error)
        
        # Start the thread
        self._bootstrapper_thread.started.connect(self._bootstrapper_worker.run)
        self._bootstrapper_thread.start()
    
    def _update_progress_value(self, value: int, max_value: int = 10000):
        """Update progress bar value"""
        self._progress = value
        self._progress_max = max_value
        if hasattr(self, 'progress_bar'):
            self.progress_bar.setRange(0, max_value)
            self.progress_bar.setValue(value)
    
    def _bootstrapping_finished(self):
        """Handle bootstrapping completion"""
        self._update_status("Launching...")
        self._log("Bootstrapping complete!")
        
        # Clean up thread
        if self._bootstrapper_thread and self._bootstrapper_thread.isRunning():
            self._bootstrapper_thread.quit()
            self._bootstrapper_thread.wait()
        
        self.accept()
    
    def _bootstrapping_error(self, error: str):
        """Handle bootstrapping error"""
        self._update_status(f"Error: {error}")
        self._log(f"Error: {error}")
        
        # Clean up thread
        if self._bootstrapper_thread and self._bootstrapper_thread.isRunning():
            self._bootstrapper_thread.quit()
            self._bootstrapper_thread.wait()
        
        # Show error message
        frontend.show_message_box(error, QMessageBox.Icon.Critical)
        self.reject()


class BootstrapperWorker(QObject):
    """Worker class to run bootstrapping in a separate thread"""
    
    progress_updated = pyqtSignal(int, int)
    status_updated = pyqtSignal(str)
    log_message = pyqtSignal(str)
    finished = pyqtSignal()
    error_occurred = pyqtSignal(str)
    
    def __init__(self, launch_mode: LaunchMode):
        super().__init__()
        self._launch_mode = launch_mode
        self._cancel_requested = False
    
    def run(self):
        """Run the bootstrapping process"""
        import asyncio
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            self.log_message.emit("Starting bootstrapping...")
            self.status_updated.emit("Initializing...")
            
            # Create bootstrapper
            from ...bootstrapper import Bootstrapper
            bootstrapper = Bootstrapper(self._launch_mode)
            
            # For now, simulate the process with actual progress
            # In a real implementation, we would connect to the bootstrapper's signals
            self._simulate_bootstrapping(bootstrapper)
            
            self.finished.emit()
        except Exception as e:
            self.error_occurred.emit(str(e))
    
    def _simulate_bootstrapping(self, bootstrapper):
        """Simulate bootstrapping with actual progress updates"""
        import time
        
        total_steps = 10
        for i in range(total_steps):
            if self._cancel_requested:
                return
            
            progress = int((i + 1) / total_steps * 10000)
            self.progress_updated.emit(progress, 10000)
            
            # Update status
            if i < 3:
                self.status_updated.emit("Checking for updates...")
            elif i < 6:
                self.status_updated.emit("Applying settings...")
            else:
                self.status_updated.emit("Launching Roblox...")
            
            # Log message
            self.log_message.emit(f"Step {i + 1}/{total_steps} completed")
            
            time.sleep(0.5)  # Simulate work
    
    def cancel(self):
        """Cancel the bootstrapping process"""
        self._cancel_requested = True
        
        # Cancel the worker if it exists
        if hasattr(self, '_bootstrapper_worker'):
            self._bootstrapper_worker.cancel()
        
        self._update_status("Cancelled")
        self._log("Bootstrapping cancelled by user")
        
        # Clean up thread
        if hasattr(self, '_bootstrapper_thread') and self._bootstrapper_thread.isRunning():
            self._bootstrapper_thread.quit()
            self._bootstrapper_thread.wait()
        
        self.reject()
    
    def _update_status(self, status: str):
        """Update the status text"""
        self._status = status
        if hasattr(self, 'status_label'):
            self.status_label.setText(status)
    
    def _log(self, message: str):
        """Add a message to the log"""
        if hasattr(self, 'log_text'):
            self.log_text.append(message)
    
    def closeEvent(self, event):
        """Handle close event"""
        # Clean up thread if running
        if hasattr(self, '_bootstrapper_thread') and self._bootstrapper_thread.isRunning():
            self._bootstrapper_thread.quit()
            self._bootstrapper_thread.wait()
        event.accept()
