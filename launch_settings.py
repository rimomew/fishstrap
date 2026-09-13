"""Launch settings and argument parsing for PyFishstrap"""

import re
import sys
from typing import List, Dict, Optional
from dataclasses import dataclass, field

from .enums import LaunchMode
from .paths import Paths


@dataclass
class LaunchFlag:
    """Represents a launch flag"""
    identifiers: str
    active: bool = False
    
    def __post_init__(self):
        """Parse identifiers into a list"""
        self.identifiers_list = self.identifiers.split(',')
    
    def check(self, args: List[str]) -> bool:
        """Check if any of the identifiers are in the arguments"""
        for identifier in self.identifiers_list:
            if identifier in args:
                self.active = True
                return True
            # Check for flag with value (e.g., --flag=value)
            for arg in args:
                if arg.startswith(f"--{identifier}=") or arg.startswith(f"-{identifier}="):
                    self.active = True
                    return True
        self.active = False
        return False


class LaunchSettings:
    """Manages launch settings and command-line arguments"""
    
    def __init__(self, args: Optional[List[str]] = None):
        """Initialize launch settings with command-line arguments"""
        if args is None:
            args = sys.argv[1:]  # Skip the script name
        
        self.args = args
        self._roblox_launch_mode = LaunchMode.NONE
        self._roblox_launch_args = ""
        
        # Initialize flags
        self._flags: Dict[str, LaunchFlag] = {
            'menu': LaunchFlag("preferences,menu,settings"),
            'watcher': LaunchFlag("watcher"),
            'backgroundupdater': LaunchFlag("backgroundupdater"),
            'quiet': LaunchFlag("quiet"),
            'uninstall': LaunchFlag("uninstall"),
            'nolaunch': LaunchFlag("nolaunch"),
            'testmode': LaunchFlag("testmode"),
            'nogpu': LaunchFlag("nogpu"),
            'upgrade': LaunchFlag("upgrade"),
            'player': LaunchFlag("player"),
            'studio': LaunchFlag("studio"),
            'version': LaunchFlag("version"),
            'channel': LaunchFlag("channel"),
            'force': LaunchFlag("force"),
            'bloxshade': LaunchFlag("bloxshade"),
        }
        
        # Parse arguments
        self._parse_arguments()
    
    @property
    def menu_flag(self) -> LaunchFlag:
        """Menu flag (preferences, menu, settings)"""
        return self._flags['menu']
    
    @property
    def watcher_flag(self) -> LaunchFlag:
        """Watcher flag"""
        return self._flags['watcher']
    
    @property
    def background_updater_flag(self) -> LaunchFlag:
        """Background updater flag"""
        return self._flags['backgroundupdater']
    
    @property
    def quiet_flag(self) -> LaunchFlag:
        """Quiet flag"""
        return self._flags['quiet']
    
    @property
    def uninstall_flag(self) -> LaunchFlag:
        """Uninstall flag"""
        return self._flags['uninstall']
    
    @property
    def no_launch_flag(self) -> LaunchFlag:
        """No launch flag"""
        return self._flags['nolaunch']
    
    @property
    def test_mode_flag(self) -> LaunchFlag:
        """Test mode flag"""
        return self._flags['testmode']
    
    @property
    def no_gpu_flag(self) -> LaunchFlag:
        """No GPU flag"""
        return self._flags['nogpu']
    
    @property
    def upgrade_flag(self) -> LaunchFlag:
        """Upgrade flag"""
        return self._flags['upgrade']
    
    @property
    def player_flag(self) -> LaunchFlag:
        """Player flag"""
        return self._flags['player']
    
    @property
    def studio_flag(self) -> LaunchFlag:
        """Studio flag"""
        return self._flags['studio']
    
    @property
    def version_flag(self) -> LaunchFlag:
        """Version flag"""
        return self._flags['version']
    
    @property
    def channel_flag(self) -> LaunchFlag:
        """Channel flag"""
        return self._flags['channel']
    
    @property
    def force_flag(self) -> LaunchFlag:
        """Force flag"""
        return self._flags['force']
    
    @property
    def bloxshade_flag(self) -> LaunchFlag:
        """Bloxshade flag"""
        return self._flags['bloxshade']
    
    @property
    def bypass_update_check(self) -> bool:
        """Whether to bypass update check"""
        # In debug mode, always bypass
        # For now, bypass if uninstall or watcher flag is active
        return self.uninstall_flag.active or self.watcher_flag.active
    
    @property
    def roblox_launch_mode(self) -> LaunchMode:
        """Get the Roblox launch mode"""
        return self._roblox_launch_mode
    
    @property
    def roblox_launch_args(self) -> str:
        """Get the Roblox launch arguments"""
        return self._roblox_launch_args
    
    def _parse_arguments(self) -> None:
        """Parse command-line arguments"""
        # Check all flags
        for flag in self._flags.values():
            flag.check(self.args)
        
        # Infer Roblox launch URIs
        if len(self.args) >= 1:
            arg = self.args[0]
            
            # Check for roblox: or roblox-player: URIs
            if arg.lower().startswith("roblox:") or arg.lower().startswith("roblox-player:"):
                self._roblox_launch_mode = LaunchMode.PLAYER
                self._roblox_launch_args = arg
                return
            
            # Check for version- prefix (Roblox version directories)
            if arg.lower().startswith("version-"):
                self._roblox_launch_mode = LaunchMode.UNKNOWN
                self._roblox_launch_args = arg
                return
        
        # Check for explicit player/studio flags
        if self.player_flag.active:
            self._roblox_launch_mode = LaunchMode.PLAYER
        elif self.studio_flag.active:
            self._roblox_launch_mode = LaunchMode.STUDIO
        
        # Extract additional information from flags
        self._extract_flag_values()
    
    def _extract_flag_values(self) -> None:
        """Extract values from flags that have them"""
        for i, arg in enumerate(self.args):
            # Check for --version= or -version=
            if arg.startswith("--version=") or arg.startswith("-version="):
                self._roblox_launch_args = arg.split('=', 1)[1]
            
            # Check for --channel= or -channel=
            if arg.startswith("--channel=") or arg.startswith("-channel="):
                channel = arg.split('=', 1)[1]
                # Store channel in settings or state
                
            # Check for placeId, universeId, etc.
            if 'placeId=' in arg:
                place_id = self._extract_value(arg, 'placeId')
                if place_id:
                    # Store in game join data
                    pass
            
            if 'universeId=' in arg:
                universe_id = self._extract_value(arg, 'universeId')
                if universe_id:
                    # Store in game join data
                    pass
    
    def _extract_value(self, arg: str, key: str) -> Optional[str]:
        """Extract a value from a command-line argument"""
        # Handle --key=value
        if arg.startswith(f"--{key}="):
            return arg[len(f"--{key}="):]
        # Handle -key=value
        if arg.startswith(f"-{key}="):
            return arg[len(f"-{key}="):]
        # Handle key=value
        if f"{key}=" in arg:
            parts = arg.split(f"{key}=", 1)
            if len(parts) > 1:
                return parts[1]
        return None
    
    def get_flag_value(self, flag_name: str) -> Optional[str]:
        """Get the value of a specific flag"""
        for arg in self.args:
            if arg.startswith(f"--{flag_name}="):
                return arg[len(f"--{flag_name}="):]
            if arg.startswith(f"-{flag_name}="):
                return arg[len(f"-{flag_name}="):]
        return None
    
    def has_channel(self) -> bool:
        """Check if a channel was specified"""
        return self.channel_flag.active or self.get_flag_value('channel') is not None
    
    def get_channel(self) -> Optional[str]:
        """Get the specified channel"""
        return self.get_flag_value('channel')
    
    def has_version(self) -> bool:
        """Check if a version was specified"""
        return self.version_flag.active or self.get_flag_value('version') is not None
    
    def get_version(self) -> Optional[str]:
        """Get the specified version"""
        return self.get_flag_value('version')


# Global launch settings instance
launch_settings = None


def get_launch_settings() -> LaunchSettings:
    """Get the global launch settings instance"""
    global launch_settings
    if launch_settings is None:
        launch_settings = LaunchSettings()
    return launch_settings


def reset_launch_settings() -> None:
    """Reset the global launch settings instance"""
    global launch_settings
    launch_settings = None
