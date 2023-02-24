import fitz
import os


class PDFToJPGHandler:

    def pdf_to_jpg(self, pdf_file):
        pdf_doc = fitz.open(pdf_file)
        for i in range(len(pdf_doc)):
            page = pdf_doc[i]
            pix = page.get_pixmap()
            jpg_file_path = os.path.join("TaskHandler/instance/uploads", "page-%i.jpg" % i)
            os.makedirs(os.path.dirname(jpg_file_path), exist_ok=True)
            pix.save(jpg_file_path)
        pdf_doc.close()



