from app.main import create_app
from app.libs.logger import get_logger

logger = get_logger()
app = create_app()

if __name__ == "__main__":
    logger.info("Starting the application...")
    app.run(debug=True, host="0.0.0.0", port=5000, threaded=True, use_reloader=True)