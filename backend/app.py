from flask import Flask, request
from io import BytesIO
from PyPDF2 import PdfReader

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)