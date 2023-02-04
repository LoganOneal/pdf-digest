from flask_login import login_required, current_user
from flask import request, flash, send_file, jsonify, redirect, url_for, Response
from io import BytesIO
import json

from app.extensions import db, grobidClient
from app.models.file import File
from app.models.article import ArticleModel
from app.models.section import Section
from app.models.paragraph import Paragraph
from app.files import bp
from app.files.parsing import parse_file
from app.grobid_client.types import UNSET 


@bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        new_file = File(filename=file.filename.split('.', 1)[0], data=file.read(), user_id=current_user.id, extension = file.filename.split('.')[-1])
        db.session.add(new_file)
        db.session.commit()
        flash('File added!', category='success')
        
    return redirect(url_for('main.home'))

@bp.route('/download/<fileId>')
@login_required
def download(fileId):
    file = File.query.filter_by(id=fileId).first()
    return send_file(BytesIO(file.data), download_name=file.filename, as_attachment=True)

@bp.route('/delete', methods=['POST'])
@login_required
def delete_file():  
    file = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    fileId = file['fileId']
    file = File.query.get(fileId)

    if file:
        if file.user_id == current_user.id:
            db.session.delete(file)
            db.session.commit()

    return jsonify({})

@bp.route('/parse/<fileId>')
@login_required
def parse(fileId):
    file = File.query.filter_by(id=fileId).first()

    article = parse_file(file)

    article_model = ArticleModel(title=article.title,user_id=current_user.id)
    db.session.add(article_model)
    #db.session.commit()

    for section in article.sections:
        name = None
        num = None
        if section.name is not UNSET:
            name = section.name
        if section.num is not UNSET:
            num = section.num

        section_model = Section(name=name, num=num)
        article_model.sections.append(section_model)
        db.session.add(section_model)
        #db.session.commit()

        for paragraph in section.paragraphs:
            paragraph_model = Paragraph(text=paragraph.text)
            section_model.paragraphs.append(paragraph_model)
            db.session.add(paragraph_model)
    
        db.session.commit() 

    flash('File parsed!', category='success')
    return redirect(url_for('main.home'))

