from dummy_server.dbConn import DbConn


class ChannelService:
    __slots__ = ["db"]

    def __init__(self, db: DbConn):
        self.db = db

    def create_channel(self, name, userid, chan_count):
        if chan_count > 5:
            print('you cannot create over 5 channels')
            return 0

        sql = 'INSERT INTO Channel(channelName, userNum) ' \
              'VALUES (%s, %s)'
        return self.db.exec_query_insert(sql, (name, userid))

    def update_intro(self, intro, chan_id):
        sql = 'UPDATE Channel SET chanIntro=%s WHERE chanId=%s'
        self.db.exec_query_insert(sql, (intro, chan_id))
        return 1

    def check_name_overlap(self, name):
        sql = 'SELECT chanId FROM Channel WHERE channelName=%s'
        return self.db.exec_query_fetch(sql, "one", (name))

    def update_name(self, name, chan_id):
        sql = 'UPDATE Channel SET channelName=%s WHERE chanId=%s'
        self.db.exec_query_insert(sql, (name, chan_id))
        return 1

    def get_channel_data(self, chan_id):
        sql = 'SELECT chanIntro, createdAt FROM Channel ' \
              'WHERE chanId=%s'
        return self.db.exec_query_fetch(sql, "one", args=(chan_id))

    def watch_history(self, chan_id):
        sql = 'SELECT C.chanId, C.channelName, W.videoName, W.watchDate, W.historyNum ' \
              'FROM Channel C, WatchHistory W ' \
              'WHERE C.chanId=%s AND C.chanId = W.watchedBy'
        return self.db.exec_query_fetch(sql, "all", (chan_id))

    def delete_history(self, hist_id):
        sql = 'DELETE FROM WatchHistory ' \
              'WHERE historyNum=%s'
        return self.db.exec_query_insert(sql, (hist_id))
