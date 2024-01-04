from uvicorn.config import LOGGING_CONFIG

# LOGGING CONFIG

log_config = LOGGING_CONFIG
log_config["handlers"]["file_handler"] = {
    "formatter": "default",
    "class": "logging.handlers.RotatingFileHandler",
    "filename": "logconfig.log",
}

log_config["handlers"]["file_handler_access"] = {
    "formatter": "access",
    "class": "logging.handlers.RotatingFileHandler",
    "filename": "logconfig.log",
}
log_config["loggers"]["uvicorn"]["handlers"] = ["default", "file_handler"]
log_config["loggers"]["uvicorn.access"]["handlers"] = ["access", "file_handler_access"]