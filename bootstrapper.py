"""Bootstrapper for launching Roblox with custom settings"""

import os
import sys
import time
import shutil
import zipfile
import tempfile
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio

from .enums import LaunchMode, ErrorCode, BootstrapperStyle
from .paths import Paths
from .app import App
from .launch_settings import LaunchSettings
from .managers import FastFlagManager, StateManager, GameJoinManager
from .utils import (
    is_windows, is_linux, is_mac, get_timestamp, 
    launch_process, find_roblox_executable, format_file_size
)
from .api import HttpClient, RoValraClient, RobloxClient


class Bootstrapper:
    """Handles the bootstrapping process for launching Roblox"""
    
    def __init__(self, launch_mode: LaunchMode):
        """Initialize the bootstrapper"""
        self._launch_mode = launch_mode
        self._launch_command_line = App.launch_settings.roblox_launch_args
        self._latest_version: Optional[str] = None
        self._latest_version_guid: Optional[str] = None
        self._latest_version_directory: Optional[Path] = None
        self._version_package_manifest: Optional[Dict[str, Any]] = None
        self._join_data: Optional[Dict[str, Any]] = None
        self._is_installing = False
        self._total_downloaded_bytes = 0
        self._total_packaged_bytes = 0
        self._package_extraction_success = True
        self._no_connection = False
        
        # Progress tracking
        self._progress = 0
        self._progress_max = 10000
        self._progress_increment = 1.0
        
        # Dialog reference (for UI updates)
        self.dialog = None
        
        # Mutex for preventing multiple instances
        self._mutex = None
        
        # Process tracking
        self._app_pid = 0
        self._app_window_handle = None
    
    @property
    def is_studio_launch(self) -> bool:
        """Check if this is a Studio launch"""
        return self._launch_mode != LaunchMode.PLAYER
    
    def launch(self) -> None:
        """Start the bootstrapping process"""
        const_log_ident = "Bootstrapper::Launch"
        
        try:
            # Check if we need to upgrade
            if self._must_upgrade():
                App.log(f"{const_log_ident}: Must upgrade, launching installer")
                self.launch_installer()
                return
            
            # Initialize paths if not already done
            if not Paths.initialized:
                self._initialize_paths()
            
            # Load state
            App.state.load()
            App.roblox_state.load()
            App.fast_flags.load()
            
            # Check if we need to install
            if self._must_install():
                App.log(f"{const_log_ident}: Must install, launching installer")
                self.launch_installer()
                return
            
            # Process the launch
            self._process_launch()
            
        except Exception as e:
            App.finalize_exception_handling(e)
            App.terminate(ErrorCode.ERROR_INSTALL_FAILURE)
    
    def _must_upgrade(self) -> bool:
        """Check if we must upgrade before launching"""
        # Check if force flag is active
        if App.launch_settings.force_flag.active:
            return True
        
        # Check if force reinstall is set in state
        if hasattr(App.state.prop, 'force_reinstall') and App.state.prop.force_reinstall:
            return True
        
        # Check if version GUID is empty or executable doesn't exist
        if not App.roblox_state.prop.player.versionGuid:
            return True
        
        # Check if executable exists
        if not self._get_executable_path().exists():
            return True
        
        return False
    
    def _must_install(self) -> bool:
        """Check if we must install before launching"""
        # Similar to _must_upgrade but for initial installation
        return self._must_upgrade()
    
    def _initialize_paths(self) -> None:
        """Initialize paths if not already done"""
        # Use the directory where the executable is located
        if is_windows():
            exe_path = Path(sys.executable)
            base_dir = exe_path.parent
        else:
            base_dir = Path(__file__).parent.parent
        
        Paths.initialize(base_dir)
    
    def _get_executable_path(self) -> Path:
        """Get the path to the Roblox executable"""
        if self.is_studio_launch:
            return Paths.roblox / Paths.ROBLOX_STUDIO_APP_NAME
        else:
            return Paths.roblox / Paths.ROBLOX_PLAYER_APP_NAME
    
    def _process_launch(self) -> None:
        """Process the launch"""
        const_log_ident = "Bootstrapper::_ProcessLaunch"
        
        # Check for game join data
        if App.launch_settings.roblox_launch_args:
            self._parse_launch_args()
        
        # Apply FastFlags if needed
        if App.fast_flags.has_changed():
            self._apply_fast_flags()
        
        # Launch Roblox
        self._launch_roblox()
    
    def _parse_launch_args(self) -> None:
        """Parse launch arguments"""
        args = App.launch_settings.roblox_launch_args
        
        # Parse roblox: or roblox-player: URIs
        if args.lower().startswith("roblox:") or args.lower().startswith("roblox-player:"):
            self._parse_roblox_uri(args)
    
    def _parse_roblox_uri(self, uri: str) -> None:
        """Parse a Roblox URI"""
        from urllib.parse import urlparse, parse_qs
        
        parsed = urlparse(uri)
        query_params = parse_qs(parsed.query)
        
        # Extract placeId
        if 'placeId' in query_params:
            App.game_join.set_place_id(int(query_params['placeId'][0]))
        
        # Extract universeId
        if 'universeId' in query_params:
            App.game_join.set_universe_id(int(query_params['universeId'][0]))
        
        # Extract serverId
        if 'serverId' in query_params:
            App.game_join.set_server_id(query_params['serverId'][0])
        
        # Extract launchMode
        if 'launchMode' in query_params:
            launch_mode = query_params['launchMode'][0]
            if launch_mode.lower() == 'studio':
                self._launch_mode = LaunchMode.STUDIO
        
        # Store the original launch args
        self._launch_command_line = uri
    
    def _apply_fast_flags(self) -> None:
        """Apply FastFlags to the ClientAppSettings.json file"""
        const_log_ident = "Bootstrapper::_ApplyFastFlags"
        
        try:
            # Get the FastFlags file path
            fast_flags_path = Paths.modifications / "ClientSettings" / "ClientAppSettings.json"
            
            # Ensure directory exists
            fast_flags_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save FastFlags
            App.fast_flags.save()
            
            App.log(f"{const_log_ident}: FastFlags applied")
            
        except Exception as e:
            App.log(f"{const_log_ident}: Error applying FastFlags: {e}")
    
    def _launch_roblox(self) -> None:
        """Launch Roblox"""
        const_log_ident = "Bootstrapper::_LaunchRoblox"
        
        try:
            # Get executable path
            exe_path = self._get_executable_path()
            
            if not exe_path.exists():
                App.log(f"{const_log_ident}: Executable not found: {exe_path}")
                App.terminate(ErrorCode.ERROR_INSTALL_FAILURE)
                return
            
            # Build command line arguments
            args = self._build_launch_args()
            
            # Launch the process
            App.log(f"{const_log_ident}: Launching {exe_path} with args: {args}")
            
            process = launch_process(str(exe_path), args)
            
            if process:
                # Store process info
                self._app_pid = process.pid
                
                # Wait for process to complete (optional)
                # process.wait()
                
                # Terminate the bootstrapper
                App.terminate(ErrorCode.ERROR_SUCCESS)
            else:
                App.log(f"{const_log_ident}: Failed to launch process")
                App.terminate(ErrorCode.ERROR_INSTALL_FAILURE)
                
        except Exception as e:
            App.log(f"{const_log_ident}: Error launching Roblox: {e}")
            App.terminate(ErrorCode.ERROR_INSTALL_FAILURE)
    
    def _build_launch_args(self) -> List[str]:
        """Build the launch arguments for Roblox"""
        args = []
        
        # Add channel if specified
        if App.launch_settings.has_channel():
            channel = App.launch_settings.get_channel()
            if channel:
                args.extend(["--channel", channel])
        
        # Add version if specified
        if App.launch_settings.has_version():
            version = App.launch_settings.get_version()
            if version:
                args.extend(["--version", version])
        
        # Add game join arguments
        if App.launch_settings.roblox_launch_args:
            args.append(App.launch_settings.roblox_launch_args)
        
        # Add custom arguments from settings
        if hasattr(App.settings.prop, 'roblox_launch_args'):
            custom_args = App.settings.prop.roblox_launch_args
            if custom_args:
                args.extend(custom_args.split())
        
        return args
    
    def launch_installer(self) -> None:
        """Launch the installer"""
        App.launch_installer()


