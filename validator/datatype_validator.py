"""
datatype_validator.py

Purpose:
    Validate and convert DataFrame columns
    to expected data types.
"""

import pandas as pd

from config.logger import Logger

logger = Logger.get_logger()


class DatatypeValidator:

    def __init__(self, datatype_config: dict):
        """
        Example:

        {
            "shipment_id": "string",
            "order_date": "date",
            "weight": "float",
            "capacity": "int",
            "timestamp": "datetime"
        }
        """

        self.datatype_config = datatype_config

    def validate(self, dataframe: pd.DataFrame):

        logger.info("Starting Datatype Validation")

        dataframe = dataframe.copy()

        error_records = []

        invalid_index = set()

        for column, datatype in self.datatype_config.items():

            if column not in dataframe.columns:
                continue

            # -----------------------------
            # STRING
            # -----------------------------
            if datatype == "string":

                dataframe[column] = (
                    dataframe[column]
                    .astype("string")
                    .str.strip()
                )

            # -----------------------------
            # INTEGER
            # -----------------------------
            elif datatype == "int":

                converted = pd.to_numeric(
                    dataframe[column],
                    errors="coerce"
                )

                invalid = dataframe[
                    converted.isna() &
                    dataframe[column].notna()
                ]

                for idx, row in invalid.iterrows():

                    error_records.append({
                        "row_number": idx + 2,
                        "column_name": column,
                        "invalid_value": row[column],
                        "expected_type": "INTEGER"
                    })

                    invalid_index.add(idx)

                dataframe[column] = converted.astype("Int64")

            # -----------------------------
            # FLOAT / DECIMAL
            # -----------------------------
            elif datatype == "float":

                converted = pd.to_numeric(
                    dataframe[column],
                    errors="coerce"
                )

                invalid = dataframe[
                    converted.isna() &
                    dataframe[column].notna()
                ]

                for idx, row in invalid.iterrows():

                    error_records.append({
                        "row_number": idx + 2,
                        "column_name": column,
                        "invalid_value": row[column],
                        "expected_type": "DECIMAL"
                    })

                    invalid_index.add(idx)

                dataframe[column] = converted

            # -----------------------------
            # DATE
            # -----------------------------
            elif datatype == "date":

                converted = pd.to_datetime(
                    dataframe[column],
                    errors="coerce"
                )

                invalid = dataframe[
                    converted.isna() &
                    dataframe[column].notna()
                ]

                for idx, row in invalid.iterrows():

                    error_records.append({
                        "row_number": idx + 2,
                        "column_name": column,
                        "invalid_value": row[column],
                        "expected_type": "DATE"
                    })

                    invalid_index.add(idx)

                dataframe[column] = converted.dt.date

            # -----------------------------
            # DATETIME
            # -----------------------------
            elif datatype == "datetime":

                converted = pd.to_datetime(
                    dataframe[column],
                    errors="coerce"
                )

                invalid = dataframe[
                    converted.isna() &
                    dataframe[column].notna()
                ]

                for idx, row in invalid.iterrows():

                    error_records.append({
                        "row_number": idx + 2,
                        "column_name": column,
                        "invalid_value": row[column],
                        "expected_type": "DATETIME"
                    })

                    invalid_index.add(idx)

                dataframe[column] = converted

        valid_dataframe = dataframe.drop(index=list(invalid_index))

        invalid_dataframe = dataframe.loc[list(invalid_index)]

        logger.info(
            f"Valid Records   : {len(valid_dataframe)}"
        )

        logger.info(
            f"Invalid Records : {len(invalid_dataframe)}"
        )

        return {

            "status": len(error_records) == 0,

            "valid_data": valid_dataframe.reset_index(drop=True),

            "invalid_data": invalid_dataframe.reset_index(drop=True),

            "errors": error_records

        }