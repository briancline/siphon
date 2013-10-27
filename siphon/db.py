import sqlite3


class DBManager(object):
    SchemaVersion = 1

    def __init__(self, file_name):
        self._file = file_name
        self._conn = sqlite3.connect(self._file)
        self.create_db()

    def create_db(self):
        cursor = self._conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS _metadata ("
                       "version INT"
                       ")")
        cursor.execute("INSERT INTO _metadata VALUES (%d)" %
                       self.SchemaVersion)

        cursor.execute("CREATE TABLE IF NOT EXISTS remote_files ("
                       "sum TEXT(32), "
                       "name TEXT, "
                       "path TEXT, "
                       "retrieved INT(1)"
                       ")")

        cursor.execute("CREATE TABLE IF NOT EXISTS local_files ("
                       "sum TEXT(32), "
                       "name TEXT, "
                       "path TEXT"
                       ")")

    def version(self):
        cursor = self._conn.cursor()
        result = cursor.execute("SELECT version FROM _metadata")
        return result.fetchone()[0]

    def get_all_remote(self):
        cursor = self._conn.cursor()
        result = cursor.execute("SELECT sum, name, path FROM remote_files")
        return result.fetchall()

    def get_sum(self, sum=None, name=None):
        if sum is None and name is None:
            return None

        if sum is not None:
            criteria = "sum = '%s'" % sum
        elif name is not None:
            criteria = "name = '%s'" % sum

        cursor = self._conn.cursor()
        result = cursor.execute("SELECT sum, name, path "
                                "FROM remote_files "
                                "WHERE %s" % criteria)
        return result.fetchone()

    def add_file(self, sum, name, path, retrieved=0):
        cursor = self._conn.cursor()
        cursor.execute("INSERT INTO remote_files VALUES(?, ?, ?, ?)",
                       (sum,
                        name.decode('utf-8', 'ignore'),
                        path.decode('utf-8', 'ignore'),
                        retrieved))
        self._conn.commit()
