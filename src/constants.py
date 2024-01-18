from pathlib import Path

BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S"
DOWNLOADS_DIR = BASE_DIR / "downloads"
DT_FORMAT = "%d.%m.%Y %H:%M:%S"
ENCODING_CONST = "utf-8"
EXPECTED_STATUS = {
    "A": ("Active", "Accepted"),
    "D": ("Deferred",),
    "F": ("Final",),
    "P": ("Provisional",),
    "R": ("Rejected",),
    "S": ("Superseded",),
    "W": ("Withdrawn",),
    "": ("Draft", "Active"),
}
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "parser.log"
LXML = "lxml"
MAIN_DOC_URL = "https://docs.python.org/3/"
PATTERN_DOWNLOAD = r".+pdf-a4\.zip$"
PATTERN_LATEST_VERSION = r"Python (?P<version>\d\.\d+) \((?P<status>.*)\)"
PEP_DOC_URL = "https://peps.python.org/"
