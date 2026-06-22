# setup.py
from storage.database import engine
from storage.models import Base # registers tables with Base
from logger_setup import logger

if __name__ == "__main__":
    logger.info("Initializing database..")
    Base.metadata.create_all(bind=engine)
    logger.info("Database ready.")
