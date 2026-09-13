"""
PyFishstrap - A Python reimplementation of Fishstrap, a custom bootstrapper for Roblox.

This project aims to replicate the functionality of Fishstrap (https://github.com/rimomew/fishstrap)
in Python, providing a cross-platform alternative for managing Roblox launches.

Features:
- Roblox Player and Studio launching
- FastFlags editor
- Global Basic Settings editor
- Server information from RoValra API
- Game join functionality
- Settings and state management
"""

__version__ = "0.1.0"
__author__ = "PyFishstrap"
__license__ = "MIT"

from .app import App
from .enums import LaunchMode, ErrorCode, NextAction
from .managers import SettingsManager, StateManager, FastFlagManager
from .paths import Paths
