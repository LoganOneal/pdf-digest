from flask import jsonify, request, send_file, redirect, url_for
from flask_restx import Api, Resource
from io import BytesIO

from apps.authentication.decorators import token_required
from flask_login import current_user

from apps.api import blueprint
from apps.models    import *
from apps.grobid_client.types import UNSET
from apps.tasks import parse_task, send_async_email 

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
                #await parse(new_file.id)
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
    

@blueprint.route('/parse/<int:file_id>')
def parse(file_id):

    task = parse_task.apply_async(args=[file_id])
    #task = send_async_email.apply_async()

    print( url_for('api_blueprint.taskstatus', task_id=task.id))

    return jsonify({'Location': url_for('api_blueprint.taskstatus',
                                                  task_id=task.id)}), 202, {'Location': url_for('api_blueprint.taskstatus',
                                                  task_id=task.id)}

@blueprint.route('/status/<task_id>')
def taskstatus(task_id):
    task = parse_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)

