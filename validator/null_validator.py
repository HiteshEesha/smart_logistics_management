"""
null_validator.py

Purpose:
    1. Validate required columns exist.
    2. Validate NOT NULL columns.
    3. Return valid and invalid records separately.
"""

import pandas as pd

from config.logger import Logger

logger = Logger.get_logger()


class NullValidator:

    def __init__(self, required_columns):
        """
        Parameters
        ----------
        required_columns : list

        Example:

        [
            "shipment_id",
            "order_date",
            "origin",
            "destination",
            "weight",
            "courier_id",
            "status"
        ]
        """

        self.required_columns = required_columns

    def validate(self, dataframe: pd.DataFrame):

        logger.info("Starting NULL Validation")

        # -------------------------------
        # Step 1 : Required Columns Check
        # -------------------------------

        missing_columns = list(
            set(self.required_columns) - set(dataframe.columns)
        )

        if missing_columns:

            logger.error(
                f"Missing Required Columns : {missing_columns}"
            )

            raise ValueError(
                f"Missing Required Columns : {missing_columns}"
            )

        # ------------------------------------
        # Step 2 : Blank String → NULL
        # ------------------------------------

        dataframe = dataframe.replace(
            r'^\s*$',
            pd.NA,
            regex=True
        )

        # ------------------------------------
        # Step 3 : Check NULL Values
        # ------------------------------------

        error_records = []

        for column in self.required_columns:

            null_rows = dataframe[
                dataframe[column].isna()
            ]

            if not null_rows.empty:

                logger.warning(
                    f"{column} contains "
                    f"{len(null_rows)} NULL value(s)"
                )

                for index in null_rows.index:

                    error_records.append({

                        "row_number": index + 2,

                        "column_name": column,

                        "error_message": f"{column} cannot be NULL"

                    })

        # ------------------------------------
        # Step 4 : Separate Valid/Invalid Rows
        # ------------------------------------

        invalid_mask = dataframe[
            self.required_columns
        ].isna().any(axis=1)

        invalid_dataframe = dataframe[invalid_mask].copy()

        valid_dataframe = dataframe[~invalid_mask].copy()

        logger.info(
            f"Valid Records   : {len(valid_dataframe)}"
        )

        logger.info(
            f"Invalid Records : {len(invalid_dataframe)}"
        )

        return {

            "status": len(error_records) == 0,

            "valid_data": valid_dataframe,

            "invalid_data": invalid_dataframe,

            "errors": error_records

        }