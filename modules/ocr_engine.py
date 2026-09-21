# # ============================================
# # MedSafe AI - OCR Engine (EasyOCR Version)
# # ============================================

# import easyocr
# import numpy as np
# from PIL import Image

# # Initialize reader once
# reader = easyocr.Reader(['en'], gpu=False)


# def extract_text_from_image(image):

#     # Convert PIL image to numpy array
#     image_np = np.array(Image.open(image))

#     results = reader.readtext(image_np)

#     # Combine detected text
#     extracted_text = " ".join([text[1] for text in results])

#     return extracted_text


# ============================================
# MedSafe AI - OCR Engine
# ============================================

import easyocr
import numpy as np
from PIL import Image


# Initialize OCR reader once
reader = easyocr.Reader(
    ["en"],
    gpu=False
)


def extract_text_from_image(image):

    try:

        image.seek(0)

        pil_image = Image.open(
            image
        ).convert("RGB")

        image_np = np.array(
            pil_image
        )

        results = reader.readtext(
            image_np,
            detail=1,
            paragraph=False
        )

        extracted_text = []

        for result in results:

            if len(result) >= 2:

                text = result[1].strip()

                if text:
                    extracted_text.append(text)

        return " ".join(
            extracted_text
        )

    except Exception as e:

        return f"OCR Error: {str(e)}"