class InterProcessLock:
    """Inter-process lock to prevent multiple instances"""
    
    def __init__(self, name: str):
        """Initialize the inter-process lock"""
        self._name = name
        self._is_acquired = False
        self._lock_file = None
        
        if is_windows():
            self._acquire_windows()
        else:
            self._acquire_unix()
    
    def _acquire_windows(self) -> None:
        """Acquire lock on Windows"""
        try:
            import win32file
            import win32con
            
            # Create a lock file in temp directory
            lock_path = Paths.temp / f"{self._name}.lock"
            
            # Try to create the file exclusively
            self._lock_file = open(lock_path, 'w')
            
            try:
                win32file.LockFileEx(
                    win32file.CreateFile(
                        str(lock_path),
                        win32con.GENERIC_READ | win32con.GENERIC_WRITE,
                        0,
                        None,
                        win32con.OPEN_EXISTING,
                        win32con.FILE_ATTRIBUTE_NORMAL,
                        None
                    ).handle,
                    win32con.LOCKFILE_EXCLUSIVE_LOCK | win32con.LOCKFILE_FAIL_IMMEDIATELY,
                    0,
                    0xFFFF0000,
                    0,
                    win32file.LockFileEx
                )
                self._is_acquired = True
            except Exception:
                self._lock_file.close()
                self._lock_file = None
                self._is_acquired = False
                
        except ImportError:
            # win32file not available, use file-based lock
            self._acquire_unix()
    
    def _acquire_unix(self) -> None:
        """Acquire lock on Unix-like systems"""
        import fcntl
        
        lock_path = Paths.temp / f"{self._name}.lock"
        
        try:
            self._lock_file = open(lock_path, 'w')
            fcntl.lockf(self._lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self._is_acquired = True
        except (IOError, OSError):
            self._lock_file = None
            self._is_acquired = False
    
    @property
    def is_acquired(self) -> bool:
        """Check if the lock is acquired"""
        return self._is_acquired
    
    def release(self) -> None:
        """Release the lock"""
        if self._lock_file:
            try:
                if is_windows():
                    import win32file
                    import win32con
                    
                    lock_path = Paths.temp / f"{self._name}.lock"
                    handle = win32file.CreateFile(
                        str(lock_path),
                        win32con.GENERIC_READ | win32con.GENERIC_WRITE,
                        0,
                        None,
                        win32con.OPEN_EXISTING,
                        win32con.FILE_ATTRIBUTE_NORMAL,
                        None
                    )
                    win32file.UnlockFileEx(handle.handle, 0, 0xFFFF0000, 0)
                else:
                    import fcntl
                    fcntl.lockf(self._lock_file, fcntl.LOCK_UN)
            except Exception:
                pass
            
            self._lock_file.close()
            self._lock_file = None
            self._is_acquired = False
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.release()
    
    def dispose(self) -> None:
        """Dispose the lock"""
        self.release()
