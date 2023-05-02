import os.path
from flask import Blueprint, request, render_template, current_app, redirect, url_for
from access import login_required, group_required
from db_work import select, call_proc
from sql_provider import SQLProvider
#отчеты - это агрегированные данные, которые сохраняются в базе данных в отдельных таблицах, накапливаются там и постепенно начинают мешать поддерживать процессы

blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

report_list = [{'rep_name': 'Отчет о регистрациях кораблей за месяц', 'rep_id': '1'},
               {'rep_name': 'Отчет  о разгрузках за месяц', 'rep_id': '2'},
               {'rep_name': 'Отчет Отчёт регистрациях кораблей в каждом порту за заданный год', 'rep_id': '3'},
               ]
report_url = {'1': {'create_rep': 'bp_report.create_rep1', 'view_rep': 'bp_report.view_rep1'},
              '2': {'create_rep': 'bp_report.create_rep2', 'view_rep': 'bp_report.view_rep2'},
              '3': {'create_rep': 'bp_report.create_rep3', 'view_rep': 'bp_report.view_rep3'}}


@blueprint_report.route('/',methods=['GET', 'POST'])
@group_required
def start_report():
    if request.method == 'GET':
        print('get')
        return render_template('menu_report.html', report_list = report_list)
    else:
        print('post')
        rep_id = request.form.get('rep_id')
        print('rep_id=', rep_id )
        if request.form.get('create_rep'):
            url_rep = report_url[rep_id]['create_rep']
        else:
            url_rep = report_url[rep_id]['view_rep']
        print('url_rep= ', url_rep)
    return redirect(url_for(url_rep))


@blueprint_report.route('/create_rep1', methods=['GET', 'POST'])
@group_required
def create_rep1():
    if request.method == 'GET':
        print("GET_create")
        return render_template('report_create.html')
    else:
        print('1111111111111111111111111')
        print("POST_create")
        rep_month = request.form.get('input_month')
        rep_year = request.form.get('input_year')
        print("Loading...")
        if rep_year and rep_month and int(rep_month)<13 and int(rep_month)>0 and int(rep_year)>0:
            _sql = provider.get('ch1.sql', in_month=rep_month, in_year=rep_year)
            check = select(current_app.config['db_config'], _sql)[0]
            print(_sql)
            print(check)
            print('checkreport = ', check)
            if (len(check)!=0):
                _sql = provider.get('check_rep.sql', in_month=rep_month, in_year = rep_year)
                check = select(current_app.config['db_config'], _sql)[0][0][0]
                print('checkreport = ' ,check)
                if (check == 0):

                    res = call_proc(current_app.config['db_config'], 'reg_report',  rep_month, rep_year)

                    return render_template('report_created.html')
                else:
                    return render_template('report_create.html', message ="Такой отчет уже существует")
            else:
                return render_template('report_create.html', message="Нет данных для создания отчета")
        else:
            return render_template('report_create.html', message ="Повторите ввод" )

    # rep_month = 9
    # rep_year = 2022
    # res = call_proc(current_app.config['db_config'], 'product_report', rep_month, rep_year) #надо чтоб была процедура
    # print('res= ', res)
    # return render_template('report_created.html')


@blueprint_report.route('/view_rep1', methods=['GET', 'POST'])
@group_required
def view_rep1():
    columns = ['№ отчета', '№ причала', 'Количество зарегистрированных кораблей', 'Месяц регистрации', 'Год регистрации']
    #columns = ['№ отчета', '№ регистрации', '№ корабля', 'имя корабля','дата прибытия', 'дата отбытия','название причала']
    if request.method == 'GET':
        return render_template('view_rep.html', name = 'Просмотр отчета о регистрациях кораблей за месяц')
    else:
        rep_month = request.form.get('input_month')
        rep_year = request.form.get('input_year')
        print(rep_year, rep_month)

        if rep_year and rep_month and int(rep_month)<13 and int(rep_month)>0 and int(rep_year)>0:
            _sql = provider.get('rep1.sql', in_year=rep_year, in_month = rep_month)
            result, schema = select(current_app.config['db_config'], _sql)
            if len(result)==0:
                return render_template('view_rep.html', name='Просмотр отчета о регистрациях кораблей за месяц',
                                       message='Такого отчета нет')
            else:
                return render_template('result_rep1.html', month=rep_month, year = rep_year, schema = columns, result = result)
        else:
            return render_template('view_rep.html', name = 'Просмотр отчета о регистрациях кораблей за месяц', message = 'Повторите ввод')

