import sqlite3
from config import DB_PATH
from db import queries

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(queries.CREATE_TABLE_TASKS)
    conn.commit()
    conn.close()

def get_tasks(filter_type="all"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if filter_type == 'completed':
        cursor.execute(queries.SELECT_COMPLETED)
    elif filter_type == "incomplete":
        cursor.execute(queries.SELECT_INCOMPLETE)
    else:
        cursor.execute(queries.SELECT_TASKS)
    
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def add_task_db(task, quantity=1):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(queries.INSERT_TASK, (task, quantity, 0))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id

def update_task_db(task_id, new_task=None, quantity=None, completed=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if new_task is not None:
        cursor.execute("UPDATE tasks SET text = ? WHERE id = ?", (new_task, task_id))
    if quantity is not None:
        cursor.execute("UPDATE tasks SET quantity = ? WHERE id = ?", (quantity, task_id))
    if completed is not None:
        cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, task_id))
    
    conn.commit()
    conn.close()

def delete_task_db(task_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(queries.DELETE_TASK, (task_id,))
    conn.commit()
    conn.close()