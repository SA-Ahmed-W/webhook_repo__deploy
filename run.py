from app import create_app
from utils.init_logger import logger
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


# Get environment variable
PORT = os.getenv('PORT', 5000)
ENV = os.getenv('FLASK_ENV', 'development')
DEBUG = os.getenv('FLASK_DEBUG', False)


if ENV == 'development':
    logger.info("Starting the application in development mode...")
else:
    logger.info("Starting the application in production mode...")

app = create_app()

if __name__ == "__main__":
    logger.info("Starting the application...")
    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)