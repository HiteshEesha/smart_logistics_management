"""
date_transformer.py

Purpose:
    Convert date columns into MySQL compatible format.
"""

import pandas as pd


class DateTransformer:

    @staticmethod
    def convert_to_date(df, columns):

        for column in columns:

            if column in df.columns:

                df[column] = pd.to_datetime(
                    df[column],
                    errors="coerce"
                ).dt.date

        return df

    @staticmethod
    def convert_to_datetime(df, columns):

        for column in columns:

            if column in df.columns:

                df[column] = pd.to_datetime(
                    df[column],
                    errors="coerce"
                )

        return df

    @staticmethod
    def format_datetime(df, columns):

        for column in columns:

            if column in df.columns:

                df[column] = pd.to_datetime(
                    df[column],
                    errors="coerce"
                ).dt.strftime("%Y-%m-%d %H:%M:%S")

        return df

    @staticmethod
    def fill_missing_dates(df, column, default_date):

        if column in df.columns:

            df[column] = df[column].fillna(default_date)

        return df