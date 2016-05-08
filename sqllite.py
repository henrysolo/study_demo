import sqlite3

conn = sqlite3.connect('test.db')
print "Opened database successfully";
try:
    cursor = conn.execute("SELECT id, name, address, salary  from COMPANY")
    for row in cursor:
        print "ID = ", row[0]
        print "NAME = ", row[1]
        print "ADDRESS = ", row[2]
        print "SALARY = ", row[3], "\n"
except sqlite3.OperationalError:
    print "Table created successfully"

conn.commit()
print "Records created successfully"
conn.close()


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('test.db')

    def insert(self):
        try:
            result = conn.execute("INSERT INTO username, password,status from users")
        except sqlite3.OperationalError:
            self.create_table()
            self.insert()
        return result

    def select(self):
        try:
            result = conn.execute("SELECT username, password from users")
        except sqlite3.OperationalError:
            self.create_table()
            self.select()
        return result

    def delete(self):
        try:
            result = conn.execute("delete from users")
        except sqlite3.OperationalError:
            self.create_table()
            self.select()
        return result

    def update(self):
        try:
            result = conn.execute("SELECT id, name, address, salary  from COMPANY")
        except sqlite3.OperationalError:
            self.create_table()
            self.select()
        return result

    def create_table(self):
        try:
            result = conn.execute("SELECT id, name, address, salary  from COMPANY")
        except sqlite3.OperationalError:
            self.create_table()
            self.select()
        return result
