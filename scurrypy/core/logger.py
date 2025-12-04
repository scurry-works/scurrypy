from typing import Protocol

class LoggerLike(Protocol):
    def log_info(self, message: str): ...
    def log_warn(self, message: str): ...
    def log_error(self, message: str): ...
    def log_high_priority(self, message: str): ...
    def close(self): ...

class Logger(LoggerLike):
    """A utility class for logging messages, supporting log levels, color-coded console output, 
        optional file logging, and redaction of sensitive information. 
    """

    DEBUG = '\033[36m'
    """Debug color: CYCAN"""

    INFO = '\033[32m'
    """Info color: GREEN"""

    WARNING = '\033[33m'
    """Warning color: YELLOW"""

    ERROR = '\033[31m'
    """Error color: RED"""

    TIME = '\033[90m'
    """Timestamp color: GRAY"""

    RESET = '\033[0m'
    """Reset color: DEFAULT"""
    
    def __init__(self, debug_mode: bool = False, quiet: bool = False):
        """Initializes logger. Opens log file 'bot.log' for writing.

        Args:
            debug_mode (bool, optional): toggle debug messages. Defaults to False.
            quiet: (bool, optional): supress low-priority logs (INFO, DEBUG, WARN). Defaults to False.
        """
        try:
            self.fp = open('bot.log', 'w', encoding="utf-8")
            """Log file for writing."""
        except Exception as e:
            self.log_error(f"Error {type(e)}: {e}")

        self.debug_mode = debug_mode
        """If debug logs should be printed."""

        self.quiet = quiet
        """If only high-level logs should be printed."""

    def log_traceback(self):
        import traceback
        self.log("DEBUG", self.DEBUG, traceback.format_exc())
    
    def log(self, level: str, color: str, message: str):
        """Internal helper that writes formatted log to both file and console.

        Args:
            level (str): DEBUG, INFO, WARN, CRITICAL, ERROR
            color (str): color specified by Logger properties
            message (str): descriptive message to log
        """
        if self.quiet and level not in ('ERROR', 'WARN', 'HIGH'):
            return # suppress lower-level logs in quiet mode
        
        from datetime import datetime
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.fp.write(f"[{date}] {level}: {message}\n")
        self.fp.flush()
        print(f"{self.TIME}[{date}]{self.RESET} {color}{level}:{self.RESET} {message}\n")
    
    def log_info(self, message: str):
        """Logs a info-level message.

        Args:
            message (str): descriptive message to log
        """
        self.log("INFO", self.INFO, message)
    
    def log_warn(self, message: str):
        """Logs a warn-level message.

        Args:
            message (str): descriptive message to log
        """
        self.log("WARN", self.WARNING, message)
    
    def log_error(self, message: str):
        """Logs a error-level message.

        Args:
            message (str): descriptive message to log
        """
        self.log("ERROR", self.ERROR, message)

        if self.debug_mode == True:
            self.log_traceback()
    
    def log_high_priority(self, message: str):
        """Always log this, regardless of quiet/debug_mode.

        Args:
            message (str): descriptive message to log
        """
        self.log("HIGH", self.INFO, message)
    
    def close(self):
        """Closes the log file."""
        self.fp.close()
