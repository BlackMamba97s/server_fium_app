import unittest
import io
from unittest.mock import patch
from flask import Flask
import os
from TaskHandler.PDFToJPGHandler import PDFToJPGHandler
import shutil


class PDFToJPGTestCase(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.uploads_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'TaskHandler/instance/uploads/'))
        os.makedirs(self.uploads_dir, exist_ok=True)
        with open(os.path.join(self.uploads_dir, "test.pdf"), "wb") as f:
            f.write(b"test content")

    def test_upload_dispatcher(self):
        with open("test.pdf", "wb") as f:
            f.write(b"test content")
        with open("test.pdf", "rb") as f:
            response = self.client.post("/upload", data={'file': (f, 'test.pdf')}, content_type='multipart/form-data')
        assert response.status_code == 200
        assert os.path.isfile("TaskHandler/instance/uploads/test.pdf")

    def test_pdf_to_jpg(self):
        with open("test.pdf", "wb") as f:
            f.write(b"test content")
        with open("test.pdf", "rb") as f:
            response = self.client.post("/upload", data={'file': (f, 'test.pdf')}, content_type='multipart/form-data')
        assert response.status_code == 200
        assert os.path.isfile(os.path.join(self.uploads_dir, 'page-0.jpg'))

    def test_pdf_to_jpg_zip(self):
        with open("test.pdf", "wb") as f:
            f.write(b"test content")
        with open("test.pdf", "rb") as f:
            response = self.client.post("/upload", data={'file': (f, 'test.pdf')}, content_type='multipart/form-data')
        assert response.status_code == 200
        assert os.path.isfile(os.path.join(self.uploads_dir, 'jpgs.zip'))

    def tearDown(self):
        try:
            shutil.rmtree(self.uploads_dir)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    unittest.main()
