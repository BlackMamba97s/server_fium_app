import os
import shutil
import tempfile
from pdf2docx import parse


class PDFToDocHandler:

    @staticmethod
    def pdf_to_doc(pdf_file_path, docx_file_path):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Use temporary directory to store intermediate files
            temp_file_path = os.path.join(temp_dir, 'temp.docx')
            # Parse PDF to docx format
            parse(pdf_file_path, temp_file_path)
            # Move the temporary docx file to the final destination
            shutil.move(temp_file_path, docx_file_path)