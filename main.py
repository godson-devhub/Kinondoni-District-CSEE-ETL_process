from config import SCHOOL_URLS
from extractor import fetch_html, extract_school_data
from transformer import transform_data
from loader import save_csv

from utils import (
    safe_sleep,
    extract_school_code,
    setup_logger,
    log_extraction,
    log_transformation,
    log_loading,
    log_pipeline_start,
    log_pipeline_end
)

# setup logger
logger = setup_logger()

# start pipeline log
log_pipeline_start(logger)

all_data = []

print("STARTING ETL PIPELINE...")

for url in SCHOOL_URLS:

    # extract school code
    school_code = extract_school_code(url)

    print(f"Extracting: {school_code}")

    logger.info(f"Starting extraction for school: {school_code}")

    try:

        # fetch html page
        html = fetch_html(url)

        # extract student records
        records = extract_school_data(html, school_code)

        print(f"Records extracted: {len(records)}")

        # log extraction
        log_extraction(logger, school_code, len(records))

        # append data
        all_data.extend(records)

    except Exception as e:

        logger.error(
            f"Extraction failed for school {school_code} | Error: {str(e)}"
        )

        print(f"ERROR extracting {school_code}")

    # polite delay
    safe_sleep()

# total extracted records
print(f"\nTOTAL RECORDS: {len(all_data)}")

logger.info(f"TOTAL RECORDS EXTRACTED: {len(all_data)}")

# transform data
print("\nTRANSFORMING DATA...")

transformed = transform_data(all_data)

# log transformation
log_transformation(logger, len(all_data))

# display transformed data
print("\nTRANSFORMED DATA:")
print(transformed)

# save csv
save_csv(transformed)

# log loading
log_loading(
    logger,
    "data/processed/bmath_school_performance.csv"
)

print("\nCSV FILE SAVED SUCCESSFULLY")

# end pipeline
log_pipeline_end(logger)

print("\nETL PROCESS COMPLETED SUCCESSFULLY")