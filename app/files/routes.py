from flask_login import login_required, current_user
from flask import request, flash, send_file, jsonify, redirect, url_for, Response
from io import BytesIO
import json
import os 

from app.extensions import db, grobidClient
from app.models.file import File
from app.files import bp
from app.files.processing import parse_file


@bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        new_file = File(filename=file.filename, data=file.read(), user_id=current_user.id, extension = file.filename.split('.')[-1])
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

    parsed_xml = parse_file(file)

    #return send_file(parse_file, download_name=file.filename, as_attachment=True)

    return Response(parsed_xml, mimetype='text/xml')
