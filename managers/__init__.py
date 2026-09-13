"""Manager classes for PyFishstrap"""

import json
import copy
from pathlib import Path
from typing import Optional, Any, Dict, List, Type, TypeVar, Generic
from abc import ABC, abstractmethod

from ..models import Settings, State, RobloxState, RemoteDataBase, GameJoinData
from ..utils import read_json_file, write_json_file, md5_hash_file
from ..paths import Paths


T = TypeVar('T')


class JsonManager(ABC, Generic[T]):
    """Base class for JSON-based managers"""
    
    def __init__(self, data_class: Type[T]):
        self.data_class = data_class
        self._original: T = data_class()
        self._current: T = data_class()
        self._last_file_hash: Optional[str] = None
        self._loaded: bool = False
        self._file_location: Path = Path()
    
    @property
    def class_name(self) -> str:
        """Get the class name"""
        return self.__class__.__name__
    
    @property
    def original(self) -> T:
        """Get the original data"""
        return self._original
    
    @property
    def current(self) -> T:
        """Get the current data"""
        return self._current
    
    @property
    def prop(self) -> T:
        """Get the current data (alias for current)"""
        return self._current
    
    @property
    def loaded(self) -> bool:
        """Check if data has been loaded"""
        return self._loaded
    
    @property
    @abstractmethod
    def file_location(self) -> Path:
        """Get the file location for this manager"""
        pass
    
    def load(self, alert_failure: bool = True) -> bool:
        """Load data from file"""
        try:
            data = read_json_file(self.file_location)
            if data is None:
                # File doesn't exist, create default
                self._current = self.data_class()
                self._original = copy.deepcopy(self._current)
                self._loaded = True
                self._last_file_hash = md5_hash_file(self.file_location)
                return True
            
            # Convert dict to dataclass
            self._current = self._from_dict(data)
            self._original = copy.deepcopy(self._current)
            self._loaded = True
            self._last_file_hash = md5_hash_file(self.file_location)
            return True
        except Exception as e:
            print(f"Error loading {self.class_name}: {e}")
            if alert_failure:
                # Show error message (will be implemented in UI)
                pass
            # Create backup
            backup_path = Path(str(self.file_location) + ".bak")
            try:
                import shutil
                shutil.copy2(self.file_location, backup_path)
            except Exception as backup_e:
                print(f"Error creating backup: {backup_e}")
            
            # Save default
            self.save()
            return False
    
    def save(self) -> bool:
        """Save data to file"""
        try:
            self.file_location.parent.mkdir(parents=True, exist_ok=True)
            data_dict = self._to_dict(self._current)
            success = write_json_file(self.file_location, data_dict)
            if success:
                self._last_file_hash = md5_hash_file(self.file_location)
                self._original = copy.deepcopy(self._current)
            return success
        except Exception as e:
            print(f"Error saving {self.class_name}: {e}")
            return False
    
    def has_file_changed(self) -> bool:
        """Check if the file has changed since last load"""
        if not self._last_file_hash:
            return False
        return self._last_file_hash != md5_hash_file(self.file_location)
    
    def _from_dict(self, data: Dict[str, Any]) -> T:
        """Convert dictionary to dataclass instance"""
        # This is a simple implementation; may need to be overridden for complex cases
        return self.data_class(**data)
    
    def _to_dict(self, obj: T) -> Dict[str, Any]:
        """Convert dataclass instance to dictionary"""
        return obj.__dict__


class SettingsManager(JsonManager[Settings]):
    """Manager for application settings"""
    
    def __init__(self):
        super().__init__(Settings)
    
    @property
    def file_location(self) -> Path:
        """Get the settings file location"""
        return Paths.base / "Settings.json"
    
    def load(self, alert_failure: bool = True) -> bool:
        """Load settings from file"""
        result = super().load(alert_failure)
        # Apply any migrations or defaults
        self._apply_defaults()
        return result
    
    def _apply_defaults(self):
        """Apply default values for any missing settings"""
        # This would be expanded with actual default values
        pass


