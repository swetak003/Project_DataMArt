import logging
import os
from datetime import datetime

# Log file name
LOG_FILE = f"dmart_project_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Logs directory (ONLY directory)
logs_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_dir, exist_ok=True)

# Full log file path
LOG_FILE_PATH = os.path.join(logs_dir, LOG_FILE)

# Logging configuration
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    level=logging.INFO
)

# ✅ THIS IS MANDATORY
logger = logging.getLogger(__name__)
