import time
import random
import logging
import os


def safe_sleep(min_sec=1, max_sec=3):
    """
    Random sleep to avoid overloading NECTA server
    """
    time.sleep(random.uniform(min_sec, max_sec))


def extract_school_code(url):
    """
    Extract school code from URL
    Example:
    https://.../s4210.htm -> s4210
    """
    return url.split("/")[-1].replace(".htm", "")


def setup_logger():
    """
    Configure ETL logger
    """

    # create logs folder if not exists
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        filename="logs/etl.log",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        filemode="a"
    )

    logger = logging.getLogger()

    return logger


def log_extraction(logger, school_code, total_records):
    """
    Log extraction process
    """

    logger.info(
        f"Successfully extracted {total_records} student records from school {school_code}"
    )


def log_transformation(logger, total_records):
    """
    Log transformation stage
    """

    logger.info(
        f"Transformation completed successfully for {total_records} records"
    )


def log_loading(logger, filepath):
    """
    Log loading stage
    """

    logger.info(
        f"Dataset loaded successfully into CSV file: {filepath}"
    )


def log_pipeline_start(logger):
    """
    Log ETL pipeline start
    """

    logger.info("ETL PIPELINE STARTED")


def log_pipeline_end(logger):
    """
    Log ETL pipeline completion
    """

    logger.info("ETL PIPELINE COMPLETED SUCCESSFULLY")