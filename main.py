import os
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


if __name__ == "__main__":
    folder = "./src"  # Set your PDF folder
    classified_data = classify_pdfs_in_folder(folder)
    for item in classified_data:
        print(item)
