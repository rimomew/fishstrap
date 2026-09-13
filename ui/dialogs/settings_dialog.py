"""Settings dialog for PyFishstrap"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QLabel, QGroupBox, QFormLayout, QComboBox, QLineEdit,
    QCheckBox, QSpinBox, QPushButton, QFileDialog, QColorDialog,
    QScrollArea, QFrame, QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QFont, QPalette, QColor
from typing import Optional, List, Dict, Any
import sys

from ...enums import Theme, BootstrapperStyle, ChannelChangeMode, CursorType, EmojiType
from ...paths import Paths
from ... import App
from ..frontend import frontend


class SettingsDialog(QDialog):
    """Settings dialog for PyFishstrap"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle(f"{Paths.PROJECT_NAME} - Settings")
        self.setMinimumSize(700, 500)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        
        # Initialize UI
        self._init_ui()
        
        # Load settings
        self._load_settings()
        
        # Connect signals
        self._connect_signals()
    
    def _init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Create tabs
        self._create_general_tab()
        self._create_appearance_tab()
        self._create_roblox_tab()
        self._create_fastflags_tab()
        self._create_integrations_tab()
        self._create_about_tab()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Save button
        self.save_btn = QPushButton("Save")
        self.save_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave))
        self.save_btn.clicked.connect(self._save_settings)
        button_layout.addWidget(self.save_btn)
        
        # Cancel button
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.DialogCancel))
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        # Apply button
        self.apply_btn = QPushButton("Apply")
        self.apply_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.DialogApply))
        self.apply_btn.clicked.connect(self._apply_settings)
        button_layout.addWidget(self.apply_btn)
        
        layout.addLayout(button_layout)
    
    def _create_general_tab(self):
        """Create the general settings tab"""
        general_tab = QWidget()
        layout = QVBoxLayout(general_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Language group
        language_group = QGroupBox("Language")
        language_layout = QFormLayout(language_group)
        
        self.language_combo = QComboBox()
        self.language_combo.addItem("English (US)", "en-us")
        self.language_combo.addItem("English (UK)", "en-gb")
        # Add more languages as needed
        language_layout.addRow("Locale:", self.language_combo)
        
        layout.addWidget(language_group)
        
        # Updates group
        updates_group = QGroupBox("Updates")
        updates_layout = QFormLayout(updates_group)
        
        self.check_updates_check = QCheckBox("Check for updates on startup")
        updates_layout.addRow(self.check_updates_check)
        
        self.force_local_data_check = QCheckBox("Force local data (offline mode)")
        updates_layout.addRow(self.force_local_data_check)
        
        layout.addWidget(updates_group)
        
        # Logging group
        logging_group = QGroupBox("Logging")
        logging_layout = QFormLayout(logging_group)
        
        self.enable_logging_check = QCheckBox("Enable logging")
        logging_layout.addRow(self.enable_logging_check)
        
        self.log_level_combo = QComboBox()
        self.log_level_combo.addItems(["Error", "Warning", "Info", "Debug", "Trace"])
        logging_layout.addRow("Log level:", self.log_level_combo)
        
        layout.addWidget(logging_group)
        
        self.tab_widget.addTab(general_tab, "General")
    
    def _create_appearance_tab(self):
        """Create the appearance settings tab"""
        appearance_tab = QWidget()
        layout = QVBoxLayout(appearance_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Theme group
        theme_group = QGroupBox("Theme")
        theme_layout = QFormLayout(theme_group)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("System", "System")
        self.theme_combo.addItem("Light", "Light")
        self.theme_combo.addItem("Dark", "Dark")
        theme_layout.addRow("Application theme:", self.theme_combo)
        
        layout.addWidget(theme_group)
        
        # Bootstrapper style group
        style_group = QGroupBox("Bootstrapper Style")
        style_layout = QFormLayout(style_group)
        
        self.style_combo = QComboBox()
        self.style_combo.addItem("Classic", "Classic")
        self.style_combo.addItem("Fluent", "Fluent")
        self.style_combo.addItem("Terminal", "Terminal")
        self.style_combo.addItem("Byfron", "Byfron")
        self.style_combo.addItem("2025", "TwentyFive")
        self.style_combo.addItem("Legacy 2008", "Legacy2008")
        self.style_combo.addItem("Legacy 2011", "Legacy2011")
        self.style_combo.addItem("Vista", "Vista")
        self.style_combo.addItem("Custom", "Custom")
        style_layout.addRow("Bootstrapper style:", self.style_combo)
        
        layout.addWidget(style_group)
        
        # Cursor group
        cursor_group = QGroupBox("Cursor")
        cursor_layout = QFormLayout(cursor_group)
        
        self.cursor_combo = QComboBox()
        self.cursor_combo.addItem("Default", "Default")
        self.cursor_combo.addItem("2006", "From2006")
        self.cursor_combo.addItem("2013", "From2013")
        cursor_layout.addRow("Cursor type:", self.cursor_combo)
        
        self.custom_cursor_check = QCheckBox("Enable custom cursor")
        cursor_layout.addRow(self.custom_cursor_check)
        
        self.cursor_path_edit = QLineEdit()
        self.cursor_path_edit.setPlaceholderText("Path to custom cursor file")
        cursor_layout.addRow("Cursor path:", self.cursor_path_edit)
        
        self.cursor_browse_btn = QPushButton("Browse...")
        self.cursor_browse_btn.clicked.connect(self._browse_cursor)
        cursor_layout.addRow("", self.cursor_browse_btn)
        
        layout.addWidget(cursor_group)
        
        # Emoji group
        emoji_group = QGroupBox("Emoji")
        emoji_layout = QFormLayout(emoji_group)
        
        self.emoji_combo = QComboBox()
        self.emoji_combo.addItem("Roblox", "Roblox")
        self.emoji_combo.addItem("Discord", "Discord")
        self.emoji_combo.addItem("Twitter", "Twitter")
        emoji_layout.addRow("Emoji type:", self.emoji_combo)
        
        layout.addWidget(emoji_group)
        
        self.tab_widget.addTab(appearance_tab, "Appearance")
    
    def _create_roblox_tab(self):
        """Create the Roblox settings tab"""
        roblox_tab = QWidget()
        layout = QVBoxLayout(roblox_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Channel group
        channel_group = QGroupBox("Channel")
        channel_layout = QFormLayout(channel_group)
        
        self.channel_mode_combo = QComboBox()
        self.channel_mode_combo.addItem("Automatic", "Automatic")
        self.channel_mode_combo.addItem("Manual", "Manual")
        channel_layout.addRow("Channel change mode:", self.channel_mode_combo)
        
        self.selected_channel_combo = QComboBox()
        self.selected_channel_combo.addItem("Default", "")
        self.selected_channel_combo.addItem("Live", "live")
        self.selected_channel_combo.addItem("Beta", "beta")
        channel_layout.addRow("Selected channel:", self.selected_channel_combo)
        
        layout.addWidget(channel_group)
        
        # Launch options group
        launch_group = QGroupBox("Launch Options")
        launch_layout = QFormLayout(launch_group)
        
        self.static_directory_check = QCheckBox("Use static directory")
        launch_layout.addRow(self.static_directory_check)
        
        self.nolaunch_check = QCheckBox("Don't launch after bootstrapping")
        launch_layout.addRow(self.nolaunch_check)
        
        layout.addWidget(launch_group)
        
        # Custom bootstrapper group
        custom_group = QGroupBox("Custom Bootstrapper")
        custom_layout = QFormLayout(custom_group)
        
        self.custom_bootstrapper_check = QCheckBox("Enable custom bootstrapper")
        custom_layout.addRow(self.custom_bootstrapper_check)
        
        self.custom_bootstrapper_path_edit = QLineEdit()
        self.custom_bootstrapper_path_edit.setPlaceholderText("Path to custom bootstrapper template")
        custom_layout.addRow("Template path:", self.custom_bootstrapper_path_edit)
        
        self.bootstrapper_browse_btn = QPushButton("Browse...")
        self.bootstrapper_browse_btn.clicked.connect(self._browse_bootstrapper)
        custom_layout.addRow("", self.bootstrapper_browse_btn)
        
        layout.addWidget(custom_group)
        
        self.tab_widget.addTab(roblox_tab, "Roblox")
    
    def _create_fastflags_tab(self):
        """Create the FastFlags settings tab"""
        fastflags_tab = QWidget()
        layout = QVBoxLayout(fastflags_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # FastFlags group
        ff_group = QGroupBox("FastFlags")
        ff_layout = QVBoxLayout(ff_group)
        
        # Description
        desc_label = QLabel(
            "FastFlags (FFlags/DFlags) are Roblox client settings that can be customized. "
            "These settings are applied to ClientAppSettings.json."
        )
        desc_label.setWordWrap(True)
        ff_layout.addWidget(desc_label)
        
        # Open editor button
        self.edit_fastflags_btn = QPushButton("Open FastFlags Editor")
        self.edit_fastflags_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.PreferencesSystem))
        self.edit_fastflags_btn.clicked.connect(self._open_fastflags_editor)
        ff_layout.addWidget(self.edit_fastflags_btn)
        
        layout.addWidget(ff_group)
        
        # Global Basic Settings group
        gbs_group = QGroupBox("Global Basic Settings")
        gbs_layout = QVBoxLayout(gbs_group)
        
        gbs_desc_label = QLabel(
            "Global Basic Settings allow you to customize Roblox client behavior."
        )
        gbs_desc_label.setWordWrap(True)
        gbs_layout.addWidget(gbs_desc_label)
        
        self.edit_gbs_btn = QPushButton("Open Global Basic Settings Editor")
        self.edit_gbs_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.PreferencesSystem))
        self.edit_gbs_btn.clicked.connect(self._open_gbs_editor)
        gbs_layout.addWidget(self.edit_gbs_btn)
        
        layout.addWidget(gbs_group)
        
        self.tab_widget.addTab(fastflags_tab, "FastFlags & GBS")
    
    def _create_integrations_tab(self):
        """Create the integrations settings tab"""
        integrations_tab = QWidget()
        layout = QVBoxLayout(integrations_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Discord RPC group
        discord_group = QGroupBox("Discord Rich Presence")
        discord_layout = QFormLayout(discord_group)
        
        self.discord_rpc_check = QCheckBox("Enable Discord Rich Presence")
        discord_layout.addRow(self.discord_rpc_check)
        
        self.discord_status_combo = QComboBox()
        self.discord_status_combo.addItem("Show both game and universe name", "Both")
        self.discord_status_combo.addItem("Show game name only", "GameName")
        self.discord_status_combo.addItem("Show universe name only", "UniverseName")
        self.discord_status_combo.addItem("Show nothing", "None")
        discord_layout.addRow("Status display:", self.discord_status_combo)
        
        layout.addWidget(discord_group)
        
        # Cookies group
        cookies_group = QGroupBox("Cookies")
        cookies_layout = QFormLayout(cookies_group)
        
        self.allow_cookie_access_check = QCheckBox("Allow cookie access")
        cookies_layout.addRow(self.allow_cookie_access_check)
        
        layout.addWidget(cookies_group)
        
        self.tab_widget.addTab(integrations_tab, "Integrations")
    
    def _create_about_tab(self):
        """Create the about tab"""
        about_tab = QWidget()
        layout = QVBoxLayout(about_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # About info
        about_label = QLabel(
            f"<h2>{Paths.PROJECT_NAME}</h2>"
            f"<p>Version: 0.1.0</p>"
            f"<p>A custom bootstrapper for Roblox based on Bloxstrap.</p>"
            f"<p>Project: <a href='{Paths.PROJECT_REPOSITORY}'>{Paths.PROJECT_REPOSITORY}</a></p>"
        )
        about_label.setWordWrap(True)
        about_label.setOpenExternalLinks(True)
        about_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(about_label)
        
        # Special thanks
        thanks_label = QLabel(
            "<h3>Special Thanks</h3>"
            "<p>Valra for providing their API<br/>"
            "Other independent contributors</p>"
        )
        thanks_label.setWordWrap(True)
        thanks_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(thanks_label)
        
        # Reset settings button
        reset_btn = QPushButton("Reset Settings to Default")
        reset_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditUndo))
        reset_btn.clicked.connect(self._reset_settings)
        layout.addWidget(reset_btn)
        
        self.tab_widget.addTab(about_tab, "About")
    
    def _load_settings(self):
        """Load settings from the settings manager"""
        settings = App.settings.prop
        
        # General
        self.language_combo.setCurrentText(settings.locale)
        self.check_updates_check.setChecked(settings.checkForUpdates)
        self.force_local_data_check.setChecked(settings.forceLocalData)
        self.enable_logging_check.setChecked(settings.enableLogging)
        self.log_level_combo.setCurrentText(settings.logLevel)
        
        # Appearance
        self.theme_combo.setCurrentText(settings.theme)
        self.style_combo.setCurrentText(settings.bootstrapperStyle)
        self.cursor_combo.setCurrentText(settings.cursorType)
        self.custom_cursor_check.setChecked(settings.customFontEnabled)
        self.cursor_path_edit.setText(settings.customFontPath)
        self.emoji_combo.setCurrentText(settings.emojiType)
        
        # Roblox
        self.channel_mode_combo.setCurrentText(settings.channelChangeMode)
        self.selected_channel_combo.setCurrentText(settings.selectedChannel)
        self.static_directory_check.setChecked(settings.staticDirectory)
        self.nolaunch_check.setChecked(False)  # Not stored in settings
        self.custom_bootstrapper_check.setChecked(settings.customBootstrapperEnabled)
        self.custom_bootstrapper_path_edit.setText(settings.customBootstrapperPath)
        
        # Integrations
        self.discord_rpc_check.setChecked(settings.discordRPC)
        self.discord_status_combo.setCurrentText(settings.discordRPCStatusDisplay)
        self.allow_cookie_access_check.setChecked(settings.allowCookieAccess)
    
    def _save_settings(self):
        """Save settings to the settings manager"""
        settings = App.settings.prop
        
        # General
        settings.locale = self.language_combo.currentData()
        settings.checkForUpdates = self.check_updates_check.isChecked()
        settings.forceLocalData = self.force_local_data_check.isChecked()
        settings.enableLogging = self.enable_logging_check.isChecked()
        settings.logLevel = self.log_level_combo.currentText()
        
        # Appearance
        settings.theme = self.theme_combo.currentText()
        settings.bootstrapperStyle = self.style_combo.currentText()
        settings.cursorType = self.cursor_combo.currentText()
        settings.customFontEnabled = self.custom_cursor_check.isChecked()
        settings.customFontPath = self.cursor_path_edit.text()
        settings.emojiType = self.emoji_combo.currentText()
        
        # Roblox
        settings.channelChangeMode = self.channel_mode_combo.currentText()
        settings.selectedChannel = self.selected_channel_combo.currentData()
        settings.staticDirectory = self.static_directory_check.isChecked()
        settings.customBootstrapperEnabled = self.custom_bootstrapper_check.isChecked()
        settings.customBootstrapperPath = self.custom_bootstrapper_path_edit.text()
        
        # Integrations
        settings.discordRPC = self.discord_rpc_check.isChecked()
        settings.discordRPCStatusDisplay = self.discord_status_combo.currentText()
        settings.allowCookieAccess = self.allow_cookie_access_check.isChecked()
        
        # Save settings
        App.settings.save()
        
        # Apply theme
        theme_str = settings.theme
        if theme_str == "Dark":
            frontend.theme = Theme.DARK
        elif theme_str == "Light":
            frontend.theme = Theme.LIGHT
        else:
            frontend.theme = Theme.SYSTEM
        
        # Apply style
        style_str = settings.bootstrapperStyle
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
            frontend.style = style_map[style_str]
        
        # Close dialog
        self.accept()
    
    def _apply_settings(self):
        """Apply settings without closing the dialog"""
        self._save_settings()
        
        # Show confirmation
        frontend.show_message_box(
            "Settings applied successfully!",
            QMessageBox.Icon.Information,
            "Settings Applied"
        )
    
    def _connect_signals(self):
        """Connect signals to slots"""
        # Enable/disable custom cursor path based on checkbox
        self.custom_cursor_check.stateChanged.connect(
            lambda state: self.cursor_path_edit.setEnabled(state == Qt.CheckState.Checked)
        )
        self.cursor_browse_btn.setEnabled(self.custom_cursor_check.isChecked())
        
        # Enable/disable custom bootstrapper path based on checkbox
        self.custom_bootstrapper_check.stateChanged.connect(
            lambda state: self.custom_bootstrapper_path_edit.setEnabled(state == Qt.CheckState.Checked)
        )
        self.bootstrapper_browse_btn.setEnabled(self.custom_bootstrapper_check.isChecked())
    
    def _browse_cursor(self):
        """Browse for cursor file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Cursor File",
            str(Paths.base),
            "Font Files (*.ttf);;All Files (*)"
        )
        
        if file_path:
            self.cursor_path_edit.setText(file_path)
    
    def _browse_bootstrapper(self):
        """Browse for bootstrapper template"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Bootstrapper Template",
            str(Paths.base),
            "XML Files (*.xml);;All Files (*)"
        )
        
        if file_path:
            self.custom_bootstrapper_path_edit.setText(file_path)
    
    def _open_fastflags_editor(self):
        """Open the FastFlags editor"""
        from .fast_flags_editor import FastFlagsEditorDialog
        
        dialog = FastFlagsEditorDialog(self)
        dialog.exec()
    
    def _open_gbs_editor(self):
        """Open the Global Basic Settings editor"""
        # This will be implemented later
        frontend.show_message_box(
            "Global Basic Settings editor not yet implemented",
            QMessageBox.Icon.Information,
            "Not Implemented"
        )
    
    def _reset_settings(self):
        """Reset settings to default"""
        result = frontend.show_message_box(
            "Are you sure you want to reset all settings to default?",
            QMessageBox.Icon.Question,
            "Reset Settings",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if result == QMessageBox.StandardButton.Yes:
            # Reset settings to default
            App.settings._current = App.settings.data_class()
            App.settings.save()
            
            # Reload settings in UI
            self._load_settings()
            
            frontend.show_message_box(
                "Settings have been reset to default.",
                QMessageBox.Icon.Information,
                "Settings Reset"
            )
    
    def closeEvent(self, event):
        """Handle close event"""
        # Save window geometry
        App.settings.prop.window_state = {
            'geometry': self.saveGeometry().toBase64().data().decode('utf-8'),
            'state': self.saveState().toBase64().data().decode('utf-8'),
        }
        App.settings.save()
        
        event.accept()
