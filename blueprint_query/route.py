import os.path
from flask import Blueprint, request, render_template, current_app
from db_work import select
from sql_provider import SQLProvider
from access import login_required, group_required


blueprint_query = Blueprint('bp_query', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route('/queries', methods=['GET', 'POST'])
@group_required
def queries():
    return render_template('query_menu.html')


#Первый запрос вывод информации о регистрации кораблей за один месяц
@blueprint_query.route('/query1', methods=['GET', 'POST'])
@group_required
def query1():
    columns = ['Номер регистрации', 'Дата прибытия', 'Дата отбытия', 'Номер сотрудника', 'Номер корабля',
               'Номер причала', 'Дата разгрузки']
    if request.method == 'GET':
        return render_template('query1_form.html')
    else:
        input_month = request.form.get('month_reg')
        input_year = request.form.get('year_reg')
        if input_month and input_year and (int(input_month)<13 and int(input_month)>0):
            _sql = provider.get('query1.sql', input_month=input_month, input_year=input_year)
            reg_result, schema = select(current_app.config['db_config'], _sql)
            print(reg_result)
            return render_template('db_result.html', schema=columns, result=reg_result, title_result = 'Регистрации кораблей за один месяц')
        else:
            return render_template('query1_form.html', message = 'Пожалуйста, повторите ввод')


#Второй запрос вывод информации о количестве регистраций каждого корабля  за период
@blueprint_query.route('/query2', methods=['GET', 'POST'])
@group_required
def query2():
    columns = ['Номер судна', 'Имя судна', 'Количество регистраций']
    if request.method == 'GET':
        return render_template('query2_form.html')
    else:
        input_start = request.form.get('start_date')
        input_end = request.form.get('end_date')
        if input_start and input_end:
            _sql = provider.get('query2.sql', input_start=input_start, input_end=input_end)
            q2_result, schema = select(current_app.config['db_config'], _sql)
            return render_template('db_result.html', schema=columns, result=q2_result, title_result = 'Количество регистраций каждого корабля за период')
        else:
            return render_template('query2_form.html', message = 'Пожалуйста, повторите ввод')


#Третий запрос
@blueprint_query.route('/query3', methods=['GET', 'POST'])
@group_required
def query3():
    columns = ['Номер сотрудника', 'Имя сотрудника', 'Количество разгрузок', 'Количество часов']
    if request.method == 'GET':
        return render_template('query3_form.html')
    else:
        input_start = request.form.get('start_date')
        input_end = request.form.get('end_date')
        if input_start and input_end:
            _sql = provider.get('query3.sql', input_start=input_start, input_end=input_end)
            q3_result, schema = select(current_app.config['db_config'], _sql)
            return render_template('db_result.html', schema=columns, result=q3_result,  title_result = 'Количество отработанных разгрузок за период')
        else:
            return render_template('query3_form.html', message = 'Пожалуйста, повторите ввод')