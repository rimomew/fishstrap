"""Utility functions and classes for PyFishstrap"""

import os
import sys
import json
import hashlib
import time
import platform
import subprocess
import urllib.parse
import webbrowser
from pathlib import Path
from typing import Optional, Any, Dict, List, Tuple
from datetime import datetime


def get_timestamp() -> str:
    """Get current timestamp in ISO format"""
    return datetime.utcnow().isoformat()


def md5_hash(data: str) -> str:
    """Calculate MD5 hash of a string"""
    return hashlib.md5(data.encode('utf-8')).hexdigest()


def md5_hash_file(file_path: Path) -> str:
    """Calculate MD5 hash of a file"""
    if not file_path.exists():
        return ""
    
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def read_json_file(file_path: Path) -> Optional[Dict[str, Any]]:
    """Read a JSON file and return its contents"""
    if not file_path.exists():
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading JSON file {file_path}: {e}")
        return None


def write_json_file(file_path: Path, data: Any, indent: int = 4) -> bool:
    """Write data to a JSON file"""
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        return True
    except (IOError, TypeError) as e:
        print(f"Error writing JSON file {file_path}: {e}")
        return False


def is_windows() -> bool:
    """Check if running on Windows"""
    return platform.system() == 'Windows'


def is_linux() -> bool:
    """Check if running on Linux"""
    return platform.system() == 'Linux'


def is_mac() -> bool:
    """Check if running on macOS"""
    return platform.system() == 'Darwin'


def get_os_version() -> Tuple[str, str, str]:
    """Get OS version information"""
    system = platform.system()
    release = platform.release()
    version = platform.version()
    return system, release, version


def open_url(url: str) -> bool:
    """Open a URL in the default browser"""
    try:
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"Error opening URL {url}: {e}")
        return False


def parse_roblox_url(url: str) -> Optional[Dict[str, str]]:
    """Parse a Roblox URL and extract relevant information"""
    try:
        parsed = urllib.parse.urlparse(url)
        
        # Handle roblox: and roblox-player: URIs
        if parsed.scheme.lower() in ['roblox', 'roblox-player']:
            result = {'scheme': parsed.scheme}
            
            # Parse query parameters
            query_params = urllib.parse.parse_qs(parsed.query)
            
            if 'placeId' in query_params:
                result['placeId'] = query_params['placeId'][0]
            if 'universeId' in query_params:
                result['universeId'] = query_params['universeId'][0]
            if 'gameId' in query_params:
                result['gameId'] = query_params['gameId'][0]
            if 'launchMode' in query_params:
                result['launchMode'] = query_params['launchMode'][0]
            if 'channel' in query_params:
                result['channel'] = query_params['channel'][0]
            
            return result
        
        # Handle http/https URLs
        if parsed.netloc.lower().endswith('.roblox.com'):
            result = {'scheme': parsed.scheme, 'netloc': parsed.netloc}
            
            # Extract path components
            path_parts = parsed.path.strip('/').split('/')
            
            if len(path_parts) >= 2 and path_parts[0] == 'games':
                result['gameId'] = path_parts[1]
            
            return result
        
        return None
    except Exception as e:
        print(f"Error parsing Roblox URL {url}: {e}")
        return None


def launch_process(executable: str, args: List[str] = None, cwd: Optional[str] = None) -> Optional[subprocess.Popen]:
    """Launch a process"""
    if args is None:
        args = []
    
    try:
        if is_windows():
            # On Windows, use shell=True to properly handle paths with spaces
            full_cmd = [executable] + args
            return subprocess.Popen(full_cmd, cwd=cwd, shell=True)
        else:
            # On Unix-like systems
            return subprocess.Popen([executable] + args, cwd=cwd)
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error launching process {executable}: {e}")
        return None


def find_roblox_executable(launch_mode: str) -> Optional[Path]:
    """Find the Roblox executable based on launch mode"""
    if not is_windows():
        return None  # Roblox is Windows-only
    
    from .paths import Paths
    
    # Check in the Roblox installation directory
    roblox_dir = Paths.roblox
    
    if launch_mode == "Player":
        # Try common executable names
        for name in ["RobloxPlayerBeta.exe", "RobloxPlayer.exe"]:
            exe_path = roblox_dir / name
            if exe_path.exists():
                return exe_path
    elif launch_mode == "Studio":
        for name in ["RobloxStudioBeta.exe", "RobloxStudio.exe"]:
            exe_path = roblox_dir / name
            if exe_path.exists():
                return exe_path
    
    # Check in Versions directory
    versions_dir = Paths.versions
    if versions_dir.exists():
        # Find the latest version directory
        version_dirs = sorted(versions_dir.iterdir(), key=lambda x: x.name, reverse=True)
        for version_dir in version_dirs:
            if launch_mode == "Player":
                exe_path = version_dir / "RobloxPlayerBeta.exe"
                if exe_path.exists():
                    return exe_path
            elif launch_mode == "Studio":
                exe_path = version_dir / "RobloxStudioBeta.exe"
                if exe_path.exists():
                    return exe_path
    
    return None


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def sanitize_filename(filename: str) -> str:
    """Sanitize a filename by removing invalid characters"""
    if is_windows():
        # Windows reserved characters
        invalid_chars = '<>:"|?*\\'
    else:
        # Unix-like systems
        invalid_chars = '/'
    
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    return filename.strip(' .')


def get_file_extension(file_path: Path) -> str:
    """Get the file extension from a path"""
    return file_path.suffix.lower()


def is_admin() -> bool:
    """Check if the current process has admin privileges"""
    if is_windows():
        import ctypes
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False
    elif is_linux() or is_mac():
        return os.geteuid() == 0
    return False


def get_user_agent() -> str:
    """Get the user agent string for HTTP requests"""
    from .paths import Paths
    from . import __version__
    
    system_info = f"{platform.system()}/{platform.release()}"
    python_version = f"Python/{platform.python_version()}"
    
    return f"{Paths.PROJECT_NAME}/{__version__} ({system_info}; {python_version})"
