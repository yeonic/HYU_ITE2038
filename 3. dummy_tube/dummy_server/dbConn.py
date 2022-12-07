import pymysql
import pymysql.cursors


class DbConn:
    __slots__ = ["connection"]

    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost', port=3306, user='root',
            password='jayyeon0802', db='dummy_tube', charset='utf8'
        )

    def _connect(self):
        self.connection = pymysql.connect(
            host='localhost', port=3306, user='root',
            password='jayyeon0802', db='dummy_tube', charset='utf8'
        )

    def exec_query_insert(self, sql, args=()):
        if not self.connection.open:
            self._connect()

        try:
            with self.connection:
                with self.connection.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
                    cursor.execute(sql, args)
                    self.connection.commit()
            return 1

        except pymysql.err.Error as e:
            print(e)
            return 0

    def exec_query_fetch(self, sql, mode, args=()):
        if not self.connection.open:
            self._connect()

        try:
            with self.connection:
                with self.connection.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
                    cursor.execute(sql, args)
                    return cursor.fetchone() if mode == 'one' else cursor.fetchall()

        except pymysql.err.Error as e:
            print(e)
            return 0
