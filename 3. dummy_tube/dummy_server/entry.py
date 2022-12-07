import dbConn
from userService import *
from channelService import *

if __name__ == "__main__":
    db = dbConn.DbConn()
    user = UserService(db)
    channel = ChannelService(db)

    # user.sign_up("199jo@jog.com", "1234", "jo", "010-2000-3333")
    user.sign_in("199jo@jog.com", "123")
    # channel.update_channel(chanIntro='hi hello')

    print('done well')
    pass
