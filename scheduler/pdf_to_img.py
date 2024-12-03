from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
from pathlib import Path

class PDFToImageConverter:
    #initialize converter with path to pdf and path to save the converted img
    def __init__(self, pdf_dir: Path, image_dir: Path):
        self.pdf_dir = pdf_dir
        self.image_dir = image_dir

        self.image_dir.mkdir(exist_ok=True)
    #iterate over all the pdfs in directory
    def list_pdfs(self):
        pdfs = list(PDF_DIR.glob("*.pdf"))
        for pdf in pdfs:
            print(pdf)
        return pdfs
    #convert a single pdf to image
    def convert_pdf_to_image(self, pdf_file: Path):
        images = convert_from_path(pdf_file)
        for i, image in enumerate(images):
            output_image_path = self.image_dir / f"{pdf_file.stem}_page_{i+1}.png"
            image.save(output_image_path, "PNG")
            print(f"Saved: {output_image_path}")
    #use list_pdf and convert_pdf_to_image to convert all pdfs in a directory
    def convert_all_pdfs(self):
        pdf_files = self.list_pdfs()
        for pdf in pdf_files:
            self.convert_pdf_to_image(pdf)

BASE_DIR = Path(__file__).resolve().parent.parent

PDF_DIR = BASE_DIR / "pdfs"
IMAGE_DIR = BASE_DIR / "output_images" 

IMAGE_DIR.mkdir(exist_ok=True)

if __name__ == "__main__":
    converter = PDFToImageConverter(pdf_dir=PDF_DIR, image_dir=IMAGE_DIR)
    converter.convert_all_pdfs()

