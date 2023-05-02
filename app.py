import json

from flask import Flask, render_template, redirect, session, url_for
from auth.route import blueprint_auth
from blueprint_query.route import blueprint_query
from blueprint_report.route import blueprint_report
from unloading.route_cache import blueprint_unload

app = Flask(__name__)
app.secret_key = 'SuperKey'
app.register_blueprint(blueprint_query, url_prefix='/zaproses')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_unload, url_prefix='/unload')

app.config['db_config'] = json.load(open('data_files/dbconfig.json'))
app.config['access_config'] = json.load(open('data_files/access.json'))
app.config['cache_config'] = json.load(open('data_files/cache.json'))


@app.route('/')
@app.route('/', methods=['GET', 'POST'])
def menu_choice():
    if 'user_id' in session:
        if session.get('user_group', None):
            return render_template('internal_user_menu.html')
        else:
            return render_template('external_user_menu.html')
    else:
        return redirect(url_for('blueprint_auth.start_auth'))


@app.route('/exit')
def exit_func():
    if 'user_id' in session:
        session.clear()
    return redirect(url_for('blueprint_auth.start_auth'))


# @app.route('/reports')
# def reports():
#     return 'Coming soon'

# @app.route('/greeting/')
# @app.route('/greeting/<name>')
# def greeting_handler(name: str = None) -> str:
#     str = 'Hello, '
#     if name is None:
#          str += 'unknown'
#     else:
#         str += name
#     return str
#
#
# @app.route('/form', methods=['GET', 'POST'])
# def form_handler():
#     print(request)
#     if request.method == 'GET':
#         return render_template('form.html')
#     else:
#         login = request.form.get('login')
#         password = request.form.get('password')
#         return f'Login: {login}, Password: {password}'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)