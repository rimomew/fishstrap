"""Main window for PyFishstrap"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, 
    QPushButton, QLabel, QFrame, QGroupBox, QScrollArea, QComboBox,
    QLineEdit, QTextEdit, QCheckBox, QSpinBox, QDoubleSpinBox,
    QFormLayout, QGridLayout, QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QTimer
from PyQt6.QtGui import QIcon, QPixmap, QFont, QPalette, QColor
from typing import Optional, List, Dict, Any
import sys

from ..enums import LaunchMode, Theme, BootstrapperStyle
from ..paths import Paths
from .. import App
from .frontend import frontend


class MainWindow(QMainWindow):
    """Main window for PyFishstrap"""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle(f"{Paths.PROJECT_NAME} - Main Menu")
        self.setMinimumSize(800, 600)
        self.setWindowIcon(self._get_icon())
        
        # Initialize UI
        self._init_ui()
        
        # Load settings
        self._load_settings()
        
        # Connect signals
        self._connect_signals()
        
        # Start background tasks
        self._start_background_tasks()
    
    def _get_icon(self) -> Optional[QIcon]:
        """Get the application icon"""
        # Try to load icon from resources
        try:
            # For now, return None - icon will be set by the OS
            return None
        except Exception:
            return None
    
    def _init_ui(self):
        """Initialize the UI"""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Create header
        self._create_header(main_layout)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ccc;
            }
            QTabBar::tab {
                padding: 8px 16px;
            }
        """)
        main_layout.addWidget(self.tab_widget)
        
        # Create tabs
        self._create_home_tab()
        self._create_launch_tab()
        self._create_server_tab()
        self._create_settings_tab()
        self._create_about_tab()
    
    def _create_header(self, layout):
        """Create the header section"""
        header_frame = QFrame()
        header_frame.setFrameShape(QFrame.Shape.Panel)
        header_frame.setFrameShadow(QFrame.Shadow.Raised)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(15, 15, 15, 15)
        
        # Logo
        logo_label = QLabel()
        logo_label.setPixmap(self._get_logo())
        logo_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        header_layout.addWidget(logo_label)
        
        # Spacer
        header_layout.addStretch()
        
        # Title
        title_label = QLabel(f"<h1>{Paths.PROJECT_NAME}</h1>")
        title_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        header_layout.addWidget(title_label)
        
        layout.addWidget(header_frame)
    
    def _get_logo(self) -> Optional[QPixmap]:
        """Get the logo pixmap"""
        # Try to load logo from resources
        try:
            # For now, return a placeholder
            return None
        except Exception:
            return None
    
    def _create_home_tab(self):
        """Create the home tab"""
        home_tab = QWidget()
        layout = QVBoxLayout(home_tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Welcome message
        welcome_label = QLabel(
            f"<h2>Welcome to {Paths.PROJECT_NAME}</h2>"
            f"<p>A custom bootstrapper for Roblox with additional features.</p>"
        )
        welcome_label.setWordWrap(True)
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_label)
        
        # Quick launch buttons
        quick_launch_group = QGroupBox("Quick Launch")
        quick_launch_layout = QHBoxLayout(quick_launch_group)
        
        player_btn = QPushButton("Launch Roblox Player")
        player_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.ApplicationXExecutable))
        player_btn.clicked.connect(lambda: self._launch_roblox(LaunchMode.PLAYER))
        quick_launch_layout.addWidget(player_btn)
        
        studio_btn = QPushButton("Launch Roblox Studio")
        studio_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.ApplicationXExecutable))
        studio_btn.clicked.connect(lambda: self._launch_roblox(LaunchMode.STUDIO))
        quick_launch_layout.addWidget(studio_btn)
        
        layout.addWidget(quick_launch_group)
        
        # Recent games
        recent_group = QGroupBox("Recent Games")
        recent_layout = QVBoxLayout(recent_group)
        
        # Placeholder for recent games list
        recent_label = QLabel("No recent games")
        recent_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        recent_layout.addWidget(recent_label)
        
        layout.addWidget(recent_group)
        
        self.tab_widget.addTab(home_tab, "Home")
    
    def _create_launch_tab(self):
        """Create the launch tab"""
        launch_tab = QWidget()
        layout = QVBoxLayout(launch_tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Launch options
        options_group = QGroupBox("Launch Options")
        options_layout = QFormLayout(options_group)
        
        # Mode selection
        self.mode_combo = QComboBox()
        self.mode_combo.addItem("Player", LaunchMode.PLAYER)
        self.mode_combo.addItem("Studio", LaunchMode.STUDIO)
        options_layout.addRow("Mode:", self.mode_combo)
        
        # Channel selection
        self.channel_combo = QComboBox()
        self.channel_combo.addItem("Default", "")
        self.channel_combo.addItem("Live", "live")
        self.channel_combo.addItem("Beta", "beta")
        options_layout.addRow("Channel:", self.channel_combo)
        
        # Version input
        self.version_edit = QLineEdit()
        self.version_edit.setPlaceholderText("Leave empty for latest")
        options_layout.addRow("Version:", self.version_edit)
        
        # Custom arguments
        self.args_edit = QLineEdit()
        self.args_edit.setPlaceholderText("Additional command line arguments")
        options_layout.addRow("Arguments:", self.args_edit)
        
        layout.addWidget(options_group)
        
        # Launch button
        launch_btn = QPushButton("Launch Roblox")
        launch_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlay))
        launch_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        launch_btn.clicked.connect(self._launch_with_options)
        layout.addWidget(launch_btn)
        
        self.tab_widget.addTab(launch_tab, "Launch")
    
    def _create_server_tab(self):
        """Create the server information tab"""
        server_tab = QWidget()
        layout = QVBoxLayout(server_tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Server info group
        server_group = QGroupBox("Server Information")
        server_layout = QVBoxLayout(server_group)
        
        # Datacenter selection
        dc_layout = QHBoxLayout()
        dc_label = QLabel("Datacenter:")
        self.dc_combo = QComboBox()
        self.dc_combo.addItem("Auto", "")
        dc_layout.addWidget(dc_label)
        dc_layout.addWidget(self.dc_combo)
        server_layout.addLayout(dc_layout)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh Server Info")
        refresh_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.ViewRefresh))
        refresh_btn.clicked.connect(self._refresh_server_info)
        server_layout.addWidget(refresh_btn)
        
        # Server info display
        self.server_info_text = QTextEdit()
        self.server_info_text.setReadOnly(True)
        self.server_info_text.setPlaceholderText("Server information will appear here...")
        server_layout.addWidget(self.server_info_text)
        
        layout.addWidget(server_group)
        
        self.tab_widget.addTab(server_tab, "Servers")
    
    def _create_settings_tab(self):
        """Create the settings tab"""
        settings_tab = QWidget()
        layout = QVBoxLayout(settings_tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Settings button
        settings_btn = QPushButton("Open Settings Dialog")
        settings_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.PreferencesSystem))
        settings_btn.clicked.connect(self._open_settings)
        layout.addWidget(settings_btn)
        
        self.tab_widget.addTab(settings_tab, "Settings")
    
    def _create_about_tab(self):
        """Create the about tab"""
        about_tab = QWidget()
        layout = QVBoxLayout(about_tab)
        layout.setContentsMargins(15, 15, 15, 15)
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
        
        self.tab_widget.addTab(about_tab, "About")
    
    def _load_settings(self):
        """Load settings and update UI"""
        # Update theme
        theme_str = App.settings.prop.theme
        if theme_str == "Dark":
            frontend.theme = Theme.DARK
        elif theme_str == "Light":
            frontend.theme = Theme.LIGHT
        
        # Update style
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
            frontend.style = style_map[style_str]
    
    def _connect_signals(self):
        """Connect signals to slots"""
        pass
    
    def _start_background_tasks(self):
        """Start background tasks"""
        # Load remote data using Qt's async integration
        from ..api import RoValraClient
        import asyncio
        
        async def load_data():
            try:
                # Get datacenters
                datacenters = await RoValraClient.get_datacenters()
                if datacenters:
                    self._update_datacenters(datacenters)
                
                # Get server info
                await self._update_server_info()
            except Exception as e:
                print(f"Error loading data: {e}")
        
        # Run async task in a thread to avoid blocking the UI
        from PyQt6.QtCore import QThread
        
        class AsyncTaskThread(QThread):
            def __init__(self, coro):
                super().__init__()
                self.coro = coro
            
            def run(self):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.coro)
        
        thread = AsyncTaskThread(load_data())
        thread.start()
    
    def _update_datacenters(self, datacenters: List[str]):
        """Update the datacenter combo box"""
        self.dc_combo.clear()
        self.dc_combo.addItem("Auto", "")
        for dc in datacenters:
            self.dc_combo.addItem(dc, dc)
    
    async def _update_server_info(self, datacenter: str = ""):
        """Update server information display"""
        from ..api import RoValraClient
        
        try:
            servers = await RoValraClient.get_servers(datacenter)
            if servers and 'servers' in servers:
                info = f"Found {len(servers['servers'])} servers\n\n"
                for server in servers['servers'][:10]:  # Show first 10
                    info += f"Server ID: {server.get('server_id', 'N/A')}\n"
                
                self.server_info_text.setPlainText(info)
        except Exception as e:
            self.server_info_text.setPlainText(f"Error loading server info: {e}")
    
    def _refresh_server_info(self):
        """Refresh server information"""
        import asyncio
        from PyQt6.QtCore import QThread
        
        datacenter = self.dc_combo.currentData()
        
        class AsyncTaskThread(QThread):
            def __init__(self, coro):
                super().__init__()
                self.coro = coro
            
            def run(self):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.coro)
        
        thread = AsyncTaskThread(self._update_server_info(datacenter))
        thread.start()
    
    def _launch_roblox(self, launch_mode: LaunchMode):
        """Launch Roblox with the given mode"""
        App.launch_roblox(launch_mode)
    
    def _launch_with_options(self):
        """Launch Roblox with custom options"""
        mode = self.mode_combo.currentData()
        channel = self.channel_combo.currentData()
        version = self.version_edit.text().strip()
        args = self.args_edit.text().strip()
        
        # Build launch arguments
        launch_args = []
        if channel:
            launch_args.append(f"--channel={channel}")
        if version:
            launch_args.append(f"--version={version}")
        if args:
            launch_args.append(args)
        
        # Update launch settings
        from ..launch_settings import LaunchSettings
        App._launch_settings = LaunchSettings(launch_args)
        
        # Launch Roblox
        App.launch_roblox(mode)
    
    def _open_settings(self):
        """Open the settings dialog"""
        frontend.show_settings()
    
    def closeEvent(self, event):
        """Handle close event"""
        # Save window state
        App.settings.prop.window_state = {
            'geometry': self.saveGeometry().toBase64().data().decode('utf-8'),
            'state': self.saveState().toBase64().data().decode('utf-8'),
        }
        App.settings.save()
        
        event.accept()
