import os.path

from flask import Blueprint, request, render_template, current_app, redirect, session, url_for

from access import login_required, group_required
from db_work import select_dict,  call_proc, select
from sql_provider import SQLProvider
from db_context_manager import DBConnection

blueprint_unload = Blueprint('bp_unload', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_unload.route('/', methods=['GET', 'POST'])
def unload_index():
    db_config = current_app.config['db_config']
    if request.method == 'GET':
        sql = provider.get('ships.sql')
        ships = select_dict(db_config, sql)
        print(ships)
        return render_template('start_unload.html', ships= ships)
    else:
        date_un = request.form.get('date_un')
        print(date_un)
        reg_id = request.form.get('ship')
        print(reg_id)  #Добавить проверку на корректную дату???
        sql = provider.get('workers.sql', date_un=date_un)
        session['date_un'] = date_un
        session['reg_id'] = reg_id
        workers = select_dict(db_config, sql) #сделать новый sql который достает только нужные item
        print(workers)
        unloading_workers = session.get('unloading', {})
        return redirect(url_for('bp_unload.unload_list'))


@blueprint_unload.route('/list', methods=['GET', 'POST'])
def unload_list():
    date_un = session.get('date_un')
    print(date_un)
    #reg_id = session.get('reg_id')
    db_config = current_app.config['db_config']
    if request.method == 'GET':
        sql = provider.get('workers.sql', date_un=date_un)
        workers = select_dict(db_config, sql)
        print(workers)
        unloading_workers = session.get('unloading', {})
        return render_template('unloading_list.html', workers=workers, unloading=unloading_workers)
    else:
        emp_id = request.form.get('emp_id')
        print(emp_id)
        sql = provider.get('select_emp.sql', emp_id=emp_id)
        worker = select_dict(db_config, sql)  # сделать новый sql который достает только нужные item
        print(worker)
        add_unload(emp_id, worker)
        return redirect(url_for('bp_unload.unload_list'))


def add_unload(emp_id, workers: dict):
    # item_description = [item for item in items if str(item['prod_id']) == str(prod_id)]
    # print('Item_description before = ', item_description)
    # item_description = item_description[0]
    curr_unloading = session.get('unloading', {})
    print('curr = ', curr_unloading)
    print('workers = ', workers)
    if emp_id in curr_unloading:
        pass
    else:
        curr_unloading[emp_id] = {
            'name': workers[0]['name'],
            'prof': workers[0]['prof']
        }
        session['unloading'] = curr_unloading
        session.permanent = True
    return True


@blueprint_unload.route('/save_team', methods = ['GET', 'POSt'])
def save_team():
    if 'unloading' not in session:
        return render_template('empty.html')
    else:
        date_un = session.get('date_un')
        reg_id = session.get('reg_id')
        current_unloading = session.get('unloading', {})
        # print(0)
        team_id = save_team_with_list(current_app.config['db_config'], reg_id, date_un, current_unloading)
        if team_id:
            call_proc(current_app.config['db_config'], 'fill_card', team_id)
            session.pop('unloading')
            session.pop('date_un')
            session.pop('reg_id')
            return render_template('team_created.html')
        else:
            return 'Error...'


def save_team_with_list(dbconfig:dict, reg_id: int, date_un, current_unloading:dict):
    with DBConnection(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        #print(1)
        print(date_un)
        print(reg_id)
        _sql1 = provider.get('add_undate.sql', date_un=date_un, reg_id=reg_id)
        result1 = cursor.execute(_sql1)
        print("res1 = ", result1)
        _sql2 = provider.get('insert_un.sql', date_un=date_un, reg_id=reg_id, hours=8)
        print(_sql2)
        result2 = cursor.execute(_sql2)
        print("res2 = ",result2)
        if result2:
            _sql2 = provider.get('select_un_id.sql', date_un=date_un, reg_id=reg_id)
            cursor.execute(_sql2)
            unload_id = cursor.fetchall()[0][0]
            print('unload_id = ', unload_id)
            print(current_unloading)
            if unload_id:
                for key in current_unloading:
                    print(key)
                    _sql3 = provider.get('insert_team.sql', id_un=unload_id, id_em=key)
                    cursor.execute(_sql3)
                return unload_id


@blueprint_unload.route('/clear-unload')
def clear_unload():
    if 'unloading' in session:
        session.pop('unloading')
    return redirect(url_for('bp_unload.unload_list'))


@blueprint_unload.route('/timetable')
def timetable():
    user_id = session['user_id']
    db_config = current_app.config['db_config']
    _sql = provider.get('timetable.sql', user_id=user_id)
    result, schema = select(db_config, _sql)
    schema = ['Номер разгрузки','Дата разгрузки','Номер регистрации',  'Название корабля']
    return render_template('timetable.html', schema=schema, result=result)
