from dbConn import DbConn

# open_code
# 0 -> open to everyone
# 1 -> do not open


class PlService:
    __slots__ = ["db"]

    def __init__(self, db: DbConn):
        self.db = db

    def create_playlist(self, current_chan_id, p_name):
        sql = 'INSERT INTO Playlist(channelNum, playlistName) ' \
              'VALUES (%s, %s)'
        return self.db.exec_query_insert(sql, (current_chan_id, p_name))

    def change_open_code(self, open_code, pl_id):
        sql = 'UPDATE Playlist SET openCode=%s ' \
              'WHERE playlistNum=%s'
        return self.db.exec_query_insert(sql, (open_code, pl_id))

    def get_my_playlists(self, current_chan_id):
        # get playlists
        # where chan_id = channelNum
        sql = 'SELECT playlistNum, playlistName, openCode ' \
              'FROM Playlist WHERE channelNum=%s'
        return self.db.exec_query_fetch(sql, (current_chan_id))

    def get_someones_playlists(self, some_chen_id):
        # get playlist
        # where channelNum = some_chan_id and open_code = 0
        sql = 'SELECT P.playlistNum, P.playlistName, C.channelName ' \
              'FROM Playlist P, Channel C ' \
              'WHERE P.channelNum = %s ' \
              'AND P.openCode = 0' \
              'AND P.channelNum = C.chanId'

        return self.db.exec_query_fetch(sql, (some_chen_id))

    def watch_playlist(self, now_p_num):
        # join playlist, contain, video, channel
        # then get playlistName, videoId, videoTitle, channelName
        sql = 'SELECT pl.playlistName, v.videoId, v.videoTitle, c.channelName ' \
              'FROM Contains as cs ' \
              'JOIN Playlist as pl ' \
              'ON pl.playlistNum = cs.plistId ' \
              'JOIN Video as v ' \
              'ON v.videoId = cd.plistId ' \
              'JOIN Channel as c ' \
              'ON c.chanId = pl.playlistNum ' \
              'WHERE pl.playlistNum = %s'

        return self.db.exec_query_fetch(sql, (now_p_num))


