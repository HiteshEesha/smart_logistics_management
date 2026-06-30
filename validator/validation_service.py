import pandas as pd

from validator.null_validator import NullValidator
from validator.duplicate_validator import DuplicateValidator
from validator.foreign_key_validator import ForeignKeyValidator
from validator.business_validator import BusinessValidator
from validator.datatype_validator import DatatypeValidator
from config.table_config import TABLE_CONFIG
from config.database import database
from config.logger import Logger

logger = Logger.get_logger()

_DTYPE_MAP = {
    int: "int",
    float: "float",
    str: "string",
    "datetime": "datetime",
    "date": "date",
}


class ValidationService:

    @staticmethod
    def validate(dataframe, table_name, validators):

        config = TABLE_CONFIG[table_name]

        if "null" in validators:
            result = NullValidator(config["required_columns"]).validate(dataframe)
            dataframe = result["valid_data"]
            logger.info(f"[{table_name}] After null validation: {len(dataframe)} rows")

        if "datatype" in validators:
            dt_config = {
                col: _DTYPE_MAP.get(dtype, "string")
                for col, dtype in config["data_types"].items()
            }
            result = DatatypeValidator(dt_config).validate(dataframe)
            dataframe = result["valid_data"]
            logger.info(f"[{table_name}] After datatype validation: {len(dataframe)} rows")

        if "duplicate" in validators:
            raw_conn = database.get_engine().raw_connection()
            try:
                dup_validator = DuplicateValidator(raw_conn)
                valid_rows = [
                    row for _, row in dataframe.iterrows()
                    if not dup_validator.is_duplicate(
                        table_name, config["duplicate_columns"], row
                    )
                ]
                dataframe = (
                    pd.DataFrame(valid_rows).reset_index(drop=True)
                    if valid_rows
                    else dataframe.iloc[0:0]
                )
            finally:
                raw_conn.close()
            logger.info(f"[{table_name}] After duplicate validation: {len(dataframe)} rows")

        if "foreign_key" in validators and config.get("foreign_keys"):
            raw_conn = database.get_engine().raw_connection()
            try:
                fk_validator = ForeignKeyValidator(raw_conn)
                valid_mask = dataframe.apply(
                    lambda row: len(
                        fk_validator.validate_row(config["foreign_keys"], row)
                    ) == 0,
                    axis=1,
                )
                dataframe = dataframe[valid_mask].reset_index(drop=True)
            finally:
                raw_conn.close()
            logger.info(f"[{table_name}] After FK validation: {len(dataframe)} rows")

        if "business" in validators:
            biz_validator = BusinessValidator()
            valid_mask = dataframe.apply(
                lambda row: len(biz_validator.validate(row)) == 0,
                axis=1,
            )
            dataframe = dataframe[valid_mask].reset_index(drop=True)
            logger.info(f"[{table_name}] After business validation: {len(dataframe)} rows")

        return dataframe
