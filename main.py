import os
import json
from config import INPUT_DIR, OUTPUT_DIR
from datetime import datetime
from pdf_reader import load_pdf_text
from classifier import classify_text_with_llm, ClassificationResult


def classify_pdfs_in_folder(folder_path: str):
    results = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            filepath = os.path.join(folder_path, filename)
            print(f"Processing: {filepath}")
            text = load_pdf_text(filepath)
            classification: ClassificationResult = classify_text_with_llm(text)
            results.append(
                {
                    "filename": filename,
                    "filepath": filepath,
                    "is_technical": classification.is_technical,
                    "topics": classification.topics,
                    "vendor": classification.vendor,
                }
            )
    return results


def write_output(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    op_filename = f"classification_output_{timestamp}.json"

    # Write JSON results to file
    with open(op_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"\nClassification results saved to {OUTPUT_DIR + op_filename}")


if __name__ == "__main__":
    classified_data = classify_pdfs_in_folder(INPUT_DIR)
    write_output(classified_data)
    for item in classified_data:
        print(item)
