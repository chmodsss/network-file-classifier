import json
import logging
from datetime import datetime
from config import OUTPUT_DIR


logger = logging.getLogger(__name__)


def write_results_to_file(data):
    """
    Write classification results to a timestamped JSON file in the output directory.

    Args:
        data (list): List of classification results to write.

    Returns:
        str: Path to the output JSON file.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    op_filename = f"classification_output_{timestamp}.json"
    target_file = OUTPUT_DIR + op_filename

    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    logger.info(f"Classification results saved to {target_file}")
    return target_file
