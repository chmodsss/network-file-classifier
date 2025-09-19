import time
import logging
from classifier import Classifier
from writer import write_results_to_file
from config import INPUT_DIR


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    start_time = time.time()
    c = Classifier(mock_flag=False, model="gpt-4o")
    classified_data = c.classify_pdfs(INPUT_DIR)
    output_path = write_results_to_file(classified_data)
    logger.info(f"Output written to {output_path}")
    for item in classified_data:
        logger.info(item)
    end_time = time.time()
    logger.info(f"Total processing time: {end_time - start_time:.2f} seconds")
