# validators/duplicate_validator.py

from typing import List, Dict
import pymysql


class DuplicateValidator:

    def __init__(self, connection):
        self.connection = connection

    def is_duplicate(self,
                     table_name: str,
                     unique_columns: List[str],
                     row: Dict) -> bool:
        """
        Checks if a record already exists.

        Parameters
        ----------
        table_name : str
        unique_columns : List[str]
        row : Dict

        Returns
        -------
        bool
        """

        where_clause = " AND ".join(
            [f"{column}=%s" for column in unique_columns]
        )

        sql = f"""
            SELECT COUNT(*)
            FROM {table_name}
            WHERE {where_clause}
        """

        values = [row[column] for column in unique_columns]

        cursor = self.connection.cursor()
        cursor.execute(sql, values)

        count = cursor.fetchone()[0]

        cursor.close()

        return count > 0