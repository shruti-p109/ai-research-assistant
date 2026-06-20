# setup.py
from database import engine, Base
import models  # registers tables with Base
from logger_setup import logger

logger.info("Initializing database..")
Base.metadata.create_all(bind=engine)
logger.info("Database ready.")
