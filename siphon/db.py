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
        if not self.version():
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

    def get_sum(self, file_sum=None, file_name=None):
        if file_sum is None and file_name is None:
            return None

        criteria_values = ()

        if file_sum is not None:
            criteria = "sum = ?"
            criteria_values += (file_sum,)
        elif file_name is not None:
            criteria = "file_name = ?"
            criteria_values += (file_name,)

        cursor = self._conn.cursor()
        result = cursor.execute("SELECT sum, name, path "
                                "FROM remote_files "
                                "WHERE %s" % criteria,
                                criteria_values)
        return result.fetchone()

    def add_file(self, file_sum, file_name, path, retrieved=0):
        cursor = self._conn.cursor()
        cursor.execute("INSERT INTO remote_files VALUES(?, ?, ?, ?)",
                       (file_sum,
                        file_name.decode('utf-8', 'ignore'),
                        path.decode('utf-8', 'ignore'),
                        retrieved))
        self._conn.commit()
