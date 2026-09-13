#!/usr/bin/env python3
"""
PyFishstrap - Main entry point

This script serves as the main entry point for PyFishstrap, a Python reimplementation
of Fishstrap (https://github.com/rimomew/fishstrap).

Usage:
    python main.py [arguments]

Arguments:
    --menu, --preferences, --settings    Open settings menu
    --watcher                        Open the watcher
    --backgroundupdater              Open background updater
    --quiet                         Run in quiet mode (no UI)
    --uninstall                     Uninstall the application
    --nolaunch                      Don't launch Roblox after bootstrapping
    --testmode                      Run in test mode
    --nogpu                         Disable GPU acceleration
    --upgrade                       Force upgrade check
    --player                        Launch Roblox Player
    --studio                        Launch Roblox Studio
    --version=VALUE                 Specify Roblox version
    --channel=VALUE                 Specify Roblox channel
    --force                         Force reinstall
    --bloxshade                     Open Bloxshade configuration

Roblox URIs:
    roblox:placeId=123456789        Launch a specific place
    roblox-player:universeId=123   Launch a specific universe
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path for imports
script_dir = str(Path(__file__).parent)
sys.path.insert(0, script_dir)

# Set the package name for relative imports
__package__ = 'pyfishstrap'

from pyfishstrap.app import App


def run():
    """Run PyFishstrap"""
    try:
        # Initialize the application
        App.initialize()
        
        # Check if we should run with UI or console mode
        # UI mode is enabled by default unless --quiet flag is set
        from pyfishstrap.launch_settings import get_launch_settings
        launch_settings = get_launch_settings()
        
        if launch_settings.quiet_flag.active:
            # Console mode
            App.run()
        else:
            # UI mode - launch PyQt application
            try:
                run_ui()
            except ImportError as e:
                print(f"UI mode not available: {e}")
                print("Falling back to console mode...")
                App.run()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def run_ui():
    """Run PyFishstrap with PyQt UI"""
    # Initialize frontend
    from pyfishstrap.ui.frontend import frontend
    frontend.initialize()
    
    # Run the PyQt application
    from pyfishstrap.ui import run_application
    run_application()


if __name__ == "__main__":
    run()
