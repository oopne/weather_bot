import sqlite3


class DBInterface:
    def __init__(self):
        self.connect = sqlite3.connect(
            'history.db', 
            check_same_thread=False
        )
        self.cursor = self.connect.cursor()

    def setup(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS history(
           time TEXT PRIMARY KEY,
           chat_id TEXT,
           text TEXT);
        ''')
        self.connect.commit()

    def add_line(self, time, chat_id, text):
        self.cursor.execute('''INSERT INTO history(time, chat_id, text)
            VALUES(?, ?, ?);''', (time, chat_id, text))
        self.connect.commit()

    def get_lines(self, chat_id):
        self.cursor.execute('''SELECT * FROM history WHERE chat_id=?''',
            (chat_id,))
        lines = self.cursor.fetchall()
        result = ''
        for line in lines:
            result += f'time: {line[0]}\n{line[2]}\n\n'
        return result

    def __del__(self):
        self.connect.close()
