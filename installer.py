"""Installer for PyFishstrap"""

import os
import sys
import shutil
import tempfile
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any
import asyncio

from .enums import ErrorCode
from .paths import Paths
from .app import App
from .api import HttpClient, GitHubClient
from .utils import (
    is_windows, is_linux, is_mac, get_timestamp,
    format_file_size, open_url
)


class Installer:
    """Handles installation and updates of PyFishstrap"""
    
    def __init__(self):
        """Initialize the installer"""
        self._install_location: Optional[Path] = None
        self._is_implicit_install: bool = False
        self._finished: bool = False
        self._close_action: Optional[str] = None
        
        # UI elements (will be implemented later)
        self._dialog = None
    
    @property
    def install_location(self) -> Optional[Path]:
        """Get the installation location"""
        return self._install_location
    
    @install_location.setter
    def install_location(self, value: Path) -> None:
        """Set the installation location"""
        self._install_location = value
    
    @property
    def is_implicit_install(self) -> bool:
        """Check if this is an implicit install"""
        return self._is_implicit_install
    
    @property
    def finished(self) -> bool:
        """Check if installation is finished"""
        return self._finished
    
    @property
    def close_action(self) -> Optional[str]:
        """Get the close action"""
        return self._close_action
    
    def show(self) -> None:
        """Show the installer dialog"""
        # This will be implemented with the UI
        print("Installer dialog not yet implemented")
        
        # For now, do a silent install
        self._do_install()
    
    def check_install_location(self) -> bool:
        """Check if the install location is valid"""
        if self._install_location is None:
            return False
        
        # Check if directory exists and is writable
        if not self._install_location.exists():
            try:
                self._install_location.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"Error creating install location: {e}")
                return False
        
        # Check if we have write permissions
        try:
            test_file = self._install_location / "test_write.txt"
            test_file.write_text("test")
            test_file.unlink()
        except Exception as e:
            print(f"Error testing write permissions: {e}")
            return False
        
        return True
    
    def do_install(self) -> bool:
        """Perform the installation"""
        const_log_ident = "Installer::DoInstall"
        
        try:
            # Ensure install location is valid
            if not self.check_install_location():
                print(f"{const_log_ident}: Invalid install location")
                return False
            
            # Initialize paths with install location
            Paths.initialize(self._install_location)
            
            # Create directories
            self._create_directories()
            
            # Copy files
            self._copy_files()
            
            # Create shortcuts
            self._create_shortcuts()
            
            # Register in registry (Windows only)
            if is_windows():
                self._register_in_registry()
            
            # Save settings
            self._save_settings()
            
            print(f"{const_log_ident}: Installation completed successfully")
            self._finished = True
            return True
            
        except Exception as e:
            print(f"{const_log_ident}: Error during installation: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _create_directories(self) -> None:
        """Create necessary directories"""
        # These will be created by Paths.initialize
        pass
    
    def _copy_files(self) -> None:
        """Copy application files to install location"""
        const_log_ident = "Installer::_CopyFiles"
        
        # Get current script directory
        script_dir = Path(__file__).parent
        
        # Copy Python files
        files_to_copy = [
            "__init__.py",
            "app.py",
            "bootstrapper.py",
            "installer.py",
            "launch_settings.py",
            "paths.py",
        ]
        
        for file_name in files_to_copy:
            src = script_dir / file_name
            dst = self._install_location / file_name
            
            if src.exists():
                try:
                    shutil.copy2(src, dst)
                except Exception as e:
                    print(f"{const_log_ident}: Error copying {file_name}: {e}")
        
        # Copy the entire package
        package_dir = script_dir.parent
        for item in package_dir.iterdir():
            if item.is_dir() and not item.name.startswith('__'):
                dst_dir = self._install_location / item.name
                if dst_dir.exists():
                    shutil.rmtree(dst_dir)
                shutil.copytree(item, dst_dir)
    
    def _create_shortcuts(self) -> None:
        """Create desktop and start menu shortcuts"""
        const_log_ident = "Installer::_CreateShortcuts"
        
        if not is_windows():
            return
        
        try:
            import win32com.client
            
            # Create desktop shortcut
            desktop = Paths.get_desktop()
            shortcut_path = desktop / f"{Paths.PROJECT_NAME}.lnk"
            
            self._create_shortcut(shortcut_path, f"Launch {Paths.PROJECT_NAME}")
            
            # Create start menu shortcut
            start_menu = Paths.get_start_menu()
            start_menu_path = start_menu / Paths.PROJECT_NAME
            start_menu_path.mkdir(parents=True, exist_ok=True)
            
            shortcut_path = start_menu_path / f"{Paths.PROJECT_NAME}.lnk"
            self._create_shortcut(shortcut_path, f"Launch {Paths.PROJECT_NAME}")
            
            # Create uninstall shortcut
            uninstall_shortcut = start_menu_path / f"Uninstall {Paths.PROJECT_NAME}.lnk"
            self._create_shortcut(
                uninstall_shortcut,
                f"Uninstall {Paths.PROJECT_NAME}",
                arguments="--uninstall"
            )
            
            # Create settings shortcut
            settings_shortcut = start_menu_path / f"{Paths.PROJECT_NAME} Settings.lnk"
            self._create_shortcut(
                settings_shortcut,
                f"{Paths.PROJECT_NAME} Settings",
                arguments="--menu"
            )
            
        except ImportError:
            print(f"{const_log_ident}: win32com not available, skipping shortcuts")
        except Exception as e:
            print(f"{const_log_ident}: Error creating shortcuts: {e}")
    
    def _create_shortcut(self, path: Path, description: str, arguments: str = "") -> None:
        """Create a Windows shortcut"""
        import win32com.client
        
        # Get the target path (Python executable)
        target = sys.executable
        
        # Get the working directory (install location)
        working_dir = str(self._install_location)
        
        # Create shortcut
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(str(path))
        
        shortcut.TargetPath = target
        shortcut.WorkingDirectory = working_dir
        shortcut.Description = description
        shortcut.Arguments = arguments
        
        # Set icon (optional)
        # shortcut.IconLocation = str(self._install_location / "icon.ico")
        
        shortcut.Save()
    
    def _register_in_registry(self) -> None:
        """Register the application in the Windows registry"""
        const_log_ident = "Installer::_RegisterInRegistry"
        
        if not is_windows():
            return
        
        try:
            import winreg
            
            # Create uninstall key
            with winreg.CreateKey(
                winreg.HKEY_CURRENT_USER,
                Paths.UNINSTALL_KEY
            ) as key:
                winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, Paths.PROJECT_NAME)
                winreg.SetValueEx(key, "InstallLocation", 0, winreg.REG_SZ, str(self._install_location))
                winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ, 
                    f'"{sys.executable}" "{self._install_location}" --uninstall')
                winreg.SetValueEx(key, "DisplayIcon", 0, winreg.REG_SZ, 
                    f'"{sys.executable}",0')
                winreg.SetValueEx(key, "Publisher", 0, winreg.REG_SZ, Paths.PROJECT_OWNER)
                winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, "1.0.0")
            
            print(f"{const_log_ident}: Registered in registry")
            
        except ImportError:
            print(f"{const_log_ident}: winreg not available")
        except Exception as e:
            print(f"{const_log_ident}: Error registering in registry: {e}")
    
    def _save_settings(self) -> None:
        """Save default settings"""
        # Save empty settings to initialize the file
        App.settings.save()
        App.state.save()
        App.roblox_state.save()
    
    async def handle_upgrade(self) -> None:
        """Handle application upgrade"""
        const_log_ident = "Installer::HandleUpgrade"
        
        try:
            # Check for updates
            latest_release = await App.get_latest_release()
            
            if latest_release is None:
                print(f"{const_log_ident}: Could not get latest release")
                return
            
            current_version = "0.1.0"  # Will be replaced with actual version
            latest_version = latest_release.get('tag_name', '0.0.0')
            
            # Compare versions
            if self._compare_versions(current_version, latest_version) < 0:
                print(f"{const_log_ident}: New version available: {latest_version}")
                
                # Download and install update
                await self._download_and_install_update(latest_release)
            else:
                print(f"{const_log_ident}: Already up to date")
                
        except Exception as e:
            print(f"{const_log_ident}: Error handling upgrade: {e}")
    
    def _compare_versions(self, v1: str, v2: str) -> int:
        """Compare two version strings"""
        # Simple version comparison (major.minor.patch)
        v1_parts = v1.split('.')
        v2_parts = v2.split('.')
        
        # Pad with zeros to make equal length
        max_len = max(len(v1_parts), len(v2_parts))
        v1_parts.extend(['0'] * (max_len - len(v1_parts)))
        v2_parts.extend(['0'] * (max_len - len(v2_parts)))
        
        for i in range(max_len):
            try:
                v1_num = int(v1_parts[i])
                v2_num = int(v2_parts[i])
                
                if v1_num < v2_num:
                    return -1
                elif v1_num > v2_num:
                    return 1
            except ValueError:
                # If version part is not a number, compare as string
                if v1_parts[i] < v2_parts[i]:
                    return -1
                elif v1_parts[i] > v2_parts[i]:
                    return 1
        
        return 0
    
    async def _download_and_install_update(self, release: Dict[str, Any]) -> bool:
        """Download and install an update"""
        const_log_ident = "Installer::_DownloadAndInstallUpdate"
        
        try:
            # Find the appropriate asset for the current platform
            assets = release.get('assets', [])
            
            # For now, we'll just download all assets
            # In a real implementation, we'd find the right one for the platform
            
            # Create temp directory for downloads
            temp_dir = Paths.temp_updates
            temp_dir.mkdir(parents=True, exist_ok=True)
            
            # Download assets
            downloaded_files = []
            for asset in assets:
                asset_name = asset.get('name', '')
                download_url = asset.get('browser_download_url', '')
                
                if not download_url:
                    continue
                
                # Download the file
                file_path = temp_dir / asset_name
                
                print(f"{const_log_ident}: Downloading {asset_name}...")
                
                success = await self._download_file(download_url, file_path)
                if success:
                    downloaded_files.append(file_path)
                    print(f"{const_log_ident}: Downloaded {asset_name}")
                else:
                    print(f"{const_log_ident}: Failed to download {asset_name}")
            
            # Install the update
            if downloaded_files:
                print(f"{const_log_ident}: Installing update...")
                return await self._install_update(downloaded_files)
            
            return False
            
        except Exception as e:
            print(f"{const_log_ident}: Error downloading and installing update: {e}")
            return False
    
    async def _download_file(self, url: str, file_path: Path) -> bool:
        """Download a file from a URL"""
        try:
            # Use aiohttp for async download
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        content = await response.read()
                        file_path.write_bytes(content)
                        return True
            
            return False
            
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            return False
    
    async def _install_update(self, files: List[Path]) -> bool:
        """Install downloaded update files"""
        const_log_ident = "Installer::_InstallUpdate"
        
        try:
            # For now, just extract the first file (assuming it's a zip)
            if not files:
                return False
            
            zip_file = files[0]
            
            # Extract the zip file
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                for file_info in zip_ref.infolist():
                    # Extract to install location
                    file_info.filename = os.path.basename(file_info.filename)
                    zip_ref.extract(file_info, self._install_location)
            
            # Clean up temp files
            for file in files:
                file.unlink()
            
            print(f"{const_log_ident}: Update installed successfully")
            return True
            
        except Exception as e:
            print(f"{const_log_ident}: Error installing update: {e}")
            return False
    
    def uninstall(self) -> bool:
        """Uninstall the application"""
        const_log_ident = "Installer::Uninstall"
        
        try:
            # Get install location from registry
            install_location = self._get_install_location_from_registry()
            
            if not install_location:
                print(f"{const_log_ident}: Could not find install location")
                return False
            
            # Remove files
            if install_location.exists():
                shutil.rmtree(install_location)
                print(f"{const_log_ident}: Removed install location")
            
            # Remove shortcuts
            self._remove_shortcuts()
            
            # Remove registry entries
            self._remove_registry_entries()
            
            print(f"{const_log_ident}: Uninstallation completed")
            return True
            
        except Exception as e:
            print(f"{const_log_ident}: Error during uninstallation: {e}")
            return False
    
    def _get_install_location_from_registry(self) -> Optional[Path]:
        """Get the install location from the registry"""
        if not is_windows():
            return None
        
        try:
            import winreg
            
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                Paths.UNINSTALL_KEY
            ) as key:
                install_location = winreg.QueryValueEx(key, "InstallLocation")[0]
                if install_location:
                    return Path(install_location)
        except Exception:
            pass
        
        return None
    
    def _remove_shortcuts(self) -> None:
        """Remove desktop and start menu shortcuts"""
        const_log_ident = "Installer::_RemoveShortcuts"
        
        try:
            # Remove desktop shortcut
            desktop = Paths.get_desktop()
            shortcut_path = desktop / f"{Paths.PROJECT_NAME}.lnk"
            if shortcut_path.exists():
                shortcut_path.unlink()
            
            # Remove start menu shortcuts
            start_menu = Paths.get_start_menu()
            start_menu_path = start_menu / Paths.PROJECT_NAME
            if start_menu_path.exists():
                shutil.rmtree(start_menu_path)
            
            print(f"{const_log_ident}: Removed shortcuts")
            
        except Exception as e:
            print(f"{const_log_ident}: Error removing shortcuts: {e}")
    
    def _remove_registry_entries(self) -> None:
        """Remove registry entries"""
        const_log_ident = "Installer::_RemoveRegistryEntries"
        
        if not is_windows():
            return
        
        try:
            import winreg
            
            # Remove uninstall key
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, Paths.UNINSTALL_KEY)
            
            print(f"{const_log_ident}: Removed registry entries")
            
        except Exception as e:
            print(f"{const_log_ident}: Error removing registry entries: {e}")
