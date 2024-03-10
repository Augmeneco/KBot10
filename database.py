import sqlite3
import json

db = sqlite3.connect('data/db.db', check_same_thread=False)
db_cur = db.cursor()

db_cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER, data TEXT)')

class User:
    id: int
    level: int
    data: dict

    def update(self):
        users.update(self.id)

class Users:
    users = {}

    def __init__(self):
        users = db_cur.execute('SELECT * FROM users').fetchall()
        for user in users:
            id = user[0]
            data = json.loads(user[1])
            level = data['level']

            self.users[id] = {
                'level': level,
                'data': data
            }

    def get(self, id):
        if id not in self.users:
            self.add(id)

        user = User()
        user.id = id
        user.data = self.users[id]['data']
        user.level = self.users[id]['level']

        return user

    def add(self, id):
        self.users[id] = {
            'level': 1,
            'data': {'level':1}
        }

        db_cur.execute('INSERT INTO users VALUES (?, ?)', (id, json.dumps(self.users[id]['data']) ))
        db.commit()

        return self.get(id)
    
    def update(self, id):
        data = self.users[id]['data']
        data['level'] = self.users[id]['level']
        data = json.dumps(data)

        db_cur.execute('UPDATE users SET data = ? WHERE id = ?', (data, id))
        db.commit()

    def exists(self, id):
        if id in self.users: return True
        else: False
        
users = Users()