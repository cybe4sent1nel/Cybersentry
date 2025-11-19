"""
A library to build Bug Bounty-level grade Cybersecurity AIs (CYBERSENTRYs).
"""

def is_pentestperf_available():
    """
    Check if pentestperf is available
    """
    try:
        from pentestperf.ctf import CTF  # pylint: disable=import-error,import-outside-toplevel,unused-import  # noqa: E501,F401
    except ImportError:
        return False
    return True


def is_cybersentryextensions_report_available():
    """
    Check if cybersentryextensions report is available
    """
    try:
        from cybersentryextensions.report.common import get_base_instructions  # pylint: disable=import-error,import-outside-toplevel,unused-import  # noqa: E501,F401
    except ImportError:
        return False
    return True


def is_cybersentryextensions_memory_available():
    """
    Check if cybersentryextensions memory is available
    """
    try:
        from cybersentryextensions.memory import is_memory_installed  # pylint: disable=import-error,import-outside-toplevel,unused-import  # noqa: E501,F401
    except ImportError:
        return False
    return True


def is_cybersentryextensions_platform_available():
    """
    Check if cybersentryextensions-platform is available
    """
    try:
        from cybersentryextensions.platform.base import platform_manager  # pylint: disable=import-error,import-outside-toplevel,unused-import  # noqa: E501,F401
    except ImportError:
        return False
    return True
