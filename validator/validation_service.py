from null_validator import NullValidator
from duplicate_validator import DuplicateValidator
from foreign_key_validator import ForeignKeyValidator
from business_validator import BusinessValidator

class ValidationService:

    def __init__(self, connection):
        self.connection = connection

        self.duplicate_validator = DuplicateValidator(connection)
        self.fk_validator = ForeignKeyValidator(connection)
        self.business_validator = BusinessValidator()

    def validate(self, dataframe, table_name, config):

        dataframe = NullValidator.validate(dataframe)

        dataframe = self.duplicate_validator.validate_dataframe(
            dataframe,
            table_name
        )

        dataframe = self.fk_validator.validate_dataframe(
            dataframe
        )

        dataframe = self.business_validator.validate_dataframe(
            dataframe
        )

        return dataframe