INPUT_DIR = "pdf_files/"

OUTPUT_DIR = "output/"

TEMP_DIR = ".temp_uploads"

CLASSIFIER_PROMPT = """
Classify the following document text into these categories:
(1) Is the document technical (True or False)?
(2) List main topics covered in the document (examples: wi-fi, routing, switching, 5g, edge computing).
(3) Name the networking vendor mentioned if any (e.g. Cisco, Juniper, Nokia), or null.

Provide output as JSON strictly matching this schema:
{{
  "is_technical": true/false,
  "topics": ["topic1", "topic2"],
  "vendor": "VendorName" or null
}}

Document Text:
\"\"\"
{text}
\"\"\"
"""
