import mysql.connector


class Database:
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306
        self.database = 'cactusbot'
        self.user = 'root'
        self.password = 'Mohamad1375'

        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        self.cursor = self.connection.cursor(dictionary=True)

    def select(self, query):
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        return data

    def insert(self, query, data):
        self.cursor.execute(query, data)
        self.connection.commit()


db = Database()
