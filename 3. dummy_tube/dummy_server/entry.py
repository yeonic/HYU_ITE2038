import dbConn
from userService import *

if __name__ == "__main__":
    db = dbConn.DbConn()
    user = UserService(db)

    user.create_user('ye1on@naver.com', 'password', 'yoen', '010-2179-9199')
    print('done well')
    pass
