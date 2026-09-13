"""Enums for PyFishstrap"""

from enum import Enum, auto

class LaunchMode(Enum):
    """Launch mode for Roblox"""
    NONE = auto()
    UNKNOWN = auto()
    PLAYER = auto()
    STUDIO = auto()
    STUDIO_AUTH = auto()


class ErrorCode(Enum):
    """Error codes for termination"""
    ERROR_SUCCESS = 0
    ERROR_INSTALL_FAILURE = 1
    ERROR_INVALID_FUNCTION = 2
    ERROR_INSTALL_USEREXIT = 3


class NextAction(Enum):
    """Next action to perform"""
    NONE = auto()
    LAUNCH_SETTINGS = auto()
    LAUNCH_ROBLOX = auto()
    LAUNCH_ROBLOX_STUDIO = auto()
    CLOSE = auto()


class GenericTriState(Enum):
    """Tri-state enum for loading states"""
    UNKNOWN = auto()
    SUCCESSFUL = auto()
    FAILED = auto()


class Theme(Enum):
    """UI theme"""
    SYSTEM = auto()
    LIGHT = auto()
    DARK = auto()


class BootstrapperStyle(Enum):
    """Bootstrapper dialog style"""
    CLASSIC = auto()
    FLUENT = auto()
    TERMINAL = auto()
    BYFRON = auto()
    TWENTY_FIVE = auto()
    LEGACY_2008 = auto()
    LEGACY_2011 = auto()
    VISTA = auto()
    CUSTOM = auto()


class ChannelChangeMode(Enum):
    """Channel change mode"""
    AUTOMATIC = auto()
    MANUAL = auto()


class CleanerOptions(Enum):
    """Cleaner options"""
    LOGS = auto()
    CACHE = auto()
    TEMP = auto()
    ALL = auto()


class CookieState(Enum):
    """Cookie state"""
    DISABLED = auto()
    ENABLED = auto()
    PENDING = auto()


class CursorType(Enum):
    """Cursor type"""
    DEFAULT = auto()
    FROM_2006 = auto()
    FROM_2013 = auto()


class EmojiType(Enum):
    """Emoji type"""
    ROBLOX = auto()
    DISCORD = auto()
    TWITTER = auto()


class ElementVisibility(Enum):
    """UI element visibility"""
    VISIBLE = auto()
    HIDDEN = auto()
    COLLAPSED = auto()


class ServerType(Enum):
    """Server type"""
    STANDARD = auto()
    PRIVATE = auto()
    RESERVED = auto()


class ServerSessionJoinType(Enum):
    """Server session join type"""
    NORMAL = auto()
    PARTY = auto()
    PRIVATE_SERVER = auto()


class GameJoinType(Enum):
    """Game join type"""
    PLACE_ID = auto()
    GAME_LINK = auto()
    UNIVERSE_ID = auto()


class VersionComparison(Enum):
    """Version comparison result"""
    LESS = auto()
    EQUAL = auto()
    GREATER = auto()


class WebEnvironment(Enum):
    """Web environment"""
    PRODUCTION = auto()
    STAGING = auto()
    DEVELOPMENT = auto()


class DiscordRPCStatusDisplay(Enum):
    """Discord RPC status display"""
    NONE = auto()
    GAME_NAME = auto()
    UNIVERSE_NAME = auto()
    BOTH = auto()
