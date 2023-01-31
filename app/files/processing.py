import os
from app.models.file import File
from app.extensions import db, grobidClient

BASE_TEMP_DIR = 'temp'

def parse_file(file):
    if file.extension != 'pdf':
        print('File is not a PDF!')
        return None

    os.makedirs(BASE_TEMP_DIR, exist_ok=True)

    tmpFile = os.path.join(BASE_TEMP_DIR, f'{file.id}.pdf')
    with open(tmpFile, "wb") as f:
        f.write(file.data)

    rsp = grobidClient.serve("processFulltextDocument", tmpFile)

    os.remove(tmpFile)

    return rsp[0].text
