"""
csv_reader.py

Purpose:
    Read CSV files and return a Pandas DataFrame.

Author: Hitesh
"""

from pathlib import Path
import pandas as pd

from config.logger import Logger

logger = Logger.get_logger()


class CSVReader:

    def __init__(
            self,
            file_path: str,
            delimiter: str = ",",
            encoding: str = "utf-8",
            chunksize: int = None):

        self.file_path = Path(file_path)
        self.delimiter = delimiter
        self.encoding = encoding
        self.chunksize = chunksize

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

        logger.info(f"Reading CSV File : {self.file_path}")

        try:

            if self.chunksize:

                logger.info(
                    f"Reading in chunks of {self.chunksize}"
                )

                return pd.read_csv(
                    self.file_path,
                    sep=self.delimiter,
                    encoding=self.encoding,
                    chunksize=self.chunksize
                )

            dataframe = pd.read_csv(
                self.file_path,
                sep=self.delimiter,
                encoding=self.encoding
            )

            dataframe = self._clean_columns(dataframe)

            logger.info(
                f"""CSV Loaded Successfully
                File      : {self.file_path.name}
                Rows      : {len(dataframe)}
                Columns   : {len(dataframe.columns)}"""
            )

            return dataframe

        except Exception as ex:

            logger.error(ex)

            raise