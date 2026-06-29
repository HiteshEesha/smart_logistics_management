"""
transaction_manager.py

Purpose:
    Manage MySQL transactions using SQLAlchemy.
"""

from contextlib import contextmanager
from sqlalchemy.exc import SQLAlchemyError

from config.database import database
from config.logger import Logger

logger = Logger.get_logger()


class TransactionManager:

    @staticmethod
    @contextmanager
    def transaction():

        session = database.get_session()

        try:

            logger.info("Transaction Started")

            yield session

            session.commit()

            logger.info("Transaction Committed Successfully")

        except SQLAlchemyError as ex:

            session.rollback()

            logger.error(f"Transaction Rolled Back : {ex}")

            raise

        except Exception as ex:

            session.rollback()

            logger.error(f"Transaction Failed : {ex}")

            raise

        finally:

            session.close()

            logger.info("Database Session Closed")