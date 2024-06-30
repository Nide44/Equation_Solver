import logging

from solver_lib.settings import LOGGING_LEVEL

logging.basicConfig(level=LOGGING_LEVEL)
error_logger = logging.getLogger("error")
info_logger = logging.getLogger("info")

error_handler = logging.FileHandler("error.log", mode="w")
info_handler = logging.FileHandler("info.log", mode="w")

error_formatter = logging.Formatter(
    "\t%(asctime)s \t %(name)s \t %(levelname)s \t %(message)s"
)
info_formatter = logging.Formatter(
    "\t%(asctime)s \t %(name)s \t %(levelname)s \t %(message)s"
)

error_handler.setFormatter(error_formatter)
info_handler.setFormatter(info_formatter)

error_logger.addHandler(error_handler)
info_logger.addHandler(info_handler)
