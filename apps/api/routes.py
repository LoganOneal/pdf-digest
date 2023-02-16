from flask import request, send_file, redirect, url_for
from flask_restx import Api, Resource
from io import BytesIO

from apps.authentication.decorators import token_required
from flask_login import current_user

from apps.api import blueprint
from apps.api.util import parse as parse_util
from apps.models    import *
from apps.grobid_client.types import UNSET 

api = Api(blueprint)

@api.route('/file/', methods=['POST', 'GET', 'DELETE'])
@api.route('/file/<int:model_id>/', methods=['GET', 'DELETE'])
class FileRoute(Resource):

    ALLOWED_EXTENSIONS = set(['pdf'])

    def allowed_file(self,filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS
    
    @token_required
    def get(self, model_id: int = None):
        if model_id is None:
            return {
                        'message': 'No file selected for deletion',
                        'success': False
                    }, 400
        else:
            obj = File.query.get(model_id)
            if obj is None:
                return {
                           'message': 'matching record not found',
                           'success': False
                       }, 404
            return send_file(BytesIO(obj.data), download_name=obj.filename, as_attachment=True)
    
    @token_required
    def post(self):
            print("AAAAAAA")
            print(current_user.is_authenticated)
            print(current_user.get_id())
            file = request.files['file']
            if file.filename == '':
                print("No file selected for uploading")
                return {
                           'message': 'No file selected for uploading',
                           'success': False
                        }, 400

            if file and self.allowed_file(file.filename):
                new_file = File(filename=file.filename.split('.', 1)[0], 
                              data=file.read(), 
                              extension = file.filename.split('.')[-1],
                              user_id=current_user.get_id(), 
                              )
                db.session.add(new_file)
                db.session.commit()
                return {
                'message': 'File successfully uploaded',
                'success': True
                }, 201
            else:
                print("Allowed file types are pdf")
                return {
                'message': 'Allowed file types are pdf',
                'success': False
                        }, 400

    @token_required
    def delete(self, model_id: int):
        to_delete = File.query.filter_by(id=model_id)
        if to_delete.count() == 0:
            return {
                       'message': 'matching record not found',
                       'success': False
                   }, 404
        to_delete.delete()
        File.query.session.commit()
        return {
                   'message': 'record deleted!',
                   'success': True
               }, 200

@blueprint.route('/file/parse/<int:file_id>/')
async def parse(file_id):
    file = File.query.filter_by(id=file_id).first()

    article = await parse_util(file)

    article_model = ArticleModel(title=article.title,user_id=current_user.get_id())
    db.session.add(article_model)

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

        for paragraph in section.paragraphs:
            paragraph_model = Paragraph(text=paragraph.text)
            section_model.paragraphs.append(paragraph_model)
            db.session.add(paragraph_model)
    
        db.session.commit() 

    return "Done!"

@blueprint.route('/file/summarize/<articleID>')
async def summarize(articleID):
    article = ArticleModel.query.filter_by(id=articleID).first()


    paragraphs = Section.query.filter_by(id=5).first().paragraphs

    text = ""

    for par in paragraphs:
        text += par.text

    print("TEXT: ", text)


    summary = bart_summarize(text, 100)

    print("SUMMARY: ", summary)


    flash('File summarized!', category='success')
    return redirect(url_for('main.dashboard'))

