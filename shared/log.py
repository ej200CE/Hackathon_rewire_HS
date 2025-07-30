import logging 
from logging.handlers import RotatingFileHandler
import inspect
from pathlib import Path
import os

_configured = False

def setup_logger(
        component_name: str, 
        level: int = logging.INFO,
        max_bytes: int = 5_000_000,
        backup_count: int=5
) -> None:
    """
    Setup a logger for a component.

    Args:
        component_name: The name of the component.
        level: The level of the logger (i.e. INFO or DEBUG).
        max_bytes: The maximum number of bytes to write to the log file.
        backup_count: The maximum number of backup files to store.
    """
    global _configured
    if _configured:
        return

    # Create a directory for the logs
    root_dir = Path(__file__).resolve().parents[1]
    log_dir = root_dir/"logs"
    log_dir.mkdir(exist_ok=True)

    # Create a file handler in rotationfor the log file
    file_in_rotation = RotatingFileHandler(
        log_dir/f"{component_name}.log",
        maxBytes=max_bytes,
        backupCount=backup_count
    )

    file_in_rotation.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    
    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(file_in_rotation)

    if os.getenv("LOG_TO_STDOUT", "false").strip().lower() == "true":
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        root.addHandler(stream_handler)

    _configured = True
    

def auto_setup_logger(level: int = logging.INFO) -> None:
    """
    Call this at the very top of any script if you’d rather not think
    about names.  It inspects the caller’s filename, strips the
    extension, and passes that stem to `setup_logger()`.

    Example
    -------
    from shared.log import auto_setup_logger
    auto_setup_logger()           # → logs/my_script.log
    """
    caller_file = inspect.stack()[1].filename
    component_name = Path(caller_file).stem
    setup_logger(component_name, level)


