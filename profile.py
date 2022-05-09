from datetime import datetime
from time import time
from flask import Blueprint, render_template, redirect, url_for, request, flash, make_response
from sqlalchemy import Date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_required
from .models import User
from . import db, r, get_db_connection

profile = Blueprint('profile', __name__)

@profile.route('/avatar/<int:id>')
def avatar(id):
    if r.exists(current_user.id):
        logo = r.get(current_user.id)
    else:
        logo = r.get("default")
    h = make_response(logo)
    h.headers['Content-Type'] = 'image/png'
    # h.headers['Cache-Control'] = 'max-age=604800'
    return h

@profile.route('/edit_profile', methods=('GET', 'POST'))
def edit_profile():

    user = User.query.get(current_user.id)

    if request.method == 'POST':
        name = request.form['name']
        file = request.files['file']

        if not name:
            flash('name is required!')
        else:
            user.name = name
            db.session.commit()
            if file:
                r.set(user.id, file.read())
            return redirect(url_for('main.profile'))

    return render_template('edit_profile.html', user=user)


@profile.route('/edit_staff', methods=('GET', 'POST'))
def edit_staff():

    if request.method == 'POST':
        id = int(request.form['user_id'])
        admin = int(request.form['admin']) == 1
        position_id = int(request.form['position_id'])
        print("===", id, request.form['admin'], position_id)

        user = User.query.get(id)
        name = user.name
        splitted_name = name.split(' ')
        print(splitted_name)

        if not user:
            flash('user not found!')
        elif len(splitted_name) < 3:
            flash('Пользовать не корректно указал ФИО!')
        else:
            user.admin = admin
            db.session.commit()

            conn = get_db_connection()
            if len(conn.execute('SELECT * FROM staff WHERE user_id = ?', (id,)).fetchall()) > 0:
                conn.execute('UPDATE staff SET second_name = ?, first_name = ?, middle_name = ?, admin = ?, position = ?'
                         ' WHERE user_id = ?',
                         (splitted_name[0], splitted_name[1], splitted_name[2], admin, position_id, id))
            else:
                conn.execute('INSERT INTO staff (second_name, first_name, middle_name, admin, position, user_id) VALUES (?, ?, ?, ?, ?, ?)',
                         (splitted_name[0], splitted_name[1], splitted_name[2], admin, position_id, id))
            conn.commit()
            conn.close()
            db.session.commit()
            return redirect(url_for('main.profile'))
    conn = get_db_connection()
    positions = conn.execute('SELECT * FROM positions').fetchall()
    conn.close()
    return render_template('edit_staff.html', users=User.query.order_by(User.name).all(), positions=positions)


@profile.route('/staff')
def staff():
    conn = get_db_connection()
    staff = conn.execute('SELECT * FROM staff LEFT JOIN positions WHERE positions.id = position').fetchall()
    conn.close()
    return render_template('staff.html', staff=staff)


@profile.route('/clients')
def clients():
    conn = get_db_connection()
    staff = conn.execute('SELECT * FROM staff LEFT JOIN positions WHERE positions.id = position').fetchall()
    conn.close()
    return render_template('clients.html', users=User.query.order_by(User.id).all())


@profile.route('/furniture')
def furniture():
    conn = get_db_connection()
    furniture = conn.execute('SELECT * FROM furniture_and_electronics LEFT JOIN type_of_furniture WHERE type_of_furniture.furniture_id = type').fetchall()
    conn.close()
    return render_template('furniture.html', furniture=furniture)


@profile.route('/furniture-delete/<int:id>')
def furniture_delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM furniture_and_electronics WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Запись была успешно удалена!')
    return redirect(url_for('profile.furniture'))


@profile.route('/furniture-change/<int:id>', methods=('GET', 'POST'))
def furniture_change(id):
    conn = get_db_connection()
    furniture = conn.execute('SELECT * FROM furniture_and_electronics LEFT JOIN type_of_furniture ON type_of_furniture.furniture_id = type WHERE id = ?', (id,)).fetchone()
    rooms = conn.execute('SELECT * FROM rooms').fetchall()
    if request.method == 'POST':
        room_id = int(request.form['room_id'])
        conn = get_db_connection()
        conn.execute('UPDATE furniture_and_electronics SET number_of_room = ? WHERE id = ?', (room_id, id))
        conn.commit()
        conn.close()
        flash('Оборудование успешно перемещено!')
        return redirect(url_for('profile.furniture'))
    return render_template('furniture_change.html', furniture=furniture, rooms=rooms)


