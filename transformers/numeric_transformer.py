"""
numeric_transformer.py

Purpose:
    Convert numeric columns before validation.
"""

import pandas as pd


class NumericTransformer:

    @staticmethod
    def convert_integer(df, columns):

        for column in columns:

            if column in df.columns:

                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce"
                ).astype("Int64")

        return df

    @staticmethod
    def convert_float(df, columns):

        for column in columns:

            if column in df.columns:

                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce"
                )

        return df

    @staticmethod
    def round_decimal(df, columns, decimals=2):

        for column in columns:

            if column in df.columns:

                df[column] = df[column].round(decimals)

        return df

    @staticmethod
    def fill_null_numeric(df, columns, value=0):

        for column in columns:

            if column in df.columns:

                df[column] = df[column].fillna(value)

        return df