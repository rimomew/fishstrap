"""Path management for PyFishstrap"""

import os
import tempfile
from pathlib import Path


class Paths:
    """Static paths used throughout the application"""
    
    # Project info
    PROJECT_NAME = "PyFishstrap"
    PROJECT_OWNER = "PyFishstrap"
    PROJECT_REPOSITORY = "PyFishstrap/pyfishstrap"
    PROJECT_DOWNLOAD_LINK = "https://github.com/PyFishstrap/pyfishstrap/releases"
    PROJECT_HELP_LINK = "https://github.com/bloxstraplabs/bloxstrap/wiki"
    PROJECT_SUPPORT_LINK = "https://github.com/PyFishstrap/pyfishstrap/issues/new"
    PROJECT_REMOTE_DATA_LINK = "https://config.fishstrap.app/v1/Data.json"
    
    # Roblox executable names
    ROBLOX_PLAYER_APP_NAME = "RobloxPlayerBeta.exe"
    ROBLOX_STUDIO_APP_NAME = "RobloxStudioBeta.exe"
    
    # Registry key for uninstall
    UNINSTALL_KEY = f"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{PROJECT_NAME}"
    
    @staticmethod
    def get_temp_dir() -> Path:
        """Get the temp directory for the application"""
        return Path(tempfile.gettempdir()) / Paths.PROJECT_NAME
    
    @staticmethod
    def get_user_profile() -> Path:
        """Get the user profile directory"""
        return Path.home()
    
    @staticmethod
    def get_local_app_data() -> Path:
        """Get the local application data directory"""
        if os.name == 'nt':  # Windows
            return Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData' / 'Local'))
        elif os.name == 'posix':  # Linux/Mac
            return Path.home() / '.local' / 'share'
        return Path.home() / '.local'
    
    @staticmethod
    def get_desktop() -> Path:
        """Get the desktop directory"""
        if os.name == 'nt':
            return Path(os.environ.get('USERPROFILE', Path.home())) / 'Desktop'
        elif os.name == 'posix':
            return Path.home() / 'Desktop'
        return Path.home()
    
    @staticmethod
    def get_start_menu() -> Path:
        """Get the Windows start menu programs directory"""
        if os.name == 'nt':
            start_menu = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming')) / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs'
            return start_menu
        return Paths.get_desktop()
    
    @staticmethod
    def get_system_dir() -> Path:
        """Get the system directory"""
        if os.name == 'nt':
            return Path(os.environ.get('SystemRoot', 'C:\\Windows')) / 'System32'
        return Path('/usr/bin')
    
    @staticmethod
    def get_process_path() -> Path:
        """Get the current process path"""
        import sys
        return Path(sys.executable).parent
    
    # Paths that need initialization
    _base: Path = Path()
    _downloads: Path = Path()
    _saved_flag_profiles: Path = Path()
    _logs: Path = Path()
    _integrations: Path = Path()
    _versions: Path = Path()
    _modifications: Path = Path()
    _roblox: Path = Path()
    _custom_themes: Path = Path()
    _roblox_logs: Path = Path()
    _roblox_cache: Path = Path()
    _roblox_studio_cache: Path = Path()
    _application: Path = Path()
    
    @classmethod
    def initialize(cls, base_directory: Path):
        """Initialize paths with the base directory"""
        cls._base = Path(base_directory)
        cls._downloads = cls._base / "Downloads"
        cls._saved_flag_profiles = cls._base / "Profiles"
        cls._logs = cls._base / "Logs"
        cls._integrations = cls._base / "Integrations"
        cls._versions = cls._base / "Versions"
        cls._modifications = cls._base / "Modifications"
        cls._custom_themes = cls._base / "CustomThemes"
        cls._roblox = cls.get_local_app_data() / "Roblox"
        cls._roblox_logs = cls._roblox / "logs"
        cls._roblox_cache = cls._roblox / "rbx-storage"
        cls._roblox_studio_cache = Path(tempfile.gettempdir()) / "Roblox"
        cls._application = cls._base / f"{cls.PROJECT_NAME}.exe"
        
        # Ensure directories exist
        cls._downloads.mkdir(parents=True, exist_ok=True)
        cls._logs.mkdir(parents=True, exist_ok=True)
        cls._integrations.mkdir(parents=True, exist_ok=True)
        cls._versions.mkdir(parents=True, exist_ok=True)
        cls._modifications.mkdir(parents=True, exist_ok=True)
        cls._custom_themes.mkdir(parents=True, exist_ok=True)
        cls._saved_flag_profiles.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    @property
    def temp(cls) -> Path:
        """Temp directory for the application"""
        return cls.get_temp_dir()
    
    @classmethod
    @property
    def temp_updates(cls) -> Path:
        """Temp directory for updates"""
        return cls.temp / "Updates"
    
    @classmethod
    @property
    def temp_logs(cls) -> Path:
        """Temp directory for logs"""
        return cls.temp / "Logs"
    
    @classmethod
    @property
    def base(cls) -> Path:
        """Base installation directory"""
        return cls._base
    
    @classmethod
    @property
    def downloads(cls) -> Path:
        """Downloads directory"""
        return cls._downloads
    
    @classmethod
    @property
    def saved_flag_profiles(cls) -> Path:
        """Saved flag profiles directory"""
        return cls._saved_flag_profiles
    
    @classmethod
    @property
    def logs(cls) -> Path:
        """Logs directory"""
        return cls._logs
    
    @classmethod
    @property
    def integrations(cls) -> Path:
        """Integrations directory"""
        return cls._integrations
    
    @classmethod
    @property
    def versions(cls) -> Path:
        """Versions directory"""
        return cls._versions
    
    @classmethod
    @property
    def modifications(cls) -> Path:
        """Modifications directory"""
        return cls._modifications
    
    @classmethod
    @property
    def roblox(cls) -> Path:
        """Roblox directory"""
        return cls._roblox
    
    @classmethod
    @property
    def custom_themes(cls) -> Path:
        """Custom themes directory"""
        return cls._custom_themes
    
    @classmethod
    @property
    def roblox_logs(cls) -> Path:
        """Roblox logs directory"""
        return cls._roblox_logs
    
    @classmethod
    @property
    def roblox_cache(cls) -> Path:
        """Roblox cache directory"""
        return cls._roblox_cache
    
    @classmethod
    @property
    def roblox_studio_cache(cls) -> Path:
        """Roblox Studio cache directory"""
        return cls._roblox_studio_cache
    
    @classmethod
    @property
    def application(cls) -> Path:
        """Application executable path"""
        return cls._application
    
    @classmethod
    @property
    def custom_font(cls) -> Path:
        """Custom font path"""
        return cls._modifications / "content" / "fonts" / "CustomFont.ttf"
    
    @classmethod
    @property
    def initialized(cls) -> bool:
        """Check if paths have been initialized"""
        return bool(cls._base)
