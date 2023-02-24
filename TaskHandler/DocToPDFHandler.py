import os
import shutil

import docx2pdf
import pythoncom


class DocToPDFHandler:
    def doc_to_pdf(self, doc_file_path, pdf_file_path):

        pythoncom.CoInitialize()

        # Rename the file to have the .docx extension
        _, ext = os.path.splitext(doc_file_path)
        if ext != '.docx':
            temp_doc_file_path = doc_file_path + '.docx'
            shutil.move(doc_file_path, temp_doc_file_path)
            doc_file_path = temp_doc_file_path

        docx2pdf.convert(doc_file_path, pdf_file_path)

        # Delete the temporary file, if created
        if ext != '.docx':
            os.remove(doc_file_path)