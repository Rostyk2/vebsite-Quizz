import sqlite3

class SQLManager:
    def __init__(self, name):
        self.db = sqlite3.connect(name)
        self.create_tables()

    def create_tables(self):
        cursor = self.db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Quizz (
                quizz_id INTEGER PRIMARY KEY,
                quizz_name TEXT NOT NULL,
                description TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Questions (
                question_id INTEGER PRIMARY KEY,
                quiz_id INTEGER,
                content TEXT,
                FOREIGN KEY (quiz_id) REFERENCES Quizz(quizz_id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Options (
                option_id INTEGER PRIMARY KEY,
                question_id INTEGER,
                content TEXT,
                is_correct BOOLEAN,
                FOREIGN KEY (question_id) REFERENCES Questions(question_id)
            )
        ''')
        cursor.close()
        self.db.commit()

    def add_quizz(self, quizz_name, description):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO Quizz(quizz_name, description) VALUES(?, ?)", [quizz_name, description])
        self.db.commit()
        return cursor.lastrowid

    def add_quest(self, quiz_id, content):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO Questions(quiz_id, content) VALUES(?, ?)", [quiz_id, content])
        self.db.commit()
        return cursor.lastrowid

    def add_answer(self, question_id, content, is_correct):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO Options(question_id, content, is_correct) VALUES(?, ?, ?)", [question_id, content, is_correct])
        self.db.commit()
        return cursor.lastrowid

    def select_answer(self, question_id):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM Options WHERE question_id = ?", [question_id])
        records = cursor.fetchall()
        cursor.close()
        return records

    def select_questions(self, quiz_id):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM Questions WHERE quiz_id = ?", [quiz_id])
        records = cursor.fetchall()
        cursor.close()
        return records

    def select_quizzes(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM Quizz")
        records = cursor.fetchall()
        cursor.close()
        return records
