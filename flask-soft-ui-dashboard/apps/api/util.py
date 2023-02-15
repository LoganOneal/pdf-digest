import os
from apps.models import File
from apps import grobid_client
from apps.grobid_client.api.pdf import process_fulltext_document
from apps.grobid_client.models import Article, ProcessForm
from apps.grobid_client.types import TEI, File

BASE_TEMP_DIR = 'temp'


async def parse(file) -> Article:
    if file.extension != 'pdf':
        print('File is not a PDF!')
        return None

    os.makedirs(BASE_TEMP_DIR, exist_ok=True)
    pdf_file = os.path.join(BASE_TEMP_DIR, f'{file.id}.pdf')

    with open(pdf_file, "wb") as f:
        f.write(file.data)

    with open(pdf_file,"rb") as fin:
        form = ProcessForm(
            segment_sentences="0",
            input_=File(file_name=file.filename, payload=fin, mime_type="application/pdf"),
        )
        r = process_fulltext_document.sync_detailed(client=grobid_client, multipart_data=form)

        if r.is_success:
            article: Article = TEI.parse(r.content, figures=False)
            assert article.title
        else:
            print("Error: failed to parse file")

    os.remove(pdf_file)

    return article
