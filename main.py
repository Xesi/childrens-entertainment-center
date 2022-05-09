from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db, get_db_connection

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile', methods=('GET', 'POST'))
@login_required
def profile():
    conn = get_db_connection()
    events = conn.execute('SELECT *, (max_persons - COUNT(DISTINCT person)) AS free, rooms.name AS room_name FROM events e LEFT JOIN reserves ON reserves.event = e.id LEFT JOIN staff ON staff.user_id = teacher LEFT JOIN rooms ON rooms.id = room WHERE datetime(strftime(date(r_date)) || " " || strftime(time(time_end))) >= datetime("now") GROUP BY e.id ').fetchall()
    my_events = conn.execute('SELECT *, rooms.name AS room_name FROM events LEFT JOIN reserves ON event = events.id LEFT JOIN staff ON staff.user_id = teacher LEFT JOIN rooms ON rooms.id = room  WHERE datetime(strftime(date(r_date)) || " " || strftime(time(time_end))) >= datetime("now") AND (person = ? OR teacher = ?)', (current_user.id, current_user.id)).fetchall()
    # print(len(events))
    # print(len(conn.execute('SELECT * FROM events').fetchall()))
    sz = len(my_events)
    print(len(conn.execute("SELECT * from events").fetchall()))
    conn.close()
    return render_template('profile.html', user=current_user, events=events, my_events=my_events, my_events_count=sz)

