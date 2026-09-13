"""FastFlags editor dialog for PyFishstrap"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QLabel, QGroupBox, QFormLayout, QComboBox, QLineEdit,
    QCheckBox, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QFileDialog, QInputDialog, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QSortFilterProxyModel
from PyQt6.QtGui import QIcon, QFont, QColor
from typing import Optional, List, Dict, Any, Tuple
import json

from ...enums import BootstrapperStyle
from ...paths import Paths
from ... import App
from ...managers import FastFlagManager
from ..frontend import frontend


class FastFlagsEditorDialog(QDialog):
    """FastFlags editor dialog"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle(f"{Paths.PROJECT_NAME} - FastFlags Editor")
        self.setMinimumSize(800, 600)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        
        # Initialize UI
        self._init_ui()
        
        # Load FastFlags
        self._load_fastflags()
        
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
        self._create_editor_tab()
        self._create_presets_tab()
        self._create_about_tab()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Save button
        self.save_btn = QPushButton("Save")
        self.save_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave))
        self.save_btn.clicked.connect(self._save_fastflags)
        button_layout.addWidget(self.save_btn)
        
        # Apply button
        self.apply_btn = QPushButton("Apply")
        self.apply_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.DialogApply))
        self.apply_btn.clicked.connect(self._apply_fastflags)
        button_layout.addWidget(self.apply_btn)
        
        # Reset button
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditUndo))
        self.reset_btn.clicked.connect(self._reset_fastflags)
        button_layout.addWidget(self.reset_btn)
        
        # Cancel button
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.DialogCancel))
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
    
    def _create_editor_tab(self):
        """Create the editor tab"""
        editor_tab = QWidget()
        layout = QVBoxLayout(editor_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Search group
        search_group = QGroupBox("Search & Filter")
        search_layout = QHBoxLayout(search_group)
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search FastFlags...")
        self.search_edit.textChanged.connect(self._filter_fastflags)
        search_layout.addWidget(self.search_edit)
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("All", "all")
        self.filter_combo.addItem("Modified", "modified")
        self.filter_combo.addItem("Presets", "presets")
        self.filter_combo.currentTextChanged.connect(self._filter_fastflags)
        search_layout.addWidget(self.filter_combo)
        
        layout.addWidget(search_group)
        
        # Add new FastFlag
        add_layout = QHBoxLayout()
        
        self.new_flag_edit = QLineEdit()
        self.new_flag_edit.setPlaceholderText("Enter FastFlag name...")
        add_layout.addWidget(self.new_flag_edit)
        
        self.add_btn = QPushButton("Add")
        self.add_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd))
        self.add_btn.clicked.connect(self._add_fastflag)
        add_layout.addWidget(self.add_btn)
        
        layout.addLayout(add_layout)
        
        # FastFlags table
        self.fastflags_table = QTableWidget()
        self.fastflags_table.setColumnCount(3)
        self.fastflags_table.setHorizontalHeaderLabels(["Flag Name", "Value", "Type"])
        self.fastflags_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.fastflags_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.fastflags_table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked | QTableWidget.EditTrigger.EditKeyPressed)
        
        # Set column widths
        self.fastflags_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.fastflags_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.fastflags_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        
        # Connect cell changed signal
        self.fastflags_table.cellChanged.connect(self._cell_changed)
        
        layout.addWidget(self.fastflags_table)
        
        # Edit buttons
        edit_layout = QHBoxLayout()
        
        self.edit_btn = QPushButton("Edit Selected")
        self.edit_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.Edit))
        self.edit_btn.clicked.connect(self._edit_selected)
        edit_layout.addWidget(self.edit_btn)
        
        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditDelete))
        self.delete_btn.clicked.connect(self._delete_selected)
        edit_layout.addWidget(self.delete_btn)
        
        edit_layout.addStretch()
        
        layout.addLayout(edit_layout)
        
        self.tab_widget.addTab(editor_tab, "Editor")
    
    def _create_presets_tab(self):
        """Create the presets tab"""
        presets_tab = QWidget()
        layout = QVBoxLayout(presets_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Description
        desc_label = QLabel(
            "Presets allow you to quickly apply common FastFlag configurations. "
            "Select a preset category and value to apply."
        )
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Rendering presets group
        rendering_group = QGroupBox("Rendering")
        rendering_layout = QVBoxLayout(rendering_group)
        
        # Manual Fullscreen
        self.manual_fullscreen_combo = QComboBox()
        self.manual_fullscreen_combo.addItem("Default", None)
        self.manual_fullscreen_combo.addItem("Enabled", True)
        self.manual_fullscreen_combo.addItem("Disabled", False)
        rendering_layout.addWidget(QLabel("Manual Fullscreen:"))
        rendering_layout.addWidget(self.manual_fullscreen_combo)
        
        # Disable Scaling
        self.disable_scaling_combo = QComboBox()
        self.disable_scaling_combo.addItem("Default", None)
        self.disable_scaling_combo.addItem("Enabled", True)
        self.disable_scaling_combo.addItem("Disabled", False)
        rendering_layout.addWidget(QLabel("Disable Scaling:"))
        rendering_layout.addWidget(self.disable_scaling_combo)
        
        # MSAA
        self.msaa_combo = QComboBox()
        self.msaa_combo.addItem("Default", None)
        self.msaa_combo.addItem("1x", "1")
        self.msaa_combo.addItem("2x", "2")
        self.msaa_combo.addItem("4x", "4")
        rendering_layout.addWidget(QLabel("MSAA:"))
        rendering_layout.addWidget(self.msaa_combo)
        
        # FRM Quality Override
        self.frm_quality_combo = QComboBox()
        self.frm_quality_combo.addItem("Default", None)
        self.frm_quality_combo.addItems([str(i) for i in range(1, 11)])
        rendering_layout.addWidget(QLabel("FRM Quality Override:"))
        rendering_layout.addWidget(self.frm_quality_combo)
        
        layout.addWidget(rendering_group)
        
        # Rendering Mode group
        mode_group = QGroupBox("Rendering Mode")
        mode_layout = QVBoxLayout(mode_group)
        
        self.rendering_mode_combo = QComboBox()
        self.rendering_mode_combo.addItem("Default", "None")
        self.rendering_mode_combo.addItem("D3D11", "D3D11")
        self.rendering_mode_combo.addItem("Vulkan", "Vulkan")
        mode_layout.addWidget(self.rendering_mode_combo)
        
        layout.addWidget(mode_group)
        
        # Apply presets button
        apply_presets_btn = QPushButton("Apply Rendering Presets")
        apply_presets_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.DialogApply))
        apply_presets_btn.clicked.connect(self._apply_rendering_presets)
        layout.addWidget(apply_presets_btn)
        
        self.tab_widget.addTab(presets_tab, "Presets")
    
    def _create_about_tab(self):
        """Create the about tab"""
        about_tab = QWidget()
        layout = QVBoxLayout(about_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # About info
        about_label = QLabel(
            "<h2>FastFlags Editor</h2>"
            "<p>This editor allows you to modify Roblox client FastFlags (FFlags and DFlags).</p>"
            "<p>Changes are saved to ClientAppSettings.json in the Modifications folder.</p>"
            "<p><b>Warning:</b> Incorrect FastFlag values may cause issues with Roblox.</p>"
        )
        about_label.setWordWrap(True)
        about_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(about_label)
        
        # Import/Export group
        io_group = QGroupBox("Import/Export")
        io_layout = QHBoxLayout(io_group)
        
        self.import_btn = QPushButton("Import...")
        self.import_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentOpen))
        self.import_btn.clicked.connect(self._import_fastflags)
        io_layout.addWidget(self.import_btn)
        
        self.export_btn = QPushButton("Export...")
        self.export_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave))
        self.export_btn.clicked.connect(self._export_fastflags)
        io_layout.addWidget(self.export_btn)
        
        layout.addWidget(io_group)
        
        self.tab_widget.addTab(about_tab, "About")
    
    def _load_fastflags(self):
        """Load FastFlags from the manager"""
        # Get FastFlags from manager
        fastflags = App.fast_flags.prop
        
        # Clear table
        self.fastflags_table.setRowCount(0)
        
        # Add FastFlags to table
        row = 0
        for flag_name, flag_value in fastflags.items():
            self.fastflags_table.insertRow(row)
            
            # Flag name
            name_item = QTableWidgetItem(flag_name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.fastflags_table.setItem(row, 0, name_item)
            
            # Flag value
            value_item = QTableWidgetItem(str(flag_value) if flag_value is not None else "")
            self.fastflags_table.setItem(row, 1, value_item)
            
            # Flag type
            type_item = QTableWidgetItem(self._get_flag_type(flag_name, flag_value))
            type_item.setFlags(type_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.fastflags_table.setItem(row, 2, type_item)
            
            row += 1
        
        # Sort by flag name
        self.fastflags_table.sortItems(0)
        
        # Update presets from current values
        self._update_presets_from_fastflags()
    
    def _get_flag_type(self, flag_name: str, flag_value: Any) -> str:
        """Get the type of a FastFlag"""
        if flag_name.startswith("FFlag"):
            return "FFlag"
        elif flag_name.startswith("DFFlag"):
            return "DFFlag"
        elif flag_name.startswith("DFInt"):
            return "DFInt"
        elif flag_name.startswith("FInt"):
            return "FInt"
        else:
            return "Unknown"
    
    def _update_presets_from_fastflags(self):
        """Update preset combos from current FastFlag values"""
        fastflags = App.fast_flags.prop
        
        # Update preset values
        preset_flags = App.fast_flags.preset_flags
        
        # Manual Fullscreen
        if "FFlagHandleAltEnterFullscreenManually" in fastflags:
            value = fastflags["FFlagHandleAltEnterFullscreenManually"]
            self.manual_fullscreen_combo.setCurrentText(
                "Enabled" if value == "true" else "Disabled" if value == "false" else "Default"
            )
        
        # Disable Scaling
        if "DFFlagDisableDPIScale" in fastflags:
            value = fastflags["DFFlagDisableDPIScale"]
            self.disable_scaling_combo.setCurrentText(
                "Enabled" if value == "true" else "Disabled" if value == "false" else "Default"
            )
        
        # MSAA
        if "FIntDebugForceMSAASamples" in fastflags:
            value = fastflags["FIntDebugForceMSAASamples"]
            self.msaa_combo.setCurrentText(value if value in ["1", "2", "4"] else "Default")
        
        # FRM Quality Override
        if "DFIntDebugFRMQualityLevelOverride" in fastflags:
            value = fastflags["DFIntDebugFRMQualityLevelOverride"]
            self.frm_quality_combo.setCurrentText(value if value.isdigit() else "Default")
        
        # Rendering Mode
        if "FFlagDebugGraphicsPreferD3D11" in fastflags:
            if fastflags["FFlagDebugGraphicsPreferD3D11"] == "true":
                self.rendering_mode_combo.setCurrentText("D3D11")
            elif "FFlagDebugGraphicsPreferVulkan" in fastflags and fastflags["FFlagDebugGraphicsPreferVulkan"] == "true":
                self.rendering_mode_combo.setCurrentText("Vulkan")
            else:
                self.rendering_mode_combo.setCurrentText("Default")
    
    def _filter_fastflags(self):
        """Filter FastFlags based on search and filter criteria"""
        search_text = self.search_edit.text().lower()
        filter_type = self.filter_combo.currentData()
        
        # Get all FastFlags
        fastflags = App.fast_flags.prop
        
        # Clear table
        self.fastflags_table.setRowCount(0)
        
        # Add matching FastFlags
        row = 0
        for flag_name, flag_value in fastflags.items():
            # Check search
            if search_text and search_text not in flag_name.lower():
                continue
            
            # Check filter
            if filter_type == "presets":
                if flag_name not in App.fast_flags.preset_flags.values():
                    continue
            elif filter_type == "modified":
                # Check if modified from default
                if flag_name not in App.fast_flags.original:
                    continue
                if str(fastflags[flag_name]) == str(App.fast_flags.original[flag_name]):
                    continue
            
            self.fastflags_table.insertRow(row)
            
            # Flag name
            name_item = QTableWidgetItem(flag_name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.fastflags_table.setItem(row, 0, name_item)
            
            # Flag value
            value_item = QTableWidgetItem(str(flag_value) if flag_value is not None else "")
            self.fastflags_table.setItem(row, 1, value_item)
            
            # Flag type
            type_item = QTableWidgetItem(self._get_flag_type(flag_name, flag_value))
            type_item.setFlags(type_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.fastflags_table.setItem(row, 2, type_item)
            
            row += 1
    
    def _add_fastflag(self):
        """Add a new FastFlag"""
        flag_name = self.new_flag_edit.text().strip()
        
        if not flag_name:
            return
        
        # Check if already exists
        if flag_name in App.fast_flags.prop:
            frontend.show_message_box(
                f"FastFlag '{flag_name}' already exists.",
                QMessageBox.Icon.Warning,
                "Already Exists"
            )
            return
        
        # Get value from user
        value, ok = QInputDialog.getText(
            self,
            "Add FastFlag",
            f"Enter value for '{flag_name}':",
            QInputDialog.InputMode.Normal,
            ""
        )
        
        if ok:
            # Add to FastFlags
            App.fast_flags.set_value(flag_name, value)
            
            # Reload table
            self._load_fastflags()
            
            # Clear input
            self.new_flag_edit.clear()
    
    def _edit_selected(self):
        """Edit the selected FastFlag"""
        selected_row = self.fastflags_table.currentRow()
        
        if selected_row < 0:
            return
        
        flag_name_item = self.fastflags_table.item(selected_row, 0)
        flag_name = flag_name_item.text()
        
        current_value_item = self.fastflags_table.item(selected_row, 1)
        current_value = current_value_item.text()
        
        # Get new value from user
        value, ok = QInputDialog.getText(
            self,
            "Edit FastFlag",
            f"Enter new value for '{flag_name}':",
            QInputDialog.InputMode.Normal,
            current_value
        )
        
        if ok:
            # Update FastFlag
            if value:
                App.fast_flags.set_value(flag_name, value)
            else:
                App.fast_flags.set_value(flag_name, None)
            
            # Reload table
            self._load_fastflags()
    
    def _delete_selected(self):
        """Delete the selected FastFlag"""
        selected_row = self.fastflags_table.currentRow()
        
        if selected_row < 0:
            return
        
        flag_name_item = self.fastflags_table.item(selected_row, 0)
        flag_name = flag_name_item.text()
        
        # Confirm deletion
        result = frontend.show_message_box(
            f"Are you sure you want to delete '{flag_name}'?",
            QMessageBox.Icon.Question,
            "Delete FastFlag",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if result == QMessageBox.StandardButton.Yes:
            # Delete FastFlag
            App.fast_flags.set_value(flag_name, None)
            
            # Reload table
            self._load_fastflags()
    
    def _cell_changed(self, row: int, column: int):
        """Handle cell changed event"""
        if column != 1:  # Only handle value column
            return
        
        flag_name_item = self.fastflags_table.item(row, 0)
        value_item = self.fastflags_table.item(row, 1)
        
        if flag_name_item and value_item:
            flag_name = flag_name_item.text()
            value = value_item.text()
            
            # Update FastFlag
            if value:
                App.fast_flags.set_value(flag_name, value)
            else:
                App.fast_flags.set_value(flag_name, None)
    
    def _apply_rendering_presets(self):
        """Apply rendering presets"""
        # Manual Fullscreen
        manual_fullscreen = self.manual_fullscreen_combo.currentData()
        if manual_fullscreen is not None:
            App.fast_flags.set_value(
                "FFlagHandleAltEnterFullscreenManually",
                "true" if manual_fullscreen else "false"
            )
        
        # Disable Scaling
        disable_scaling = self.disable_scaling_combo.currentData()
        if disable_scaling is not None:
            App.fast_flags.set_value(
                "DFFlagDisableDPIScale",
                "true" if disable_scaling else "false"
            )
        
        # MSAA
        msaa = self.msaa_combo.currentData()
        if msaa is not None:
            App.fast_flags.set_value("FIntDebugForceMSAASamples", msaa)
        
        # FRM Quality Override
        frm_quality = self.frm_quality_combo.currentData()
        if frm_quality is not None:
            App.fast_flags.set_value("DFIntDebugFRMQualityLevelOverride", frm_quality)
        
        # Rendering Mode
        rendering_mode = self.rendering_mode_combo.currentText()
        if rendering_mode == "D3D11":
            App.fast_flags.set_value("FFlagDebugGraphicsPreferD3D11", "true")
            App.fast_flags.set_value("FFlagDebugGraphicsPreferVulkan", "false")
        elif rendering_mode == "Vulkan":
            App.fast_flags.set_value("FFlagDebugGraphicsPreferD3D11", "false")
            App.fast_flags.set_value("FFlagDebugGraphicsPreferVulkan", "true")
        else:
            App.fast_flags.set_value("FFlagDebugGraphicsPreferD3D11", None)
            App.fast_flags.set_value("FFlagDebugGraphicsPreferVulkan", None)
        
        # Reload table
        self._load_fastflags()
        
        frontend.show_message_box(
            "Rendering presets applied successfully!",
            QMessageBox.Icon.Information,
            "Presets Applied"
        )
    
    def _save_fastflags(self):
        """Save FastFlags to file"""
        App.fast_flags.save()
        
        frontend.show_message_box(
            "FastFlags saved successfully!",
            QMessageBox.Icon.Information,
            "Saved"
        )
        
        self.accept()
    
    def _apply_fastflags(self):
        """Apply FastFlags without saving"""
        self._save_fastflags()
        
        # Show confirmation
        frontend.show_message_box(
            "FastFlags applied successfully!",
            QMessageBox.Icon.Information,
            "Applied"
        )
    
    def _reset_fastflags(self):
        """Reset FastFlags to default"""
        result = frontend.show_message_box(
            "Are you sure you want to reset all FastFlags to default?",
            QMessageBox.Icon.Question,
            "Reset FastFlags",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if result == QMessageBox.StandardButton.Yes:
            # Reset FastFlags
            App.fast_flags._current = {}
            App.fast_flags._original = {}
            
            # Reload table
            self._load_fastflags()
            
            frontend.show_message_box(
                "FastFlags have been reset to default.",
                QMessageBox.Icon.Information,
                "FastFlags Reset"
            )
    
    def _import_fastflags(self):
        """Import FastFlags from a file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import FastFlags",
            str(Paths.base),
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            try:
                import json
                with open(file_path, 'r') as f:
                    fastflags = json.load(f)
                
                # Update FastFlags
                for flag_name, flag_value in fastflags.items():
                    App.fast_flags.set_value(flag_name, flag_value)
                
                # Reload table
                self._load_fastflags()
                
                frontend.show_message_box(
                    "FastFlags imported successfully!",
                    QMessageBox.Icon.Information,
                    "Imported"
                )
            except Exception as e:
                frontend.show_message_box(
                    f"Error importing FastFlags: {e}",
                    QMessageBox.Icon.Critical,
                    "Import Error"
                )
    
    def _export_fastflags(self):
        """Export FastFlags to a file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export FastFlags",
            str(Paths.base),
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            try:
                import json
                
                # Get FastFlags
                fastflags = App.fast_flags.prop
                
                # Save to file
                with open(file_path, 'w') as f:
                    json.dump(fastflags, f, indent=4)
                
                frontend.show_message_box(
                    "FastFlags exported successfully!",
                    QMessageBox.Icon.Information,
                    "Exported"
                )
            except Exception as e:
                frontend.show_message_box(
                    f"Error exporting FastFlags: {e}",
                    QMessageBox.Icon.Critical,
                    "Export Error"
                )
    
    def _connect_signals(self):
        """Connect signals to slots"""
        pass
    
    def closeEvent(self, event):
        """Handle close event"""
        # Save window geometry
        App.settings.prop.window_state = {
            'geometry': self.saveGeometry().toBase64().data().decode('utf-8'),
            'state': self.saveState().toBase64().data().decode('utf-8'),
        }
        App.settings.save()
        
        event.accept()
