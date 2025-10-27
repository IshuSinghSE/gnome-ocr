"""
Desktop Integration Module

Handles GNOME desktop interactions: screenshots, notifications, and clipboard.
"""

import subprocess
import pyperclip
from typing import Optional, Tuple


def capture_screenshot(save_path: str) -> Tuple[bool, Optional[str]]:
    """
    Captures a screenshot using available screenshot tools with area selection.
    Tries multiple tools in order: gnome-screenshot, flameshot, spectacle, scrot.
    
    Args:
        save_path: Path where the screenshot should be saved
        
    Returns:
        Tuple of (success: bool, error_message: Optional[str])
    """
    # Try gnome-screenshot first
    try:
        result = subprocess.run(
            ['gnome-screenshot', '-a', '-f', save_path],
            check=True,
            capture_output=True,
            timeout=60
        )
        return (True, None)
    except FileNotFoundError:
        pass  # Try next tool
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            return (False, "Screenshot cancelled by user")
        return (False, f"gnome-screenshot failed: {e.stderr.decode() if e.stderr else 'unknown error'}")
    except subprocess.TimeoutExpired:
        return (False, "Screenshot capture timed out")
    
    # Try flameshot
    try:
        result = subprocess.run(
            ['flameshot', 'gui', '-p', save_path],
            check=True,
            capture_output=True,
            timeout=60
        )
        return (True, None)
    except FileNotFoundError:
        pass  # Try next tool
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            return (False, "Screenshot cancelled by user")
    except subprocess.TimeoutExpired:
        return (False, "Screenshot capture timed out")
    
    # Try spectacle (KDE)
    try:
        result = subprocess.run(
            ['spectacle', '-r', '-b', '-n', '-o', save_path],
            check=True,
            capture_output=True,
            timeout=60
        )
        return (True, None)
    except FileNotFoundError:
        pass  # Try next tool
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            return (False, "Screenshot cancelled by user")
    except subprocess.TimeoutExpired:
        return (False, "Screenshot capture timed out")
    
    # No screenshot tool found
    return (False, "No screenshot tool found. Please install: gnome-screenshot, flameshot, or spectacle")


def send_notification(title: str, message: str, urgency: str = "normal") -> None:
    """
    Sends a desktop notification using notify-send.
    
    Args:
        title: Notification title
        message: Notification message body
        urgency: Notification urgency level (low, normal, critical)
    """
    try:
        subprocess.run(
            ['notify-send', '-u', urgency, title, message],
            check=False,  # Don't raise on error
            timeout=5
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        # Silently fail if notify-send is not available
        pass


def copy_to_clipboard(text: str) -> bool:
    """
    Copies text to the system clipboard.
    
    Args:
        text: Text to copy
        
    Returns:
        True if successful, False otherwise
    """
    try:
        pyperclip.copy(text)
        return True
    except Exception:
        return False
