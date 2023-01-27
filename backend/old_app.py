import os
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory
from io import BytesIO
from PyPDF2 import PdfReader
from grobid_client.grobid_client import GrobidClient
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_EXTENSIONS'] = ['.pdf']

client = GrobidClient(config_path="./config.json")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/count_words', methods=['POST'])
def count_words():
    pdf_file = request.files['pdf_file']
    pdf_reader = PdfReader(BytesIO(pdf_file.read()))
    num_pages = len(pdf_reader.pages)
    count = 0
    for i in range(num_pages):
        page = pdf_reader.pages[i]
        count += len(page.extract_text().split())
    return f'Number of words in PDF: {count}'

@app.route('/upload_file', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    return redirect(url_for('uploaded_file', filename=filename))



@app.route('/parse_pdf', methods=['POST'])
def parse_pdf():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(filename)
        file_path = app.config['UPLOAD_FOLDER'] + '/' + filename
        print(file_path)
        file.save(file_path)
        #return redirect(url_for('uploaded_file', filename=filename))

    print(client.process("processFulltextDocument", file_path, output="./processed/test_out/", consolidate_citations=True, tei_coordinates=True, force=False))

    return 'document processed!'


if __name__ == '__main__':
    app.run(debug=True)