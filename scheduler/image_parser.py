import pytesseract
from PIL import Image
from pathlib import Path

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)
IMAGE_DIR = BASE_DIR / "output_images" 
print(IMAGE_DIR)

def get_text():
    text = ""
    images = list(IMAGE_DIR.glob("*.png"))
    print(images)
    for image_path in images:
        print(image_path)
        with Image.open(image_path) as img:
            text = pytesseract.image_to_string(img)
    print(text)

get_text()


