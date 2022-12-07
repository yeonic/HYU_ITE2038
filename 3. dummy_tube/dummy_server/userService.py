from pymysql import err
import re


class UserService:
    __slots__ = ["db"]

    def __init__(self, db_conn):
        self.db = db_conn

    def create_user(self, email, password, name, pnum):
        mail_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        num_regex = re.compile(r'^(01)\d-\d{3,4}-\d{4}$')

        # email validation
        if not re.match(mail_regex, email):
            print('invalid email, try again.')
            return 0

        # mobile phone number validation
        if not re.match(num_regex, pnum):
            print('invalid phone number. Check if you\'ve forgotten hyphen(-)')
            return 0

        # do insert op
        sql = "INSERT INTO User(email, password, userName, mobileNum) VALUES (%s, %s, %s, %s)"
        return self.db.exec_query_insert(sql, (email, password, name, pnum))

    def sign_up(self, email, password, name, pnum):
        # do insert op
        exit_code = self.create_user(email, password, name, pnum)

        if exit_code == 0:
            return 0

        # fetch userId added just above
        # to add as fk to default channel
        sql = "SELECT userId FROM User WHERE email=%s"
        userId = self.db.exec_query_fetch(sql, args=(email), mode='one')

        # then create default channel

