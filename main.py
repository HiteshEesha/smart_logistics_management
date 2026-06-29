from config.database import database
from config.logger import Logger
from readers.csv_reader import CSVReader
from readers.json_reader import JSONReader
from loaders.mysql_loader import MySQLLoader

logger = Logger.get_logger()

logger.info("Starting Logistics ETL")

database.test_connection()

logger.info("Connection Successful")

# Read CSV
shipment_reader = CSVReader("datasets/shipments.csv")
shipments_df = shipment_reader.read()

# Read JSON
courier_reader = JSONReader("datasets/courier_staff.json")
courier_df = courier_reader.read()

print(shipments_df.head())
print(courier_df.head())


loader = MySQLLoader()


courier_df = CSVReader("courier.csv").read()
"""courier_df = validator.validate(courier_df)"""
loader.insert_dataframe(courier_df, "courier_staff")

routes_df = CSVReader("routes.csv").read()
"""routes_df = validator.validate(routes_df)"""
loader.insert_dataframe(routes_df, "routes")

warehouse_df = CSVReader("warehouse.csv").read()
"""warehouse_df = validator.validate(warehouse_df)"""
loader.insert_dataframe(warehouse_df, "warehouses")

shipment_df = CSVReader("shipments.csv").read()
"""shipment_df = validator.validate(shipment_df)"""
loader.insert_dataframe(shipment_df, "shipments")

tracking_df = CSVReader("tracking.csv").read()
"""tracking_df = validator.validate(tracking_df)"""
loader.insert_dataframe(tracking_df, "shipment_tracking")

cost_df = CSVReader("cost.csv").read()
"""cost_df = validator.validate(cost_df)"""
loader.insert_dataframe(cost_df, "costs")