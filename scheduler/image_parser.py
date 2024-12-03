import pytesseract
from PIL import Image
from pathlib import Path
import re

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)
IMAGE_DIR = BASE_DIR / "output_images" 
print(IMAGE_DIR)

def get_text():
    texts = []
    images = list(IMAGE_DIR.glob("*.png"))
    for image_path in images:
        with Image.open(image_path) as img:
            extracted_text = pytesseract.image_to_string(img)
            texts.append(extracted_text)
            print(extracted_text)
    return "\n".join(texts)

def get_semesters(text):
    semester_regex = r"^(Spring|Summer 1|Fall|Winter|Summer 2) \d{4} \(\d+\.\d+ Hours\)"
    semester_headers = re.finditer(semester_regex, text, re.MULTILINE)

    semester_classes = {}
    previous_header_end = None
    current_semester = None
    print(semester_headers)
    for header_match in semester_headers:
        if current_semester:
            classes_text = text[previous_header_end:header_match.start()].strip() #gets all the text between the last processed semester and the current semester
            semester_classes[current_semester] = classes_text
        print(header_match)
        current_semester = header_match.group(0) #gets the string for the matched semester so "Spring 2025 (17.0 hours)"
        previous_header_end = header_match.end() #If the match is "Spring 2025 (17.0 Hours)"" and it occurs at positions 0 to 24, then header_match.end() returns 25

    if current_semester:
        semester_classes[current_semester] = text[previous_header_end:].strip()
    print(semester_classes)
    return semester_classes

def filter_relevant_classes(semesters):
    relevant_classes = {}
    for semester, courses in semesters.items():
        class_lines = [
            re.sub(r"^-", "", course.strip())
            for course in courses.splitlines()
        ]
        relevant_classes[semester] = class_lines
    print(relevant_classes)
    return relevant_classes

if __name__ == "__main__":
    text = get_text()
    semesters = get_semesters(text=text)
    filter_relevant_classes(semesters=semesters)


