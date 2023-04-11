import os

from celery.signals import task_prerun
from flask import g
from flask_login import current_user

from apps.extensions import grobid_client
import apps.grobid_client.types as grobid_types
from apps.extensions import db
from apps.factory import create_celery_app
from apps.grobid_client.api.pdf import process_fulltext_document
from apps.grobid_client.models import Article, ProcessForm
from apps.models import ArticleModel, File, Paragraph, Section

celery = create_celery_app()

BASE_TEMP_DIR = 'temp'


@celery.task()
def parse(file_id, user_id):

    file = File.query.filter_by(id=file_id).first()

    if file is None:
        return {
                   'message': 'matching record not found',
                   'success': False
               }, 404

    if file.extension != 'pdf':
        return {
                   'message': 'File format not supported',
                   'success': False
               }, 400
    
    # do something with the file
    os.makedirs(BASE_TEMP_DIR, exist_ok=True)
    pdf_file = os.path.join(BASE_TEMP_DIR, f'{file.id}.pdf')

    with open(pdf_file, "wb") as f:
        f.write(file.data)

    with open(pdf_file,"rb") as fin:
        form = ProcessForm(
            segment_sentences="0",
            input_=grobid_types.File(file_name=file.filename, payload=fin, mime_type="application/pdf"),
        )
        r = process_fulltext_document.sync_detailed(client=grobid_client, multipart_data=form)

        if r.is_success:
            article: Article = grobid_types.TEI.parse(r.content, figures=False)
            assert article.title
        else:
            print("Error: failed to parse file")

    os.remove(pdf_file)

    article_model = ArticleModel(title=article.title,user_id=user_id)
    db.session.add(article_model)

    for section in article.sections:
        name = None
        num = None
        if section.name is not grobid_types.UNSET:
            name = section.name
        if section.num is not grobid_types.UNSET:
            num = section.num

        section_model = Section(name=name, num=num)
        article_model.sections.append(section_model)
        db.session.add(section_model)

        for paragraph in section.paragraphs:
            paragraph_model = Paragraph(text=paragraph.text)
            section_model.paragraphs.append(paragraph_model)
            db.session.add(paragraph_model)
    
        db.session.commit() 




