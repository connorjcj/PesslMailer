import mySQLdb

class Database:

    host     = "localhost"
    user     = "testuser"
    password = "testpass"
    db       = "test"

    def __init__(self):
        self.connection = MySQLdb.connect( host = self.host,
                                           user = self.user,
                                           password = self.password,
                                           db = self.db )

    def query(self, q):
        cursor = self.connection.cursor( MySQLdb.cursors.DictCursor )
        cursor.execute(q)

        return cursor.fetchall()

    def __del__(self):
        self.connection.close


if __name__ == "__main__":
    db = Database()

    q = "DELETE FROM testTabel"

    db.query(q)

    q = """
    INSERT INTO testTable
    ('name, 'age)
    VALUES
    ('Mike', 39),
    ('Michael', 21),
    ('Angela', 21)
    """

    people = db.query(q)

    for person in people:
        print("Found: %s " % person["name"])