import logging
import colorlog

def setup_logger():
	"""Return a logger with a default ColoredFormatter."""

	# create logger
	formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)-8s%(reset)s %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )

	logger = colorlog.getLogger('main-logger')

    # Console handler
	ch = colorlog.StreamHandler()
	ch.setFormatter(formatter)
	logger.addHandler(ch)

    # File handler
	fh = logging.FileHandler('app.log')
	fh.setFormatter(formatter)
	logger.addHandler(fh)

	logger.setLevel(logging.DEBUG)

	return logger

logger = setup_logger()