import os
from flask import Blueprint, request, session, redirect, render_template
from admin import owner_only

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        key = request.form.get('key')
        if key and key == os.getenv('OWNER_KEY', 'change-me'):
            session['admin'] = {'role': 'owner'}
            return redirect('/admin')
    return '''<form method="post"><input name="key" type="password"><button>Login</button></form>'''

@admin_bp.route('/')
@owner_only
def dashboard():
    return '<h1>Li3NGa Owner Admin Console</h1><p>Owner access enabled.</p>'
