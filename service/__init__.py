"""
Service Initialization Module
"""
import logging
import os
import sys
from flask import Flask

# Create Flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger("service")
logger.setLevel(logging.INFO)

# Log service startup status for verification
logger.info("**************************************************")
logger.info("SERVICERUNNING on port 8000")
logger.info("**************************************************")

# Import routes after app is defined
from service import routes  # noqa: F401, E402

