from dummy_server.dbConn import DbConn


class VideoService:
    __slots__ = ["db"]

    def __init__(self, db: DbConn):
        self.db = db

    def get_videos_to_feed(self):
        sql = 'SELECT V.videoId, V.videoTitle, V.createdAt, V.hits, C.chanId ,C.channelName ' \
              'FROM Video V, Channel C WHERE V.chanNum = C.chanId '
        return self.db.exec_query_fetch(sql, "all")

    def get_others_videos_to_feed(self, other_chen_id):
        sql = 'SELECT V.videoId, V.videoTitle, V.createdAt, V.hits, C.chanId ,C.channelName ' \
              'FROM Video V, Channel C WHERE C.chanId=%s AND V.chanNum = C.chanId'
        return self.db.exec_query_fetch(sql, "all", (other_chen_id))

    def watch_video(self, current_chan, video_id):
        # increase hits
        sql1 = 'UPDATE Video SET hits = hits + 1 WHERE videoId =%s'
        code = self.db.exec_query_insert(sql1, (video_id))

        if code == 0:
            print("Failed to increase hit")
            return 0

        # update watch history
        # -> call create_history
        res = self.create_history(current_chan, video_id)

        if res == 0:
            print("failed to create history")
            return 0

        # fetch video
        sql = 'SELECT V.videoTitle, V.createdAt, V.hits, C.channelName ' \
              'FROM Video V, Channel C ' \
              'WHERE V.videoId = %s AND V.chanNum = C.chanId '

        return self.db.exec_query_fetch(sql, "one", (video_id))

    def add_to_playlist(self, plist_num, video_id):
        # make column with two arguments
        sql = 'INSERT INTO Contains(plistId, videoNum) VALUES (%s, %s)'
        return self.db.exec_query_insert(sql, (plist_num, video_id))

    def create_video(self, chan_id, title, detail=''):
        # create video
        sql = 'INSERT INTO Video(videoTitle, videoDetail, chanNum) ' \
              'VALUES (%s, %s, %s)'
        return self.db.exec_query_insert(sql, (title, detail, chan_id))

    def create_history(self, channel_id, video_id):
        sql1 = 'SELECT videoTitle From Video WHERE videoId = %s'
        res_dict = self.db.exec_query_fetch(sql1, "one", (video_id))

        if res_dict == 0:
            return 0

        sql = 'INSERT INTO WatchHistory(videoName, watchedBy) ' \
              'VALUES (%s, %s)'
        return self.db.exec_query_insert(sql, (res_dict["videoTitle"], channel_id))

    def update_video_detail(self, video_id, new_detail=''):
        sql = 'UPDATE Video SET videoDetail=%s ' \
              'WHERE videoId=%s'
        return self.db.exec_query_insert(sql, (new_detail, video_id))

    def delete_video(self, video_id):
        sql = 'DELETE FROM Video ' \
              'WHERE videoId=%s'
        return self.db.exec_query_insert(sql, (video_id))