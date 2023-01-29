from flask_login import login_required, current_user
from flask import render_template, request, flash, send_file, jsonify, redirect, url_for
from io import BytesIO
import json

from app.extensions import db
from app.models.file import File
from app.files import bp

@bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        new_file = File(filename=file.filename, data=file.read(), user_id=current_user.id)
        db.session.add(new_file)
        db.session.commit()
        flash('File added!', category='success')
        
    return redirect(url_for('main.home'))

@bp.route('/download/<file_id>')
@login_required
def download(upload_id):
    file = File.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(file.data),
                     download_name=file.filename, as_attachment=True)

@bp.route('/delete-file', methods=['POST'])
def delete_file():  
    file = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    fileId = file['fileId']
    file = File.query.get(fileId)
    if file:
        if file.user_id == current_user.id:
            db.session.delete(file)
            db.session.commit()

    return jsonify({})