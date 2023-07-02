# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound

from apps.home.model import Sales
from flask_socketio import emit
from sqlalchemy.sql import func
from apps import db


@blueprint.route('/index')
@login_required
def index():
    query = db.session.query(func.count(Sales.product), func.count(Sales.product).filter(Sales.status == 'Completed'))
    sales = query.first()

    return render_template('home/index.html', segment='index', sales=sales)


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None


@blueprint.route('/sales', methods=['POST'])
def add_sale():
    print(request.form)

    sale = Sales(**request.form)
    sale.save()

    query = db.session.query(func.count(Sales.product), func.count(Sales.product).filter(Sales.status == 'Completed'))
    result = query.first()
    data = {'total-sales': result[0], 'sales-completed': result[1]},
    emit('sales', data, broadcast=True, namespace='/')
    return jsonify(dict(**request.form), 200)
