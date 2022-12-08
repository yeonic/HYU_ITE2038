from pymysql import err
import re
from typing import *
from channelService import *


class UserService:
    __slots__ = ["db", "channelService"]

    def __init__(self, db):
        self.db = db
        self.channelService = ChannelService(self.db)

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
        sql = "INSERT INTO User(email, password, userName, mobileNum) " \
              "VALUES (%s, %s, %s, %s)"
        return self.db.exec_query_insert(sql, (email, password, name, pnum))

    def sign_up(self, email, password, name, pnum):
        # do insert op
        exit_code = self.create_user(email, password, name, pnum)

        if exit_code == 0:
            return 0

        # fetch userId added just above
        # to add as fk to default channel
        sql = "SELECT userId, chanCount, userName FROM User WHERE email=%s"
        result: Dict = self.db.exec_query_fetch(sql, args=(email), mode='one')

        # then create default channel
        res = self.channelService.create_channel(result["userName"], result["userId"], result["chanCount"])
        if res == 0:
            return 0

        # update channel count to 1
        sql = "UPDATE User SET chanCount = chanCount + 1 WHERE userId=%s"
        self.db.exec_query_insert(sql, args=(result["userId"]))

        return 1

    def sign_in(self, email, password):
        sql = "SELECT userId FROM User WHERE email=%s AND password=%s"
        result = self.db.exec_query_fetch(sql, "one", args=(email, password))

        if result is None:
            print("Login failed.")
            return 0

        print(result)

        return result["userId"]

    def get_channel_list(self, user_id):
        sql = 'SELECT chanId, channelName FROM Channel ' \
              'WHERE userNum = %s'
        return self.db.exec_query_fetch(sql, "all", (user_id))

    def delete_channel(self, user_id, chan_id):
        sql = 'DELETE FROM c ' \
              'USING Channel as c ' \
              'LEFT JOIN User as u ' \
              'ON u.userId = c.userNum ' \
              'WHERE u.userId = %s ' \
              'AND c.chanId = %s'
        return self.db.exec_query_insert(sql, (user_id, chan_id))