class StateManager(JsonManager[State]):
    """Manager for application state"""
    
    def __init__(self):
        super().__init__(State)
    
    @property
    def file_location(self) -> Path:
        """Get the state file location"""
        return Paths.base / "State.json"


class RobloxStateManager(JsonManager[RobloxState]):
    """Manager for Roblox state"""
    
    def __init__(self):
        super().__init__(RobloxState)
    
    @property
    def file_location(self) -> Path:
        """Get the Roblox state file location"""
        return Paths.base / "RobloxState.json"


class FastFlagManager(JsonManager[Dict[str, Any]]):
    """Manager for FastFlags (ClientAppSettings.json)"""
    
    def __init__(self):
        super().__init__(dict)
        self._preset_flags: Dict[str, str] = {
            # Rendering presets
            "Rendering.ManualFullscreen": "FFlagHandleAltEnterFullscreenManually",
            "Rendering.DisableScaling": "DFFlagDisableDPIScale",
            "Rendering.MSAA": "FIntDebugForceMSAASamples",
            "Rendering.FRMQualityOverride": "DFIntDebugFRMQualityLevelOverride",
            
            # Rendering engines
            "Rendering.Mode.D3D11": "FFlagDebugGraphicsPreferD3D11",
            "Rendering.Mode.Vulkan": "FFlagDebugGraphicsPreferVulkan",
            
            # Geometry
            "Geometry.MeshLOD.Static": "DFIntCSGLevelOfDetailSwitchingDistanceStatic",
            "Geometry.MeshLOD.L0": "DFIntCSGLevelOfDetailSwitchingDistance",
            "Geometry.MeshLOD.L12": "DFIntCSGLevelOfDetailSwitchingDistanceL12",
            "Geometry.MeshLOD.L23": "DFIntCSGLevelOfDetailSwitchingDistanceL23",
            "Geometry.MeshLOD.L34": "DFIntCSGLevelOfDetailSwitchingDistanceL34",
        }
        
        self._rendering_modes: Dict[str, str] = {
            "Default": "None",
            "Vulkan": "Vulkan",
            "D3D11": "D3D11",
        }
        
        self._msaa_modes: Dict[str, Optional[str]] = {
            "Default": None,
            "x1": "1",
            "x2": "2",
            "x4": "4",
        }
    
    @property
    def file_location(self) -> Path:
        """Get the FastFlags file location"""
        return Paths.modifications / "ClientSettings" / "ClientAppSettings.json"
    
    @property
    def profiles_location(self) -> Path:
        """Get the profiles directory location"""
        return Paths.base / "Profiles"
    
    @property
    def preset_flags(self) -> Dict[str, str]:
        """Get the preset flags mapping"""
        return self._preset_flags
    
    @property
    def rendering_modes(self) -> Dict[str, str]:
        """Get the rendering modes mapping"""
        return self._rendering_modes
    
    @property
    def msaa_modes(self) -> Dict[str, Optional[str]]:
        """Get the MSAA modes mapping"""
        return self._msaa_modes
    
    def set_value(self, key: str, value: Any) -> None:
        """Set a FastFlag value"""
        if value is None:
            # Remove the key
            if key in self._current:
                del self._current[key]
        else:
            # Set the value as string
            self._current[key] = str(value)
    
    def get_value(self, key: str) -> Optional[str]:
        """Get a FastFlag value"""
        return self._current.get(key)
    
    def set_preset(self, prefix: str, value: Any) -> None:
        """Set all flags with a specific prefix"""
        for key, flag_name in self._preset_flags.items():
            if key.startswith(prefix):
                self.set_value(flag_name, value)
    
    def set_preset_enum(self, prefix: str, target: str, value: Any) -> None:
        """Set preset enum value"""
        for key, flag_name in self._preset_flags.items():
            if key.startswith(prefix) and (not target or key.endswith(target)):
                self.set_value(flag_name, value)
    
    def has_changed(self) -> bool:
        """Check if FastFlags have changed"""
        return self._current != self._original
    
    def load(self, alert_failure: bool = True) -> bool:
        """Load FastFlags from file"""
        # Ensure directory exists
        self.file_location.parent.mkdir(parents=True, exist_ok=True)
        
        # If file doesn't exist, create default
        if not self.file_location.exists():
            self._current = {}
            self._original = {}
            self._loaded = True
            return True
        
        return super().load(alert_failure)
    
    def _from_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert dictionary to dict (no conversion needed)"""
        return data
    
    def _to_dict(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Convert dict to dict (no conversion needed)"""
        return obj


