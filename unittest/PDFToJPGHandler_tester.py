import unittest
import os

from fitz import fitz

from TaskHandler.PDFToJPGHandler import PDFToJPGHandler
import shutil

class PDFToJPGHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.pdf_file = 'test.pdf'
        self.pdf_to_jpg_handler = PDFToJPGHandler()
        self.uploads_dir = 'TaskHandler/instance/uploads/'

    def test_pdf_to_jpg(self):
        with open(self.pdf_file, "wb") as f:
            f.write(b"test content")
        self.pdf_to_jpg_handler.pdf_to_jpg(self.pdf_file)
        for i in range(1):
            jpg_file_path = os.path.join(self.uploads_dir, "page-%i.jpg" % i)
            self.assertTrue(os.path.exists(jpg_file_path))

    def test_pdf_to_jpg_with_nonexistent_file(self):
        pdf_file = 'nonexistent.pdf'
        with self.assertRaises(FileNotFoundError):
            self.pdf_to_jpg_handler.pdf_to_jpg(pdf_file)

    def test_pdf_to_jpg_with_non_pdf_file(self):
        pdf_file = 'not_a_pdf.txt'
        with open(pdf_file, "wb") as f:
            f.write(b"test content")
        with self.assertRaises(fitz.FitzError):
            self.pdf_to_jpg_handler.pdf_to_jpg(pdf_file)

    def test_pdf_to_jpg_with_multiple_pages(self):
        pdf_file = 'multiple_pages.pdf'
        with open(pdf_file, "wb") as f:
            f.write(b"test content")
            f.write(b"test content")
        self.pdf_to_jpg_handler.pdf_to_jpg(pdf_file)
        for i in range(2):
            jpg_file_path = os.path.join(self.uploads_dir, "page-%i.jpg" % i)
            self.assertTrue(os.path.exists(jpg_file_path))

    def tearDown(self):
        try:
            shutil.rmtree(self.uploads_dir)
        except Exception as e:
            print(e)