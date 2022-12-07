import pymysql


class DbConn:
    __slots__ = ["connection"]

    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost', port=3306, user='root',
            password='jayyeon0802', db='dummy_tube', charset='utf8'
        )

