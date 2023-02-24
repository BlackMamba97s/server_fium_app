from PIL import Image
import os

class JPGToPDFHandler:
    def jpg_to_pdf(self, jpg_file, pdf_file):
        with Image.open(jpg_file) as img:
            img.save(pdf_file, 'PDF', resolution=100.0)