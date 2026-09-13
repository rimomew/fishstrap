"""Data models for PyFishstrap"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class GitHubRelease:
    """GitHub release model"""
    tag_name: str = ""
    name: str = ""
    body: str = ""
    published_at: str = ""
    assets: List[dict] = field(default_factory=list)


@dataclass
class GitHubReleaseAsset:
    """GitHub release asset model"""
    name: str = ""
    browser_download_url: str = ""
    size: int = 0
    download_count: int = 0


# RoValra API models
@dataclass
class RoValraServerLocation:
    """RoValra server location model"""
    server_id: str = ""
    region: str = ""
    country: str = ""
    city: str = ""
    latitude: float = 0.0
    longitude: float = 0.0


@dataclass
class RoValraServer:
    """RoValra server model"""
    server_id: str = ""
    name: str = ""
    location: Optional[RoValraServerLocation] = None
    players: int = 0
    capacity: int = 0
    ping: int = 0


@dataclass
class RoValraServers:
    """RoValra servers response model"""
    servers: List[RoValraServer] = field(default_factory=list)


@dataclass
class RoValraDatacenters:
    """RoValra datacenters model"""
    datacenters: List[str] = field(default_factory=list)


@dataclass
class RoValraGeolocation:
    """RoValra geolocation model"""
    ip: str = ""
    country: str = ""
    region: str = ""
    city: str = ""
    latitude: float = 0.0
    longitude: float = 0.0


# Roblox API models
@dataclass
class GameCreator:
    """Game creator model"""
    id: int = 0
    name: str = ""
    type: str = ""


@dataclass
class GetUserResponse:
    """Get user response model"""
    id: int = 0
    name: str = ""
    displayName: str = ""


@dataclass
class ThumbnailBatchResponse:
    """Thumbnail batch response model"""
    data: List[dict] = field(default_factory=list)


@dataclass
class ThumbnailResponse:
    """Thumbnail response model"""
    imageUrl: str = ""
    targetId: int = 0
    state: str = ""
    imageToken: str = ""


@dataclass
class ThumbnailRequest:
    """Thumbnail request model"""
    requestId: str = ""
    type: str = ""
    targetId: int = 0
    size: str = ""
    format: str = ""


@dataclass
class AuthenticatedUser:
    """Authenticated user model"""
    id: int = 0
    name: str = ""
    displayName: str = ""


@dataclass
class ClientVersion:
    """Client version model"""
    version: str = ""
    clientVersionUpload: datetime = datetime.min
    bootstrapperVersion: str = ""
    bootstrapperLastUpdated: datetime = datetime.min


@dataclass
class ClientFlagSettings:
    """Client flag settings model"""
    flags: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GameDetailResponse:
    """Game detail response model"""
    id: int = 0
    name: str = ""
    description: str = ""
    creator: Optional[GameCreator] = None
    universeId: int = 0
    rootPlaceId: int = 0
    created: datetime = datetime.min
    updated: datetime = datetime.min
    maxPlayers: int = 0
    playing: int = 0
    visits: int = 0
    isPlayable: bool = False


@dataclass
class UniverseIdResponse:
    """Universe ID response model"""
    universeId: int = 0


@dataclass
class ApiArrayResponse:
    """API array response model"""
    data: List[Any] = field(default_factory=list)


@dataclass
class UserChannel:
    """User channel model"""
    channel: str = ""
    name: str = ""


# Config models
@dataclass
class PackageMaps:
    """Package maps configuration"""
    maps: Dict[str, str] = field(default_factory=dict)


# Settings models
@dataclass
class Settings:
    """Application settings model"""
    locale: str = "en-us"
    theme: str = "System"
    bootstrapperStyle: str = "Classic"
    allowCookieAccess: bool = False
    staticDirectory: bool = False
    forceLocalData: bool = False
    selectedChannel: str = ""
    channelChangeMode: str = "Automatic"
    discordRPC: bool = False
    discordRPCStatusDisplay: str = "Both"
    lastVersionCheck: str = ""
    checkForUpdates: bool = True
    customBootstrapperEnabled: bool = False
    customBootstrapperPath: str = ""
    customFontEnabled: bool = False
    customFontPath: str = ""
    cursorType: str = "Default"
    emojiType: str = "Roblox"
    enableLogging: bool = True
    logLevel: str = "Info"


@dataclass
class State:
    """Application state model"""
    versionGuid: str = ""
    studioVersionGuid: str = ""
    lastLaunchTime: str = ""
    totalLaunches: int = 0
    playerLaunches: int = 0
    studioLaunches: int = 0
    lastSettingsTab: str = ""


@dataclass
class RobloxState:
    """Roblox state model"""
    class Studio:
        versionGuid: str = ""
        lastLaunchTime: str = ""
        
    class Player:
        versionGuid: str = ""
        lastLaunchTime: str = ""
    
    studio: Studio = field(default_factory=Studio)
    player: Player = field(default_factory=Player)


@dataclass
class RemoteDataBase:
    """Remote data base model"""
    version: str = ""
    lastUpdated: str = ""
    messages: List[str] = field(default_factory=list)
    channels: List[dict] = field(default_factory=list)
    datacenters: List[str] = field(default_factory=list)
    

@dataclass
class GameJoinData:
    """Game join data model"""
    placeId: int = 0
    universeId: int = 0
    gameName: str = ""
    serverId: str = ""
    joinType: str = "Normal"
    launchArgs: str = ""


@dataclass
class PackageManifest:
    """Package manifest model"""
    version: str = ""
    guid: str = ""
    baseUrl: str = ""
    files: List[dict] = field(default_factory=list)
