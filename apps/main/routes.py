# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.main import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound

from apps.config import API_GENERATOR
from apps.models import File

@blueprint.route('/index')
@login_required
def index():
    return render_template('main/index.html', segment='index')

@blueprint.route('/file-upload')
@login_required
def file_upload():
    return render_template('main/file-upload.html', segment='file-upload')

@blueprint.route('/my-files')
@login_required
def my_files():
    files = File.query.all()
    return render_template('main/my-files.html', files=files, segment='my-files')

@blueprint.route('/pdf-explore')
@login_required
def pdf_explore():
    return render_template('main/pdf-explore.html', segment='pdf-explore')

@blueprint.route('/wizard')
@login_required
def wizard():
    return render_template('main/wizard.html', segment='wizard')

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/dashboard/FILE.html
        return render_template("main/" + template, segment=segment, API_GENERATOR=len(API_GENERATOR))

    except TemplateNotFound:
        return render_template('shared/page-404.html'), 404

    except:
        return render_template('shared/page-500.html'), 500
    


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
