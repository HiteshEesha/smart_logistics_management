import logging
from pathlib import Path
from datetime import datetime

from config.config import Config


class Logger:

    logger = None

    @classmethod
    def get_logger(cls):

        if cls.logger:

            return cls.logger

        app = Config.get_application_config()

        log_directory = Path(app["log_directory"])

        log_directory.mkdir(exist_ok=True)

        log_file = log_directory / (
            f"etl_{datetime.now().strftime('%Y%m%d')}.log"
        )

        logger = logging.getLogger("LOGISTICS_ETL")

        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(

            "%(asctime)s | %(levelname)s | %(filename)s | %(message)s"

        )

        file_handler = logging.FileHandler(log_file)

        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()

        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        logger.addHandler(console_handler)

        cls.logger = logger

        return logger