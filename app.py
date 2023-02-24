import glob
import zipfile

from fitz import fitz
from flask import Flask, request, send_file, send_from_directory
import os

from TaskHandler.DocToPDFHandler import DocToPDFHandler
from TaskHandler.JPGToPDFHandler import JPGToPDFHandler
from TaskHandler.PDFToDocHandler import PDFToDocHandler
from TaskHandler.PDFToJPGHandler import PDFToJPGHandler
from werkzeug.utils import secure_filename
import shutil

app = Flask(__name__)

uploads_dir = 'TaskHandler/instance/uploads/'

if os.path.exists(uploads_dir):
    shutil.rmtree(uploads_dir)

os.makedirs(uploads_dir)

@app.route('/upload', methods=['POST'])
def upload_dispatcher():
    file = request.files.get('file')
    conversion_type = request.form.get('selected_choice')
    print("the user is asking for " + conversion_type)
    if file:
        file.save(os.path.join(uploads_dir, secure_filename(file.filename)))
        if conversion_type == 'pdf to jpg':
            converter = PDFToJPGHandler()
            pdf_file = os.path.join(os.getcwd(), 'TaskHandler', 'instance', 'uploads', file.filename)
            pdf_doc = fitz.open(pdf_file)
            converter.pdf_to_jpg(pdf_file)
            if len(pdf_doc) > 1:
                zip_file_path = os.path.join(uploads_dir, "jpgs.zip")
                with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
                    for file in glob.glob(os.path.join(uploads_dir, '*.jpg')):
                        zip_file.write(file)
                print("if im here i did correctly")
                return send_file(zip_file_path, as_attachment=True,download_name='jpgs.zip')
            else:
                return send_from_directory(directory=uploads_dir, filename='page-0.jpg', as_attachment=True,
                                           download_name='page-0.jpg', path=uploads_dir)
        elif conversion_type == 'jpg to pdf':
            converter = JPGToPDFHandler()
            jpg_file = os.path.join(uploads_dir, 'file.jpg')
            pdf_file = os.path.join(uploads_dir, 'file.pdf')
            converter.jpg_to_pdf(jpg_file, pdf_file)
            return send_file(pdf_file, as_attachment=True,download_name='file.pdf')
        elif conversion_type == 'doc to pdf':
            converter = DocToPDFHandler()
            doc_file = os.path.join(uploads_dir, 'file.docx')
            pdf_file = os.path.join(uploads_dir, 'file.pdf')
            converter.doc_to_pdf(doc_file, pdf_file)
            return send_file(pdf_file, as_attachment=True, download_name='file.pdf')
        elif conversion_type == 'pdf to doc':
            converter = PDFToDocHandler()
            pdf_file = os.path.join(uploads_dir, 'file.pdf')
            doc_file = os.path.join(uploads_dir, 'file.doc')
            converter.pdf_to_doc(pdf_file, doc_file)
            return send_file(doc_file, as_attachment=True,download_name='file.doc')
    try:
        shutil.rmtree(uploads_dir)
    except Exception as e:
        print(e)
    return 'Invalid conversion type or no file was uploaded'


if __name__ == '__main__':
    app.run()
