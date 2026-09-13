"""Main application class for PyFishstrap"""

import sys
import os
import platform
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

from .enums import LaunchMode, ErrorCode, NextAction, GenericTriState
from .paths import Paths
from .launch_settings import LaunchSettings, get_launch_settings
from .managers import (
    SettingsManager, StateManager, RobloxStateManager, 
    FastFlagManager, RemoteDataManager, GameJoinManager
)
from .api import HttpClient, GitHubClient, RoValraClient, RobloxClient
from .utils import (
    is_windows, is_linux, is_mac, get_os_version, 
    get_timestamp, open_url, parse_roblox_url
)


class App:
    """Main application class"""
    
    # Project constants
    PROJECT_NAME = Paths.PROJECT_NAME
    PROJECT_OWNER = Paths.PROJECT_OWNER
    PROJECT_REPOSITORY = Paths.PROJECT_REPOSITORY
    PROJECT_DOWNLOAD_LINK = Paths.PROJECT_DOWNLOAD_LINK
    PROJECT_HELP_LINK = Paths.PROJECT_HELP_LINK
    PROJECT_SUPPORT_LINK = Paths.PROJECT_SUPPORT_LINK
    PROJECT_REMOTE_DATA_LINK = Paths.PROJECT_REMOTE_DATA_LINK
    
    # Roblox executable names
    ROBLOX_PLAYER_APP_NAME = Paths.ROBLOX_PLAYER_APP_NAME
    ROBLOX_STUDIO_APP_NAME = Paths.ROBLOX_STUDIO_APP_NAME
    
    # Global instances
    _launch_settings: Optional[LaunchSettings] = None
    _settings: Optional[SettingsManager] = None
    _state: Optional[StateManager] = None
    _roblox_state: Optional[RobloxStateManager] = None
    _fast_flags: Optional[FastFlagManager] = None
    _remote_data: Optional[RemoteDataManager] = None
    _game_join: Optional[GameJoinManager] = None
    
    # Application state
    _initialized: bool = False
    _running: bool = False
    _showing_exception_dialog: bool = False
    
    @classmethod
    def initialize(cls, args: Optional[List[str]] = None) -> None:
        """Initialize the application"""
        if cls._initialized:
            return
        
        from pyfishstrap import __version__
        from pyfishstrap import __version__
        print(f"Initializing {cls.PROJECT_NAME} v{__version__}")
        
        # Initialize paths
        cls._initialize_paths()
        
        # Initialize launch settings
        if args is not None:
            cls._launch_settings = LaunchSettings(args)
        else:
            cls._launch_settings = get_launch_settings()
        
        # Initialize managers
        cls._settings = SettingsManager()
        cls._state = StateManager()
        cls._roblox_state = RobloxStateManager()
        cls._fast_flags = FastFlagManager()
        cls._remote_data = RemoteDataManager()
        cls._game_join = GameJoinManager()
        
        # Initialize HTTP client
        HttpClient.initialize()
        
        # Log system information
        cls.log_system_info()
        
        # Load settings and state
        cls._load_persistent_data()
        
        cls._initialized = True
    
    @classmethod
    def _initialize_paths(cls) -> None:
        """Initialize application paths"""
        # Check if we're running from an installed location
        # For now, use the directory where the script is located
        script_dir = Path(__file__).parent.parent
        
        # Check if this is a portable run (Settings.json and State.json exist)
        settings_file = script_dir / "Settings.json"
        state_file = script_dir / "State.json"
        
        if settings_file.exists() and state_file.exists():
            # Portable mode - use script directory as base
            Paths.initialize(script_dir)
        else:
            # Installed mode - check registry for install location
            install_location = cls._get_install_location()
            if install_location:
                Paths.initialize(Path(install_location))
            else:
                # Fallback to script directory
                Paths.initialize(script_dir)
    
    @classmethod
    def _get_install_location(cls) -> Optional[str]:
        """Get the installation location from registry (Windows only)"""
        if not is_windows():
            return None
        
        try:
            import winreg
            
            # Open the uninstall key
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                Paths.UNINSTALL_KEY
            ) as key:
                install_location = winreg.QueryValueEx(key, "InstallLocation")[0]
                if install_location and os.path.exists(install_location):
                    return install_location
        except (ImportError, FileNotFoundError, WindowsError) as e:
            print(f"Error reading install location from registry: {e}")
        
        return None
    
    @classmethod
    def log_system_info(cls) -> None:
        """Log system information"""
        system, release, version = get_os_version()
        print(f"OS: {system} {release} ({version})")
        print(f"Python: {platform.python_version()}")
        print(f"Process: {Path(__file__).parent}")
        print(f"Temp: {Paths.temp}")
        print(f"Base: {Paths.base}")
    
    @classmethod
    def _load_persistent_data(cls) -> None:
        """Load persistent data (settings, state, etc.)"""
        print("Loading persistent data...")
        
        # Load settings
        cls._settings.load()
        
        # Load state
        cls._state.load()
        
        # Load Roblox state
        cls._roblox_state.load()
        
        # Load FastFlags
        cls._fast_flags.load()
        
        print("Persistent data loaded")
    
    @classmethod
    async def load_remote_data(cls) -> None:
        """Load remote data in the background"""
        if cls._remote_data:
            await cls._remote_data.load_data()
    
    @classmethod
    def run(cls) -> None:
        """Run the application"""
        if cls._running:
            return
        
        cls._running = True
        
        try:
            # Process launch arguments
            cls.process_launch_args()
        except Exception as e:
            cls.finalize_exception_handling(e)
            cls.terminate(ErrorCode.ERROR_INSTALL_FAILURE)
    
    @classmethod
    def process_launch_args(cls) -> None:
        """Process command-line arguments and determine what to do"""
        if not cls._launch_settings:
            return
        
        launch_settings = cls._launch_settings
        
        # Check for uninstall
        if launch_settings.uninstall_flag.active:
            print("Launching uninstaller...")
            cls.launch_uninstaller()
            return
        
        # Check for menu/settings
        if launch_settings.menu_flag.active:
            print("Opening settings...")
            cls.launch_settings()
            return
        
        # Check for watcher
        if launch_settings.watcher_flag.active:
            print("Opening watcher...")
            cls.launch_watcher()
            return
        
        # Check for background updater
        if launch_settings.background_updater_flag.active:
            print("Opening background updater...")
            cls.launch_background_updater()
            return
        
        # Check for Roblox launch
        if launch_settings.roblox_launch_mode != LaunchMode.NONE:
            print(f"Launching Roblox ({launch_settings.roblox_launch_mode})...")
            cls.launch_roblox(launch_settings.roblox_launch_mode)
            return
        
        # Check for Bloxshade
        if launch_settings.bloxshade_flag.active:
            print("Opening Bloxshade config...")
            cls.launch_bloxshade_config()
            return
        
        # If no specific action and not quiet mode, show menu
        if not launch_settings.quiet_flag.active:
            print("Opening menu...")
            cls.launch_menu()
        else:
            print("Closing (quiet mode)...")
            cls.terminate()
    
    @classmethod
    def launch_settings(cls) -> None:
        """Launch the settings dialog"""
        # Try to use UI if available
        try:
            from .ui.frontend import frontend
            frontend.show_settings()
        except ImportError:
            print("Settings dialog not yet implemented (UI not available)")
            cls.terminate()
    
    @classmethod
    def launch_menu(cls) -> None:
        """Launch the main menu"""
        # Try to use UI if available
        try:
            from .ui.frontend import frontend
            frontend.show_menu()
        except ImportError:
            print("Main menu not yet implemented (UI not available)")
            cls.terminate()
    
    @classmethod
    def launch_roblox(cls, launch_mode: LaunchMode) -> None:
        """Launch Roblox in the specified mode"""
        from .bootstrapper import Bootstrapper
        
        bootstrapper = Bootstrapper(launch_mode)
        bootstrapper.launch()
    
    @classmethod
    def launch_installer(cls) -> None:
        """Launch the installer"""
        from .installer import Installer
        
        installer = Installer()
        installer.show()
    
    @classmethod
    def launch_uninstaller(cls) -> None:
        """Launch the uninstaller"""
        try:
            from .ui.frontend import frontend
            frontend.show_installer()
        except ImportError:
            print("Uninstaller not yet implemented (UI not available)")
            cls.terminate()
    
    @classmethod
    def launch_watcher(cls) -> None:
        """Launch the watcher"""
        try:
            from .ui.frontend import frontend
            frontend.show_message_box("Watcher not yet implemented")
        except ImportError:
            print("Watcher not yet implemented (UI not available)")
            cls.terminate()
    
    @classmethod
    def launch_background_updater(cls) -> None:
        """Launch the background updater"""
        try:
            from .ui.frontend import frontend
            frontend.show_message_box("Background updater not yet implemented")
        except ImportError:
            print("Background updater not yet implemented (UI not available)")
            cls.terminate()
    
    @classmethod
    def launch_bloxshade_config(cls) -> None:
        """Launch the Bloxshade configuration"""
        try:
            from .ui.frontend import frontend
            frontend.show_message_box("Bloxshade config not yet implemented")
        except ImportError:
            print("Bloxshade config not yet implemented (UI not available)")
            cls.terminate()
    
    @classmethod
    async def get_latest_release(cls) -> Optional[Dict[str, Any]]:
        """Get the latest release from GitHub"""
        try:
            release = await GitHubClient.get_latest_release(
                cls.PROJECT_OWNER, 
                cls.PROJECT_NAME
            )
            return release
        except Exception as e:
            print(f"Error getting latest release: {e}")
            return None
    
    @classmethod
    def assert_windows_os_version(cls) -> None:
        """Assert that the OS is Windows 10 or later"""
        if not is_windows():
            print("Error: PyFishstrap requires Windows 10 or later")
            cls.terminate(ErrorCode.ERROR_INVALID_FUNCTION)
        
        # Check Windows version
        system, release, version = get_os_version()
        if system != 'Windows':
            print("Error: PyFishstrap requires Windows")
            cls.terminate(ErrorCode.ERROR_INVALID_FUNCTION)
        
        # Parse Windows version
        try:
            major_version = int(release.split('.')[0])
            if major_version < 10:
                print("Error: PyFishstrap requires Windows 10 or later")
                cls.terminate(ErrorCode.ERROR_INVALID_FUNCTION)
        except (ValueError, IndexError):
            print("Error: Could not determine Windows version")
            cls.terminate(ErrorCode.ERROR_INVALID_FUNCTION)
    
    @classmethod
    def terminate(cls, exit_code: ErrorCode = ErrorCode.ERROR_SUCCESS) -> None:
        """Terminate the application with the specified exit code"""
        import asyncio
        
        # Close HTTP session
        async def cleanup():
            await HttpClient.close_session()
        
        # Run cleanup synchronously
        try:
            asyncio.run(cleanup())
        except RuntimeError:
            # Event loop already running or closed
            pass
        
        # Log termination
        print(f"Terminating with exit code {exit_code.value}")
        
        # Exit
        sys.exit(exit_code.value)
    
    @classmethod
    def soft_terminate(cls, exit_code: ErrorCode = ErrorCode.ERROR_SUCCESS) -> None:
        """Soft terminate the application (for GUI applications)"""
        print(f"Soft terminating with exit code {exit_code.value}")
        cls._running = False
    
    @classmethod
    def finalize_exception_handling(cls, exception: Exception, log: bool = True) -> None:
        """Finalize exception handling"""
        if log:
            print(f"Exception occurred: {exception}")
            import traceback
            traceback.print_exc()
        
        if cls._showing_exception_dialog:
            return
        
        cls._showing_exception_dialog = True
        
        # Send log (if implemented)
        cls.send_log()
        
        # Show error message
        print(f"An error occurred: {exception}")
        
        # Terminate
        cls.terminate(ErrorCode.ERROR_INSTALL_FAILURE)
    
    @classmethod
    def send_log(cls) -> None:
        """Send log file (placeholder for future implementation)"""
        # This would send logs to a server for debugging
        pass
    
    # Properties for global access
    @classmethod
    @property
    def launch_settings(cls) -> LaunchSettings:
        """Get the launch settings"""
        if cls._launch_settings is None:
            cls._launch_settings = get_launch_settings()
        return cls._launch_settings
    
    @classmethod
    @property
    def settings(cls) -> SettingsManager:
        """Get the settings manager"""
        if cls._settings is None:
            cls._settings = SettingsManager()
        return cls._settings
    
    @classmethod
    @property
    def state(cls) -> StateManager:
        """Get the state manager"""
        if cls._state is None:
            cls._state = StateManager()
        return cls._state
    
    @classmethod
    @property
    def roblox_state(cls) -> RobloxStateManager:
        """Get the Roblox state manager"""
        if cls._roblox_state is None:
            cls._roblox_state = RobloxStateManager()
        return cls._roblox_state
    
    @classmethod
    @property
    def fast_flags(cls) -> FastFlagManager:
        """Get the FastFlags manager"""
        if cls._fast_flags is None:
            cls._fast_flags = FastFlagManager()
        return cls._fast_flags
    
    @classmethod
    @property
    def remote_data(cls) -> RemoteDataManager:
        """Get the remote data manager"""
        if cls._remote_data is None:
            cls._remote_data = RemoteDataManager()
        return cls._remote_data
    
    @classmethod
    @property
    def game_join(cls) -> GameJoinManager:
        """Get the game join manager"""
        if cls._game_join is None:
            cls._game_join = GameJoinManager()
        return cls._game_join
    
    @classmethod
    @property
    def is_studio_visible(cls) -> bool:
        """Check if Roblox Studio is visible (has a version GUID)"""
        return bool(cls.roblox_state.prop.studio.versionGuid)


# Main entry point
def main():
    """Main entry point for PyFishstrap"""
    # Initialize the application
    App.initialize()
    
    # Run the application
    App.run()


if __name__ == "__main__":
    main()
