import os
import logging

def setup_logger():
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/server.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("visitor-management")