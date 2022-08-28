import sqlite3
conn = sqlite3.connect('players.db') 
c = conn.cursor()

def table_exists(table_name): 
    c.execute('''SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = '{}' '''.format(table_name)) 
    if c.fetchone()[0] == 1: 
        return True 
    return False

if not table_exists('users'): 
    c.execute(''' 
        CREATE TABLE users( 
            user_id BIGINT, 
            user_name TEXT, 
            score INTEGER, 
            level TEXT, 
            time_in_channel DATETIME 
        ) 
    ''')


def create_user(user_id, user_name, score = 0, level = 'silver', time_in_channel = None): 
    c.execute(''' INSERT INTO users (user_id, user_name, score, level, time_in_channel) VALUES(?, ?, ?, ?, ?) ''', (user_id, user_name, score, level, time_in_channel)) 
    conn.commit()

def get__all_users(): 
    c.execute('''SELECT * FROM users''') 
    data = [] 
    for row in c.fetchall(): 
        data.append(row) 
    return data

def get_user(user_id): 
    c.execute('''SELECT * FROM users WHERE user_id = {}'''.format(user_id)) 
    data = [] 
    for row in c.fetchall():  
        data.append(row) 
    return data

def update_user(user_id, update_dict): 
    valid_keys = ['user_name', 'score', 'level', 'time_in_channel'] 
    for key in update_dict.keys():  
        if key not in valid_keys: 
            raise Exception('Invalid field name!') 
    for key in update_dict.keys(): 
        if type(update_dict[key]) == str: 
            stmt = '''UPDATE users SET {} = '{}' WHERE user_id = {}'''.format(key, update_dict[key], user_id) 
        else: 
            stmt = '''UPDATE users SET {} = '{}' WHERE user_id = {}'''.format(key, update_dict[key], user_id) 
        c.execute(stmt) 
    conn.commit()

def delete_user(user_id): 
    c.execute('''DELETE FROM users WHERE user_id = {}'''.format(user_id)) 
    conn.commit()