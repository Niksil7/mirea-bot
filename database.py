import sqlite3


class DataBase:
    def __init__(self, filename):
        self.con = sqlite3.connect(filename)
        self.cur = self.con.cursor()

    async def add_user(self, user_id, language, action):
        try:
            self.cur.execute("INSERT INTO users VALUES(?, ?, ?)", (user_id, language, action))
            self.con.commit()
        except:
            pass

    async def get_language(self, user_id):
        self.cur.execute("SELECT language FROM users WHERE user_id=?", (user_id, ))
        try:
            return self.cur.fetchall()[0][0]
        except:
            return None

    async def set_language(self, user_id, language):
        self.cur.execute("UPDATE users SET language=? WHERE user_id=?", (language, user_id))
        self.con.commit()

    async def set_action(self, user_id, action):
        self.cur.execute("UPDATE users SET action=? WHERE user_id=?", (action, user_id))
        self.con.commit()

    async def get_action(self, user_id):
        self.cur.execute("SELECT action FROM users WHERE user_id=?", (user_id,))
        try:
            return self.cur.fetchall()[0][0]
        except:
            return None
