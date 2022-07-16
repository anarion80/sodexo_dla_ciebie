"""Constants for Sodexo Dla Ciebie integration."""
# Base component constants
NAME = "Sodexo Dla Ciebie"
DOMAIN = "sodexo_dla_ciebie"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"
ATTRIBUTION = "Data provided by https://api4you.sodexo.pl"
ISSUE_URL = "https://github.com/anarion80/sodexo_dla_ciebie/issues"

# Icons
DEFAULT_ICON = "mdi:credit-card"

# Platforms
SENSOR = "sensor"
PLATFORM = "sensor"
PLATFORMS = [SENSOR]

# Defaults
DEFAULT_NAME = DOMAIN
DEFAULT_ACTIVE_ONLY = True
ACTIVE_ONLY = "active_only"

# URLs
API_URL = "https://api4you.sodexo.pl/api/card"
LOGIN_URL = "https://api4you.sodexo.pl/api/user/login"

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""

UNIT_OF_MEASUREMENT = "PLN"
