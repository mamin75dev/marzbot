from repo.db import db


class UserRepo:
    def __init__(self):
        pass

    @classmethod
    def insert_user(cls, user_id, user_first_name, user_last_name):
        query = 'INSERT INTO users (id, first_name, last_name) VALUES (%s, %s, %s)'
        values = (user_id, user_first_name, user_last_name)
        db.insert(query, values)
