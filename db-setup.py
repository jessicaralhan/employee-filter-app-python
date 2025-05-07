from db import execute_query
from logger import get_logger

logger = get_logger(__name__)

def initialize_database():  # run sql query to setup the db 
    try:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            country VARCHAR(50) NOT NULL,
            status VARCHAR(50) NOT NULL
        )
        """
        execute_query(create_table_query)   # execute sql query on db
        logger.info("Database table 'employees' initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise

if __name__ == "__main__":
    logger.info("Starting database initialization")
    initialize_database()
