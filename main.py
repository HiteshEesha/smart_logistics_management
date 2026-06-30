from config.database import database
from config.logger import Logger
from readers.csv_reader import CSVReader
from readers.json_reader import JSONReader
from loaders.mysql_loader import MySQLLoader
from validator.validation_service import ValidationService
from config.table_config import TABLE_CONFIG

logger = Logger.get_logger()

logger.info("Starting Logistics ETL")

database.test_connection()

logger.info("Connection Successful")


loader = MySQLLoader()
#connection = database.get_engine

#validator = ValidationService(connection)

'''
# Shipment
shipment_df = CSVReader("shipment.csv").read()

shipment_df = validator.validate(
    shipment_df,
    "shipment"
)

loader.insert_dataframe(
    shipment_df,
    "shipment"
)


# Shipment_tracking
shipment_tracking_df = CSVReader("shipment_tracking.csv").read()

shipment_tracking_df = validator.validate(
    shipment_tracking_df,
    "shipment_tracking"
)

loader.insert_dataframe(
    shipment_df,
    "shipment"
)

#courier
courier_df = CSVReader("courier_staff.csv").read()
courier_df = validator.validate(
    courier_df,
    "courier_staff"
)

loader.insert_dataframe(
    courier_df,
    "courier_staff"
)


# Warehouse
warehouse_df = CSVReader("warehouse.csv").read()

warehouse_df = validator.validate(
    warehouse_df,
    "warehouses"
)

loader.insert_dataframe(
    warehouse_df,
    "warehouses"
)


# routes
routes_df = CSVReader("routes.csv").read()
routes_df = validator.validate(
    routes_df,
    "routes"
)

loader.insert_dataframe(
    routes_df,
    "routes"
)


# costs
costs_df = CSVReader("costs.csv").read()
costs_df = validator.validate(
    costs_df,
    "costs"
)

loader.insert_dataframe(
    costs_df,
    "costs"
) '''


for table_name, config in TABLE_CONFIG.items():

    print(f"Processing {table_name}")

    file = config["file"]
    df = JSONReader(file).read() if file.endswith(".json") else CSVReader(file).read()

    df = ValidationService.validate(
        dataframe=df,
        table_name=table_name,
        validators=config["validators"]
    )

    loader.insert_dataframe(df, table_name)