@blueprint_report.route('/create_rep2', methods=['GET', 'POST'])
@group_required
def create_rep2():
    if request.method == 'GET':
        print("GET_create")
        return render_template('report_create.html')
    else:
        print('1111111111111111222222222222222222111111111')

        print("POST_create")
        rep_month = request.form.get('input_month')
        rep_year = request.form.get('input_year')
        print("Loading...")
        if rep_year and rep_month and int(rep_month)<13 and int(rep_month)>0 and int(rep_year)>0:
            _sql = provider.get('ch2.sql', in_month=rep_month, in_year=rep_year)
            check = select(current_app.config['db_config'], _sql)[0]
            print(check)
            print('checkreport = ', check)
            if (len(check)!=0):
                _sql = provider.get('check_rep2.sql', in_month=rep_month, in_year = rep_year)
                check = select(current_app.config['db_config'], _sql)[0][0][0]
                print('checkreport = ' ,check)
                if (check == 0):
                    res = call_proc(current_app.config['db_config'], 'reg_report',  rep_month, rep_year)
                    return render_template('report_created.html')
                else:
                    return render_template('report_create.html', message ="Такой отчет уже существует")
            else:
                return render_template('report_create.html', message="Такого отчета нет в базе данных")
        else:
            return render_template('report_create.html', message ="Повторите ввод" )

    # rep_month = 9
    # rep_year = 2022
    # res = call_proc(current_app.config['db_config'], 'product_report', rep_month, rep_year) #надо чтоб была процедура
    # print('res= ', res)
    # return render_template('report_created.html')


@blueprint_report.route('/view_rep2', methods=['GET', 'POST'])
@group_required
def view_rep2():
    columns = ['№ отчета', '№ работника', 'Количество часов','Месяц разгрузки', 'Год разгрузки']
    #columns = ['№ отчета', '№ разгрузки', 'дата разгрузки','№ регистрации', 'имя корабля','количество рабочих']
    if request.method == 'GET':
        return render_template('view_rep.html', name = 'Просмотр отчета о разгрузках за месяц')
    else:
        rep_month = request.form.get('input_month')
        rep_year = request.form.get('input_year')
        print(rep_year, rep_month)
        if rep_year and rep_month:
            _sql = provider.get('rep2.sql', in_year=rep_year, in_month = rep_month)
            print(_sql)
            result, schema = select(current_app.config['db_config'], _sql)
            print(result)
            if(len(result)==0):
                return render_template('view_rep.html', name='Просмотр отчета о разгрузках за месяц',
                                       message='Такого отчета нет в базе данных')
            else:
                return render_template('result_rep2.html', month=rep_month, year = rep_year, schema = columns, result = result)
        else:
            return render_template('view_rep.html', name = 'Просмотр отчета о разгрузках за месяц', message = 'Повторите ввод')

@blueprint_report.route('/create_rep3', methods=['GET', 'POST'])
@group_required
def create_rep3():
    if request.method == 'GET':
        print("GET_create")
        return render_template('report_create.html')
    else:
        #print(current_app.config['dbconfig'])
        print('1111111111333333333333333333331111111')

        print("POST_create")
        rep_month = request.form.get('input_month')
        rep_year = request.form.get('input_year')

        print("Loading...")
        if rep_year and rep_month:
            _sql = provider.get('re2.sql', in_year=rep_year, in_month=rep_month)
            product_result, schema = select(current_app.config['db_config'], _sql)
            if product_result:
                return "Такой отчёт уже существует"
            else:
                res = call_proc(current_app.config['db_config'], 'reg_report', rep_month, rep_year)
                print('res=', res)
                return render_template('report_created.html')
        else:
            return "Repeat input"


@blueprint_report.route('/view_rep3', methods=['GET', 'POST'])
@group_required
def view_rep3():
    if request.method == 'GET':
        return render_template('view_rep.html')
    else:
        rep_month = request.form.get('input_month')
        rep_year = request.form.get('input_year')
        print(rep_month, rep_year)
        if rep_year and rep_month:
            _sql = provider.get('re2.sql', in_month=rep_month, in_year=rep_year)
            product_result, schema = select(current_app.config['db_config'], _sql)
            print(product_result)
            print(schema)
            print('12112121212')
            if product_result:
                return render_template('result_rep2.html', schema=["№ регистрации", "ID порта", "Кол-во кораблей, зарегистрированных в этом порту","Месяц регистрации", "Год регистрации"], result=product_result)
            else:
                return "Такой отчёт не был создан"
        else:
            return "Repeat input"

