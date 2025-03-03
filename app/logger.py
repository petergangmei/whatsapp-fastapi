import logging
import sys
from typing import Any

# Configure logging format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

class Logger:
    """Custom logger class for the application."""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def info(self, message: Any, *args: Any, **kwargs: Any) -> None:
        """Log info level message."""
        self.logger.info(message, *args, **kwargs)
    
    def error(self, message: Any, *args: Any, **kwargs: Any) -> None:
        """Log error level message."""
        self.logger.error(message, *args, **kwargs)
    
    def warning(self, message: Any, *args: Any, **kwargs: Any) -> None:
        """Log warning level message."""
        self.logger.warning(message, *args, **kwargs)
    
    def debug(self, message: Any, *args: Any, **kwargs: Any) -> None:
        """Log debug level message."""
        self.logger.debug(message, *args, **kwargs)

# Create default logger instance
logger = Logger("whatsapp_service")
