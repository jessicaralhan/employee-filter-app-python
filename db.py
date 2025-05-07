import mysql.connector
from configparser import ConfigParser
from logger import get_logger

logger = get_logger(__name__)

def get_connection():
    try:       
        config = ConfigParser()
        config.read('config.ini')
                
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
        raise

def execute_query(statement, params=(), fetch=False):
    conn = None
    cursor = None   
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)  
        print("statement", statement)
        print("params", params)
        logger.info(f"Executing query: {statement}")
        logger.info(f"With parameters: {params}")
        cursor.execute(statement, params)
        
        if fetch:
            result = cursor.fetchall()
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
