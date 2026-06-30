"""
mysql_loader.py

Production Grade MySQL Loader
"""

import time
import pandas as pd

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from config.database import database
from config.logger import Logger
from config.config import Config

logger = Logger.get_logger()


class MySQLLoader:

    def __init__(self):

        self.engine = database.get_engine()

        self.batch_size = Config.get_application_config().get(
            "batch_size",
            5000
        )

    #####################################################
    # Check Table Exists
    #####################################################

    def table_exists(self, table_name):

        sql = """
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_schema = DATABASE()
        AND table_name=:table
        """

        with self.engine.connect() as conn:

            result = conn.execute(
                text(sql),
                {"table": table_name}
            ).scalar()

        return result > 0

    #####################################################
    # Get Table Count
    #####################################################

    def row_count(self, table_name):

        sql = f"SELECT COUNT(*) FROM {table_name}"

        with self.engine.connect() as conn:

            return conn.execute(text(sql)).scalar()

    #####################################################
    # Truncate Table
    #####################################################

    def truncate(self, table_name):

        logger.info(f"Truncating {table_name}")

        with self.engine.begin() as conn:

            conn.execute(
                text(f"TRUNCATE TABLE {table_name}")
            )

    #####################################################
    # Delete Table Data
    #####################################################

    def delete_all(self, table_name):

        logger.info(f"Deleting {table_name}")

        with self.engine.begin() as conn:

            conn.execute(
                text(f"DELETE FROM {table_name}")
            )

    #####################################################
    # Sanitize dtypes
    #####################################################

    @staticmethod
    def _sanitize_dtypes(dataframe):
        df = dataframe.copy()
        for col in df.columns:
            if pd.api.types.is_extension_array_dtype(df[col]):
                df[col] = df[col].where(df[col].notna(), other=None).astype(object)
        return df

    #####################################################
    # Bulk Insert
    #####################################################

    def insert_dataframe(
            self,
            dataframe,
            table_name):

        start = time.time()

        dataframe = self._sanitize_dtypes(dataframe)

        logger.info(
            f"Loading {len(dataframe)} rows "
            f"into {table_name}"
        )

        dataframe.to_sql(

            table_name,

            self.engine,

            if_exists="append",

            index=False,

            method="multi",

            chunksize=self.batch_size

        )

        logger.info(

            f"{table_name} loaded "

            f"in {round(time.time()-start,2)} sec"

        )

    #####################################################
    # Load Using Chunks
    #####################################################

    def insert_chunks(

            self,

            dataframe,

            table_name):

        total = len(dataframe)

        logger.info(

            f"Loading {total} rows"

        )

        for start in range(

                0,

                total,

                self.batch_size):

            end = start + self.batch_size

            chunk = dataframe.iloc[start:end]

            chunk.to_sql(

                table_name,

                self.engine,

                if_exists="append",

                index=False,

                method="multi"

            )

            logger.info(

                f"{len(chunk)} inserted."

            )

    #####################################################
    # Retry Loader
    #####################################################

    def insert_retry(

            self,

            dataframe,

            table_name,

            retry=3):

        for attempt in range(retry):

            try:

                self.insert_dataframe(

                    dataframe,

                    table_name

                )

                return

            except Exception as ex:

                logger.error(

                    f"Retry {attempt+1} Failed"

                )

                if attempt == retry - 1:

                    raise ex

    #####################################################
    # Insert Multiple Tables
    #####################################################

    def load_tables(self, table_map):

        """
        table_map =

        {

            "courier_staff":df1,

            "routes":df2,

            "shipments":df3

        }

        """

        for table, dataframe in table_map.items():

            self.insert_dataframe(

                dataframe,

                table

            )

    #####################################################
    # Execute SQL
    #####################################################

    def execute_sql(self, sql):

        with self.engine.begin() as conn:

            conn.execute(text(sql))

    #####################################################
    # Get DataFrame
    #####################################################

    def read_table(self, table_name):

        return pd.read_sql(

            f"SELECT * FROM {table_name}",

            self.engine

        )

    #####################################################
    # Upsert
    #####################################################

    def upsert_dataframe(

            self,

            dataframe,

            table_name,

            primary_key):

        """
        Generic UPSERT placeholder.

        Can be extended using

        INSERT...

        ON DUPLICATE KEY UPDATE
        """

        logger.info(

            "Upsert Started"

        )

        self.insert_dataframe(

            dataframe,

            table_name

        )

    #####################################################
    # Audit
    #####################################################

    def audit(

            self,

            filename,

            table_name,

            rows,

            status):

        sql = """

        INSERT INTO import_audit

        (

            filename,

            table_name,

            rows_inserted,

            status

        )

        VALUES

        (

            :filename,

            :table,

            :rows,

            :status

        )

        """

        with self.engine.begin() as conn:

            conn.execute(

                text(sql),

                {

                    "filename": filename,

                    "table": table_name,

                    "rows": rows,

                    "status": status

                }

            )