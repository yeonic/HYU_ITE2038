from pymysql import err


class UserService:
    __slots__ = ["connection"]

    def __init__(self, connection):
        self.connection = connection

    def create_user(self, email, password, name, pnum):
        mail_regex = None
        num_regex = None

        try:
            with self.connection:
                with self.connection.cursor() as cursor:
                    sql = "INSERT INTO User(email, password, userName, mobileNum) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (email, password, name, pnum))
                    self.connection.commit()
        except err.IntegrityError as e:
            print('The email already exists. Try again')
            return 0


    def create_channel(self):
        pass
