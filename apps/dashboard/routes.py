# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.dashboard import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from flask_login import current_user

from apps.config import API_GENERATOR
from apps.models import File
from apps.authentication.models import User

@blueprint.route('/index')
@login_required
def index():
    return render_template('dashboard/index.html', segment='index', API_GENERATOR=len(API_GENERATOR))


@blueprint.route('/users.html')
@login_required
def users():
    users = User.query.all()
    print(users)
    return render_template('dashboard/users.html', segment='users', users=users, API_GENERATOR=len(API_GENERATOR))


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        print(segment)
        
        if segment == "all-files.html":
            files = File.query.all()
            return render_template("dashboard/" + template, segment=segment, files=files, API_GENERATOR=len(API_GENERATOR))
        
        # Serve the file (if exists) from app/templates/dashboard/FILE.html
        return render_template("dashboard/" + template, segment=segment, API_GENERATOR=len(API_GENERATOR))

    except TemplateNotFound:
        return render_template('dashboard/page-404.html'), 404

    except:
        return render_template('dashboard/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
