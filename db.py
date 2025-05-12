from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from configparser import ConfigParser
from logger import get_logger

logger = get_logger(__name__)

config = ConfigParser()
config.read('config.ini')

# DB_URL = URL.create(
#     drivername='mysql+mysqlconnector',
#     username=config['mysql']['user'],
#     password=config['mysql']['password'],
#     host=config['mysql']['host'],
#     database=config['mysql']['database']
# )

# print("db_url",DB_URL)
DB_URL = f"mysql+mysqlconnector://{config['mysql']['user']}:{config['mysql']['password']}@{config['mysql']['host']}/{config['mysql']['database']}"  #db url
# connect to your mysql database

engine = create_engine(DB_URL, echo=False)    # slqalchemy engine created 
logger.info("SQLAlchemy engine created successfully")

# session class used to interact with the database
SessionLocal = sessionmaker(autocommit=False , autoflush=False, bind=engine)   # configured Session class created
logger.info("SessionLocal configured successfully")
