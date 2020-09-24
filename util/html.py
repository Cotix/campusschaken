from flask import render_template
from flask_login import current_user

from config import *
from jinja2 import Environment, FileSystemLoader, select_autoescape


def ok(view, data={}, **args):
    options = {
        'status': 200,
    }
    options.update(args)

    data.update({
        'current_user': current_user
    })

    body = render_template('%s.html.j2' % view, **data)

    res = Response(body, status=options['status'], mimetype='text/html')
    return res


def error(title, text='', description=False, errno=401):
    res = ok('error', {
        'title': title,
        'text': text,
        'description': description
    }, status=errno)
    return res
