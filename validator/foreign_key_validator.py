# validators/foreign_key_validator.py

from typing import Dict


class ForeignKeyValidator:

    def __init__(self, connection):
        self.connection = connection

    def exists(self,
               table_name: str,
               column_name: str,
               value) -> bool:
        """
        Checks whether a foreign key value exists.

        Example:
            exists(
                "warehouse",
                "warehouse_id",
                101
            )
        """

        sql = f"""
            SELECT COUNT(*)
            FROM {table_name}
            WHERE {column_name}=%s
        """

        cursor = self.connection.cursor()

        cursor.execute(sql, (value,))

        count = cursor.fetchone()[0]

        cursor.close()

        return count > 0

    def validate_row(self,
                     foreign_keys: Dict,
                     row: Dict):
        """
        foreign_keys example:

        {
            "warehouse_id": {
                "table": "warehouse",
                "column": "warehouse_id"
            },
            "customer_id": {
                "table": "customer",
                "column": "customer_id"
            }
        }

        """

        errors = []

        for excel_column, config in foreign_keys.items():

            value = row.get(excel_column)

            if value is None:
                continue

            exists = self.exists(
                config["table"],
                config["column"],
                value
            )

            if not exists:
                errors.append(
                    f"{excel_column}: '{value}' not found in {config['table']}"
                )

        return errors