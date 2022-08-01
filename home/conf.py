import logging
from pathlib import Path
PRJ_PATH = Path(__file__).parent


COUNTRY = 'Hong kong'
# COUNTRY = 'south africa'
# COUNTRY = 'indonesia'
# COUNTRY = 'macau'
# COUNTRY = 'vietnam'
# COUNTRY = 'philippines'
# COUNTRY = 'argentina'


WAIT_TIME = 10
CYBERGHOSTVPN_USERNAME = 'salman@noborderz.com'
CYBERGHOSTVPN_PASSWORD = 'Surviral#123'
OUTPUTS_DIR_NAME = 'outputs'
OUTPUTS_DIR = PRJ_PATH / OUTPUTS_DIR_NAME
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)  # create it if it doesn't exist
PACKAGES_DIR_NAME = 'apk'
# tasks
TASKS_DIR_NAME = 'tasks'
TASKS_DIR = PRJ_PATH / TASKS_DIR_NAME
TASKS_DIR.mkdir(parents=True, exist_ok=True) 
PACKAGES_DIR = PRJ_PATH / PACKAGES_DIR_NAME
CYBERGHOSTVPN_APK = PACKAGES_DIR / 'cyberghost.apk'
AVD_DEVICES = [
               "pixel", "pixel_2", "pixel_2_xl", "pixel_3", "pixel_3_xl",
               "pixel_3a", "pixel_3a_xl", "pixel_4", "pixel_4_xl", "pixel_4a",
               "pixel_5"
               ]
AVD_PACKAGES = ["system-images;android-28;default;x86",
                "system-images;android-28;default;x86_64",
                "system-images;android-29;default;x86",
                "system-images;android-29;default;x86_64",
                "system-images;android-30;default;x86_64",

                # cause some errors of twitter: (errors: timestamp out of bounds, code:135)
                #  "system-images;android-31;default;x86_64",
                ]
# appium
APPIUM_SERVER_HOST = '127.0.0.1'
APPIUM_SERVER_PORT = 4724
APPIUM_SERVER_PORTS = list(range(APPIUM_SERVER_PORT, APPIUM_SERVER_PORT + 100))
#  SYSTEM_PORTS = list(range(8200, 8300))
SYSTEM_PORTS = list(range(8200, 8328))
# adb
ADB_SERVER_HOST = '127.0.0.1'
ADB_SERVER_PORT = 5037
ADB_CONSOLE_PORTS = list(range(5554, 5682, 2))
LOG_DIR = 'logs'
PRJ_PATH = Path(__file__).parent
LOG_DIR_PATH = PRJ_PATH / 'logs'
LOG_DIR_PATH.mkdir(parents=True, exist_ok=True)  # create it if it doesn't exist
LOG_LEVEL = logging.DEBUG
LOG_IN_ONE_FILE = True


CYBERGHOSTVPN_SERVERS = {
    'Albania': [],
    'Algeria': [],
    'Andorra': [],
    'Argentina': [],
    'Armenia': [],
    'Australia': ['Melbourne', 'Sydney'],
    'Austria': [],
    'Bahamas': [],
    'Bangladesh': [],
    'Belarus': [],
    'Belgium': [],
    'Bosnia & Herzegovina': [],
    'Brazil': [],
    'Bulgaria': [],
    'Cambodia': [],
    'Canada': ['Montreal', 'Toronto', 'Vancouver'],
    'Chile': [],
    'China': [],
    'Colombia': [],
    'Costa Rica': [],
    'Croatia': [],
    'Cyprus': [],
    'Czechia': [],
    'Denmark': [],
    'Egypt': [],
    'Estonia': [],
    'Finland': [],
    'France': ['Paris', 'Strasbourg'],
    'Georgia': [],
    'Germany': ['Berlin', 'Dusseldorf', 'Frankfurt'],
    'Greece': [],
    'Greenland': [],
    'Hong Kong': [],
    'Hungary': [],
    'Iceland': [],
    'India': [],
    'Indonesia': [],
    'Iran': [],
    'Ireland': [],
    'Isle of Man': [],
    'Israel': [],
    'Italy': ['Milano', 'Rome'],
    'Japan': [],
    'Kazakhstan': [],
    'Kenya': [],
    'Latvia': [],
    'Liechtenstein': [],
    'Lithuania': [],
    'Luxembourg': [],
    'Macau': [],
    'Macedonia (FYROM)': [],
    'Malaysia': [],
    'Malta': [],
    'Mexico': [],
    'Moldova': [],
    'Monaco': [],
    'Mongolia': [],
    'Montenegro': [],
    'Morocco': [],
    'Netherlands': [],
    'New Zealand': [],
    'Nigeria': [],
    'Norway': [],
    'Pakistan': [],
    'Panama': [],
    'Philippines': [],
    'Poland': [],
    'Portugal': [],
    'Qatar': [],
    'Romania': ['Bucharest', 'NoSpy Bucharest'],
    'Russia': [],
    'Saudi Arabia': [],
    'Serbia': [],
    'Singapore': [],
    'Slovakia': [],
    'Slovenia': [],
    'South Africa': [],
    'South Korea': [],
    'Spain': ['Barcelona', 'Madrid'],
    'Sri Lanka': [],
    'Sweden': [],
    'Switzerland': ['Huenenberg', 'Zurich'],
    'Taiwan': [],
    'Thailand': [],
    'Turkey': [],
    'Ukraine': [],
    'United Arab Emirates': [],
    'United Kingdom': ['Berkshire', 'London', 'Manchester'],
    'United States': [
        'Atlanta',
        'Chicago',
        'Dallas',
        'Las Vegas',
        'Los Angeles',
        'Miami',
        'New York',
        'Los Angeles',
        'Miami',
        'New York',
        'Phoenix',
        'San Francisco',
        'Seattle',
        'Washington'
    ],
    'Venezuela': [],
    'Vietnam': []
}
