import datetime

class Logger:
    """
    Application Logger to store system events, warnings, and errors.
    It can dispatch these events to the terminal UI via a registered callback.
    """
    def __init__(self):
        self.logs = []
        self.callbacks = []
        
    def add(self, message, level="INFO"):
        """
        Add a new log entry.
        
        Args:
            message (str): The log message content.
            level (str): The severity level of the log (e.g., 'INFO', 'SUCCESS', 'ERROR', 'WARN').
        """
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        entry = {'time': timestamp, 'level': level, 'message': message}
        self.logs.append(entry)
        
        for cb in self.callbacks:
            try:
                cb(entry, level)
            except Exception:
                pass
                
    def get_all(self):
        """
        Retrieve all collected logs.
        
        Returns:
            list: A list of log entry dictionaries.
        """
        return self.logs

# Global logger instance
logger = Logger()