class RemoteDataManager(JsonManager[RemoteDataBase]):
    """Manager for remote data from Fishstrap API"""
    
    def __init__(self):
        super().__init__(RemoteDataBase)
        self._loaded_state = "Unknown"  # Unknown, Successful, Failed
        self._subscribers: List[Any] = []
    
    @property
    def file_location(self) -> Path:
        """Get the remote data file location"""
        return Paths.base / "Data.json"
    
    @property
    def loaded_state(self) -> str:
        """Get the loading state"""
        return self._loaded_state
    
    def subscribe(self, handler: Any) -> None:
        """Subscribe to data loaded event"""
        if self._loaded_state == "Unknown":
            self._subscribers.append(handler)
        else:
            # Data already loaded, call handler immediately
            handler(self, None)
    
    async def wait_until_data_fetched(self, timeout: int = 3000, delay: int = 100) -> bool:
        """Wait until data is fetched"""
        import asyncio
        
        tries = 0
        max_tries = timeout // delay
        
        while self._loaded_state == "Unknown" and tries < max_tries:
            await asyncio.sleep(delay / 1000)
            tries += 1
        
        return self._loaded_state == "Successful"
    
    async def load_data(self) -> None:
        """Load remote data from API"""
        from ..api import HttpClient
        from ..paths import Paths
        from .. import App
        
        if App.settings.prop.force_local_data:
            # Load from local file
            self.load(False)
            self._loaded_state = "Successful"
        else:
            try:
                # Fetch from remote
                response = await HttpClient.get_json(Paths.PROJECT_REMOTE_DATA_LINK)
                if response:
                    self._current = self._from_dict(response)
                    self._original = copy.deepcopy(self._current)
                    self._loaded_state = "Successful"
                    self._last_file_hash = md5_hash_file(self.file_location)
                    self.save()
                else:
                    # Fallback to local
                    self.load(False)
                    self._loaded_state = "Failed"
            except Exception as e:
                print(f"Error loading remote data: {e}")
                # Fallback to local
                self.load(False)
                self._loaded_state = "Failed"
        
        # Notify subscribers
        for handler in self._subscribers:
            handler(self, None)


class GameJoinManager:
    """Manager for game join data"""
    
    def __init__(self):
        self._join_data: GameJoinData = GameJoinData()
    
    @property
    def join_data(self) -> GameJoinData:
        """Get the current join data"""
        return self._join_data
    
    def set_place_id(self, place_id: int) -> None:
        """Set the place ID to join"""
        self._join_data.placeId = place_id
    
    def set_universe_id(self, universe_id: int) -> None:
        """Set the universe ID to join"""
        self._join_data.universeId = universe_id
    
    def set_server_id(self, server_id: str) -> None:
        """Set the server ID to join"""
        self._join_data.serverId = server_id
    
    def set_join_type(self, join_type: str) -> None:
        """Set the join type"""
        self._join_data.joinType = join_type
    
    def set_launch_args(self, launch_args: str) -> None:
        """Set the launch arguments"""
        self._join_data.launchArgs = launch_args
    
    def clear(self) -> None:
        """Clear the join data"""
        self._join_data = GameJoinData()


# Global manager instances
settings = SettingsManager()
state = StateManager()
roblox_state = RobloxStateManager()
fast_flags = FastFlagManager()
remote_data = RemoteDataManager()
game_join = GameJoinManager()
