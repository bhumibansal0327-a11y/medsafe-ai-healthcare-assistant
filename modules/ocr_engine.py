# ============================================
# MedSafe AI - OCR Engine (EasyOCR Version)
# ============================================

import easyocr
import numpy as np
from PIL import Image

# Initialize reader once
reader = easyocr.Reader(['en'], gpu=False)


def extract_text_from_image(image):

    # Convert PIL image to numpy array
    image_np = np.array(Image.open(image))

    results = reader.readtext(image_np)

    # Combine detected text
    extracted_text = " ".join([text[1] for text in results])

    return extracted_text