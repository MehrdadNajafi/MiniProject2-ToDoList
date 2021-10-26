import sqlite3

con = sqlite3.connect('database.db')
my_cursor = con.cursor()

def add(id, title, description, done, time, date, priority):
    my_cursor.execute(f'INSERT INTO tasks (id, title, description, done, time, date, priority) VALUES ({id}, "{title}", "{description}", {done}, "{time}", "{date}", {priority})')
    con.commit()

def getAll():
    my_cursor.execute('SELECT * FROM tasks')
    results = my_cursor.fetchall()
    return results

def deleteTask(id):
    my_cursor.execute(f'DELETE FROM tasks WHERE id = {id}')
    con.commit()

def editDone(id, value):
    my_cursor.execute(f'UPDATE tasks SET done = {value} WHERE id = {id}')
    con.commit()