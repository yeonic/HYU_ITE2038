import dbConn
from userService import *

if __name__ == "__main__":
    db = dbConn.DbConn()
    user = UserService(db.connection)

    user.create_user('yeon@naver.com', 'password', 'yoen', '010-2179-9199')
    print('done well')
    pass
