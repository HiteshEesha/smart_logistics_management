"""
string_transformer.py

Purpose:
    Standardize string columns before validation/loading.
"""

import pandas as pd


class StringTransformer:

    @staticmethod
    def trim_whitespace(df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove leading and trailing whitespace.
        """

        object_columns = df.select_dtypes(include=["object"]).columns

        for column in object_columns:
            df[column] = df[column].astype(str).str.strip()

        return df

    @staticmethod
    def convert_uppercase(df, columns):

        for column in columns:

            if column in df.columns:
                df[column] = df[column].str.upper()

        return df

    @staticmethod
    def convert_lowercase(df, columns):

        for column in columns:

            if column in df.columns:
                df[column] = df[column].str.lower()

        return df

    @staticmethod
    def convert_titlecase(df, columns):

        for column in columns:

            if column in df.columns:
                df[column] = df[column].str.title()

        return df

    @staticmethod
    def replace_blank_with_null(df):

        df.replace(r'^\s*$', None, regex=True, inplace=True)

        return df

    @staticmethod
    def standardize_status(df, column):

        status_mapping = {

            "delivered": "Delivered",
            "in transit": "In Transit",
            "picked up": "Picked Up",
            "cancelled": "Cancelled",
            "pending": "Pending"

        }

        if column in df.columns:

            df[column] = (
                df[column]
                .astype(str)
                .str.lower()
                .map(status_mapping)
                .fillna(df[column])
            )

        return df