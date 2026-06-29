"""
json_reader.py

Purpose:
    Read JSON files and return a Pandas DataFrame.
"""

import json
from pathlib import Path

import pandas as pd

from config.logger import Logger

logger = Logger.get_logger()


class JSONReader:

    def __init__(
            self,
            file_path: str,
            lines: bool = False):

        self.file_path = Path(file_path)
        self.lines = lines

    def _validate_file(self):

        if not self.file_path.exists():
            raise FileNotFoundError(
                f"File not found : {self.file_path}"
            )

        if self.file_path.stat().st_size == 0:
            raise ValueError(
                f"File is empty : {self.file_path}"
            )

    def _clean_columns(self, dataframe):

        dataframe.columns = (
            dataframe.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        return dataframe

    def read(self):

        self._validate_file()

        logger.info(f"Reading JSON File : {self.file_path}")

        try:

            if self.lines:

                dataframe = pd.read_json(
                    self.file_path,
                    lines=True
                )

            else:

                with open(
                        self.file_path,
                        "r",
                        encoding="utf-8") as file:

                    data = json.load(file)

                dataframe = pd.DataFrame(data)

            dataframe = self._clean_columns(dataframe)

            logger.info(
                f"""JSON Loaded Successfully
                File      : {self.file_path.name}
                Rows      : {len(dataframe)}
                Columns   : {len(dataframe.columns)}"""
            )

            return dataframe

        except Exception as ex:

            logger.error(ex)

            raise