@profile.route('/furniture-add-type', methods=('GET', 'POST'))
def furniture_add_type():
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form['name']
        model = request.form['model']
        cost = int(request.form['cost'])
        if not name or not model or not cost:
            flash("Не все поля заполнены")
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO type_of_furniture (name, model, cost) VALUES (?, ?, ?)', (name, model, cost))
            conn.commit()
            conn.close()
            flash('Новый тип оборудования успешно добавлен!')
            return redirect(url_for('profile.furniture'))
    return render_template('furniture_add_type.html')


@profile.route('/furniture-add', methods=('GET', 'POST'))
def furniture_add():
    conn = get_db_connection()
    if request.method == 'POST':
        number_of_room = request.form['number_of_room']
        type = int(request.form['furniture_id'])
        if not number_of_room:
            flash("Комната не выбрана")
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO furniture_and_electronics (number_of_room, type) VALUES (?, ?)', (number_of_room, type))
            conn.commit()
            conn.close()
            flash('Новые оборудование успешно добавлено!')
            return redirect(url_for('profile.furniture'))
    conn = get_db_connection()
    furniture = conn.execute('SELECT * FROM type_of_furniture').fetchall()
    rooms = conn.execute('SELECT * FROM rooms').fetchall()
    conn.close()
    return render_template('furniture_add.html', rooms=rooms, furniture=furniture)


@profile.route('/create-event', methods=('GET', 'POST'))
def create_event():
    if request.method == 'POST':
        name = request.form['name']
        teacher = int(request.form['staff_id'])
        room = int(request.form['room_id'])
        r_date = datetime.strptime(request.form['r_date'],"%Y-%m-%d")
        time_start = datetime.strptime(request.form['time_start'], "%H:%M")
        time_end = datetime.strptime(request.form['time_end'], "%H:%M")
        cost = int(request.form['cost'])
        max_persons = int(request.form['max_persons'])
        print(name, teacher, room, r_date, time_start, time_end, cost, max_persons)
        conn = get_db_connection()
        conn.execute('INSERT INTO events (name, teacher, room, r_date, time_start, time_end, cost, max_persons) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
        (name, teacher, room, r_date, time_start, time_end, cost, max_persons))
        conn.commit()
        conn.close()
        flash('Новое мероприятие успешно создано!')
        return redirect(url_for('main.profile'))

    conn = get_db_connection()
    staff = conn.execute('SELECT * FROM staff LEFT JOIN positions ON position = positions.id').fetchall()
    rooms = conn.execute('SELECT r.id, r.name, r.square_of_room, types_of_room.name_of_type, types_of_room.max_count_people, CASE WHEN GROUP_CONCAT(t.name, ", ") is null THEN "отсутствует" ELSE GROUP_CONCAT(t.name, ", ") END AS fur FROM rooms r LEFT JOIN types_of_room ON type_of_room = types_of_room.id_of_type LEFT JOIN furniture_and_electronics f ON r.id = f.number_of_room LEFT JOIN type_of_furniture t ON f.type = t.furniture_id GROUP BY r.id').fetchall()
    conn.close()
    return render_template('create_event.html', staff=staff, rooms=rooms)


@profile.route('/join-event/<int:id>')
def join_event(id):
    conn = get_db_connection()
    conn.execute('INSERT INTO reserves (event, person) VALUES (?, ?)', (id, current_user.id))
    conn.commit()
    conn.close()
    flash('Вы были успешно записаны!')
    return redirect(url_for('main.profile'))

@profile.route('/delete-event/<int:id>')
def delete_event(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM events WHERE id = ?', (id,))
    conn.execute('DELETE FROM reserves WHERE event = ?', (id,))
    conn.commit()
    conn.close()
    flash('Мероприятие удалено')
    return redirect(url_for('main.profile'))

@profile.route('/cancell-event/<int:id>')
def cancell_event(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM reserves WHERE person = ? AND event = ?', (current_user.id, id))
    conn.commit()
    conn.close()
    flash('Ваша запись на мероприятие удалена')
    return redirect(url_for('main.profile'))