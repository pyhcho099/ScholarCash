import os
import sys
import logging
import MySQLdb
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def check_database_connection():
    load_dotenv()

    # Required environment variables
    required_vars = ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST']
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        logger.error(f"Missing environment variables: {', '.join(missing_vars)}")
        return False

    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = int(os.getenv('DB_PORT', 3306))

    # Mask sensitive info for logging
    masked_user = f"{db_user[:1]}***" if db_user and len(db_user) > 1 else "***"
    logger.info(f"Attempting connection to {db_host}:{db_port} as user '{masked_user}' for database '{db_name}'...")

    try:
        # Connect with timeout
        db = MySQLdb.connect(
            host=db_host,
            user=db_user,
            passwd=db_password,
            db=db_name,
            port=db_port,
            connect_timeout=5
        )
        logger.info("Connection successful!")

        cursor = db.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        logger.info(f"Database version: {version}")

        db.close()
        return True

    except MySQLdb.Error as e:
        logger.error(f"MySQL Error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    if check_database_connection():
        sys.exit(0)
    else:
        sys.exit(1)
