import os
from app.models.file import File
from app.extensions import grobidClient
from grobid_client.api.pdf import process_fulltext_document
from grobid_client.models import Article, ProcessForm
from grobid_client.types import TEI, File

BASE_TEMP_DIR = 'temp'

def etree_iter_path(node, tag=None, path='.'):
    if tag == "*":
        tag = None
    if tag is None or node.tag == tag:
        yield node, path
    for child in node:
        _child_path = '%s/%s' % (path, child.tag)
        for child, child_path in etree_iter_path(child, tag, path=_child_path):
            yield child, child_path

def remove_namespace(doc, namespace):
    """Remove namespace in the passed document in place."""
    ns = u'{%s}' % namespace
    nsl = len(ns)
    for elem in doc.iter():
        if elem.tag.startswith(ns):
            elem.tag = elem.tag[nsl:]


def parse_file(file):
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
        r = process_fulltext_document.sync_detailed(client=grobidClient, multipart_data=form)

        if r.is_success:
            article: Article = TEI.parse(r.content, figures=False)
            assert article.title
        else:
            print("Error: failed to parse file")

    os.remove(pdf_file)

    return article
