from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from config.config import Config


class Database:

    def __init__(self):

        db = Config.get_database_config()

        self.engine = create_engine(

            f"mysql+pymysql://"
            f"{db['username']}:{quote_plus(db['password'])}"
            f"@{db['host']}:{db['port']}/{db['database']}",

            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            echo=False

        )

        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):

        return self.Session()

    def get_engine(self):

        return self.engine

    def test_connection(self):

        try:

            with self.engine.connect() as conn:

                print("Database Connected Successfully")

        except SQLAlchemyError as e:

            print(e)
            raise


database = Database()