import mysql.connector
from configparser import ConfigParser
from logger import get_logger

logger = get_logger(__name__)

def get_connection():
    try:
        config = ConfigParser()
        config.read('config.ini')
        
        # Log the configuration (excluding password)
        logger.info(f"Connecting to database: {config['mysql']['database']} on {config['mysql']['host']}")
        
        connection = mysql.connector.connect(
            host=config['mysql']['host'],
            user=config['mysql']['user'],
            password=config['mysql']['password'],
            database=config['mysql']['database']
        )
        logger.info("Database connection established successfully")
        return connection
    except mysql.connector.Error as err:
        logger.error(f"Failed to connect to database: {err}")
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            logger.error("Access denied - check your username and password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            logger.error("Database does not exist")
        else:
            logger.error(f"Error: {err}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while connecting to database: {str(e)}")
        raise

def execute_query(statement, params=(), fetch=False):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)
        logger.info(f"Executing query: {statement}")
        logger.info(f"With parameters: {params}")
        cursor.execute(statement, params)
        
        if fetch:
            result = cursor.fetchall()
            logger.info(f"Retrieved {len(result)} records")
            return result
        
        conn.commit()
        logger.info("Query executed successfully")
        return True
        
    except mysql.connector.Error as err:
        logger.error(f"Database error: {err}")
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            logger.info("Database connection closed")
