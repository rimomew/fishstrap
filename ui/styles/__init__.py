"""Styles for PyFishstrap UI"""

from PyQt6.QtCore import QObject
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication

from ...enums import Theme


class StyleManager(QObject):
    """Manager for application styles"""
    
    def __init__(self):
        super().__init__()
        self._current_theme = Theme.SYSTEM
    
    @property
    def current_theme(self) -> Theme:
        """Get the current theme"""
        return self._current_theme
    
    @current_theme.setter
    def current_theme(self, value: Theme):
        """Set the current theme and apply it"""
        self._current_theme = value
        self.apply_theme()
    
    def apply_theme(self):
        """Apply the current theme to the application"""
        app = QApplication.instance()
        if app is None:
            return
        
        if self._current_theme == Theme.DARK:
            self._apply_dark_theme(app)
        elif self._current_theme == Theme.LIGHT:
            self._apply_light_theme(app)
        else:
            # System theme - use default
            self._apply_system_theme(app)
    
    def _apply_dark_theme(self, app: QApplication):
        """Apply dark theme"""
        # Create dark palette
        palette = QPalette()
        
        # Base colors
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
        
        # Disabled colors
        palette.setColor(QPalette.ColorRole.Disabled, QPalette.ColorRole.Text, QColor(128, 128, 128))
        palette.setColor(QPalette.ColorRole.Disabled, QPalette.ColorRole.ButtonText, QColor(128, 128, 128))
        
        app.setPalette(palette)
        
        # Set style sheet
        app.setStyleSheet(self._get_dark_style_sheet())
    
    def _apply_light_theme(self, app: QApplication):
        """Apply light theme"""
        # Create light palette
        palette = QPalette()
        
        # Base colors
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
        
        # Disabled colors
        palette.setColor(QPalette.ColorRole.Disabled, QPalette.ColorRole.Text, QColor(128, 128, 128))
        palette.setColor(QPalette.ColorRole.Disabled, QPalette.ColorRole.ButtonText, QColor(128, 128, 128))
        
        app.setPalette(palette)
        
        # Set style sheet
        app.setStyleSheet(self._get_light_style_sheet())
    
    def _apply_system_theme(self, app: QApplication):
        """Apply system theme"""
        # Reset to default palette
        app.setPalette(QPalette())
        
        # Reset style sheet
        app.setStyleSheet("")
    
    def _get_dark_style_sheet(self) -> str:
        """Get the dark theme style sheet"""
        return """
            /* General */
            QWidget {
                background-color: #2d2d2d;
                color: #dcdcdc;
                selection-background-color: #0078d7;
                selection-color: #ffffff;
            }
            
            /* Frames */
            QFrame {
                background-color: #2d2d2d;
                border-color: #444;
            }
            
            /* Group boxes */
            QGroupBox {
                border: 1px solid #444;
                border-radius: 4px;
                margin-top: 10px;
                padding: 5px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #ffffff;
            }
            
            /* Labels */
            QLabel {
                color: #dcdcdc;
            }
            
            /* Buttons */
            QPushButton {
                background-color: #3c3c3c;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 6px 12px;
                color: #dcdcdc;
            }
            
            QPushButton:hover {
                background-color: #4a4a4a;
            }
            
            QPushButton:pressed {
                background-color: #2a2a2a;
            }
            
            QPushButton:disabled {
                background-color: #3c3c3c;
                color: #666;
            }
            
            /* Line edits */
            QLineEdit {
                background-color: #1e1e1e;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 4px 8px;
                color: #dcdcdc;
                selection-background-color: #0078d7;
            }
            
            QLineEdit:focus {
                border: 1px solid #0078d7;
            }
            
            /* Text edits */
            QTextEdit {
                background-color: #1e1e1e;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 4px;
                color: #dcdcdc;
                selection-background-color: #0078d7;
            }
            
            /* Combo boxes */
            QComboBox {
                background-color: #1e1e1e;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 4px 8px;
                color: #dcdcdc;
            }
            
            QComboBox:focus {
                border: 1px solid #0078d7;
            }
            
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                border: 1px solid #444;
                color: #dcdcdc;
                selection-background-color: #0078d7;
            }
            
            /* Check boxes */
            QCheckBox {
                spacing: 5px;
                color: #dcdcdc;
            }
            
            QCheckBox:indicator {
                width: 18px;
                height: 18px;
            }
            
            QCheckBox:indicator:checked {
                background-color: #0078d7;
                border: 1px solid #0078d7;
            }
            
            QCheckBox:indicator:unchecked {
                background-color: #444;
                border: 1px solid #444;
            }
            
            /* Progress bars */
            QProgressBar {
                border: 1px solid #444;
                border-radius: 4px;
                text-align: center;
                background-color: #3c3c3c;
                color: #dcdcdc;
            }
            
            QProgressBar::chunk {
                background-color: #0078d7;
                border-radius: 3px;
            }
            
            /* Tab widgets */
            QTabWidget {
                background-color: #2d2d2d;
            }
            
            QTabWidget::pane {
                border: 1px solid #444;
                border-radius: 4px;
                background-color: #2d2d2d;
            }
            
            QTabBar::tab {
                background-color: #3c3c3c;
                border: 1px solid #444;
                border-bottom: none;
                border-radius: 4px 4px 0 0;
                padding: 8px 16px;
                color: #dcdcdc;
            }
            
            QTabBar::tab:selected {
                background-color: #2d2d2d;
                border-bottom: 1px solid #2d2d2d;
            }
            
            QTabBar::tab:hover {
                background-color: #4a4a4a;
            }
            
            /* Scroll bars */
            QScrollBar:vertical {
                border: 1px solid #444;
                background-color: #2d2d2d;
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #444;
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #555;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            
            /* Table widgets */
            QTableWidget {
                background-color: #2d2d2d;
                border: 1px solid #444;
                border-radius: 4px;
                gridline-color: #444;
            }
            
            QHeaderView {
                background-color: #3c3c3c;
                border: 1px solid #444;
                border-radius: 4px 4px 0 0;
            }
            
            QHeaderView::section {
                background-color: #3c3c3c;
                color: #dcdcdc;
                padding: 4px 8px;
                border: 1px solid #444;
                border-radius: 0px;
            }
            
            QTableWidget::item {
                background-color: #2d2d2d;
                color: #dcdcdc;
                padding: 4px;
            }
            
            QTableWidget::item:selected {
                background-color: #0078d7;
                color: #ffffff;
            }
            
            /* Message boxes */
            QMessageBox {
                background-color: #2d2d2d;
                color: #dcdcdc;
            }
            
            QMessageBox QLabel {
                color: #dcdcdc;
            }
            
            QMessageBox QPushButton {
                background-color: #3c3c3c;
                border: 1px solid #555;
                color: #dcdcdc;
            }
            
            QMessageBox QPushButton:hover {
                background-color: #4a4a4a;
            }
        """
    
    def _get_light_style_sheet(self) -> str:
        """Get the light theme style sheet"""
        return """
            /* General */
            QWidget {
                background-color: #f0f0f0;
                color: #303030;
                selection-background-color: #0078d7;
                selection-color: #ffffff;
            }
            
            /* Frames */
            QFrame {
                background-color: #f0f0f0;
                border-color: #ccc;
            }
            
            /* Group boxes */
            QGroupBox {
                border: 1px solid #ccc;
                border-radius: 4px;
                margin-top: 10px;
                padding: 5px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #000000;
            }
            
            /* Labels */
            QLabel {
                color: #303030;
            }
            
            /* Buttons */
            QPushButton {
                background-color: #e0e0e0;
                border: 1px solid #aaa;
                border-radius: 4px;
                padding: 6px 12px;
                color: #303030;
            }
            
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            
            QPushButton:pressed {
                background-color: #c0c0c0;
            }
            
            QPushButton:disabled {
                background-color: #e0e0e0;
                color: #888;
            }
            
            /* Line edits */
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 4px 8px;
                color: #303030;
                selection-background-color: #0078d7;
            }
            
            QLineEdit:focus {
                border: 1px solid #0078d7;
            }
            
            /* Text edits */
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 4px;
                color: #303030;
                selection-background-color: #0078d7;
            }
            
            /* Combo boxes */
            QComboBox {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 4px 8px;
                color: #303030;
            }
            
            QComboBox:focus {
                border: 1px solid #0078d7;
            }
            
            QComboBox QAbstractItemView {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                color: #303030;
                selection-background-color: #0078d7;
            }
            
            /* Check boxes */
            QCheckBox {
                spacing: 5px;
                color: #303030;
            }
            
            QCheckBox:indicator {
                width: 18px;
                height: 18px;
            }
            
            QCheckBox:indicator:checked {
                background-color: #0078d7;
                border: 1px solid #0078d7;
            }
            
            QCheckBox:indicator:unchecked {
                background-color: #ccc;
                border: 1px solid #ccc;
            }
            
            /* Progress bars */
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 4px;
                text-align: center;
                background-color: #e0e0e0;
                color: #303030;
            }
            
            QProgressBar::chunk {
                background-color: #0078d7;
                border-radius: 3px;
            }
            
            /* Tab widgets */
            QTabWidget {
                background-color: #f0f0f0;
            }
            
            QTabWidget::pane {
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #f0f0f0;
            }
            
            QTabBar::tab {
                background-color: #e0e0e0;
                border: 1px solid #ccc;
                border-bottom: none;
                border-radius: 4px 4px 0 0;
                padding: 8px 16px;
                color: #303030;
            }
            
            QTabBar::tab:selected {
                background-color: #f0f0f0;
                border-bottom: 1px solid #f0f0f0;
            }
            
            QTabBar::tab:hover {
                background-color: #d0d0d0;
            }
            
            /* Scroll bars */
            QScrollBar:vertical {
                border: 1px solid #ccc;
                background-color: #f0f0f0;
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #ccc;
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #bbb;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            
            /* Table widgets */
            QTableWidget {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 4px;
                gridline-color: #ccc;
            }
            
            QHeaderView {
                background-color: #e0e0e0;
                border: 1px solid #ccc;
                border-radius: 4px 4px 0 0;
            }
            
            QHeaderView::section {
                background-color: #e0e0e0;
                color: #303030;
                padding: 4px 8px;
                border: 1px solid #ccc;
                border-radius: 0px;
            }
            
            QTableWidget::item {
                background-color: #f0f0f0;
                color: #303030;
                padding: 4px;
            }
            
            QTableWidget::item:selected {
                background-color: #0078d7;
                color: #ffffff;
            }
            
            /* Message boxes */
            QMessageBox {
                background-color: #f0f0f0;
                color: #303030;
            }
            
            QMessageBox QLabel {
                color: #303030;
            }
            
            QMessageBox QPushButton {
                background-color: #e0e0e0;
                border: 1px solid #aaa;
                color: #303030;
            }
            
            QMessageBox QPushButton:hover {
                background-color: #d0d0d0;
            }
        """


# Global style manager instance
style_manager = StyleManager()
