import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        print("The database is connected successfully")

    def add_client(self, ID):
        with self.connection:
            try:
                self.cursor.execute("INSERT INTO 'client_data' VALUES (?)", (ID,))
            except: pass

    def add_check(self, user_id, bill_id):
        with self.connection:
            self.cursor.execute("INSERT INTO 'check' ('user_id', 'bill_id') VALUES (?, ?)", (user_id, bill_id,))

    def get_check(self, bill_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM 'check' WHERE bill_id = ?", (bill_id,)).fetchmany(1)
            if not bool(len(result)):
                return False
            return result[0]

    def delete_check(self, bill_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM 'check' WHERE bill_id = ?", (bill_id,))

    def get_description(self, id, difficulty):
        with self.connection:
            return self.cursor.execute("SELECT description FROM 'scheme' WHERE id = ? AND difficulty = ?", (id, difficulty, )).fetchone()[0]

    def get_link(self, id, difficulty):
        with self.connection:
            return self.cursor.execute("SELECT link FROM 'scheme' WHERE id = ? AND difficulty = ?", (id, difficulty,)).fetchone()[0]

    def get_price(self, id, difficulty):
        with self.connection:
            return self.cursor.execute("SELECT price FROM 'scheme' WHERE id = ? AND difficulty = ?", (id, difficulty,)).fetchone()[0]

    def get_users(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM client_data").fetchall()

    def add_scheme(self, id, price, difficulty, description, link):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'scheme' ('id', 'price', 'difficulty', 'description', 'link') VALUES (?, ?, ?, ?, ?)", (id, price, difficulty, description, link,))

    def get_scheme_amount(self, difficulty):
        with self.connection:
            return len(self.cursor.execute("SELECT * FROM 'scheme' WHERE difficulty = ?", (difficulty,)).fetchall())

    def exist_scheme(self, id, difficulty):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM 'scheme' WHERE id = ? AND difficulty = ?", (id, difficulty,)).fetchmany(1)
        if not bool(len(result)):
            return False
        return True