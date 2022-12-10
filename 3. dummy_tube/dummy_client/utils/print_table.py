from cli_tables.cli_tables import print_table


def print_video_as_table(video_list):
    table = [['ID', 'title', 'channel', 'created at', 'hits']]
    for video in video_list:
        table.append([str(video["videoId"]), video["videoTitle"],
                      video["channelName"], str(video["createdAt"]),
                      str(video["hits"])])

    print("\nVIDEOS")
    print_table(table)


def print_history_as_table(hist_list):
    table = [['History ID', 'Video name', 'Watched at']]
    for hist in hist_list:
        table.append([
            str(hist["historyNum"]), hist["videoName"],
            str(hist["watchDate"])
        ])

    print("\nWATCH HISTORY")
    print_table(table)


def print_playlist_as_table(pl_list):
    table = [["playlist_id", "playlist_name", "created by"]]
    for pl_item in pl_list:
        table.append([
            str(pl_item["playlistNum"]),
            pl_item["playlistName"], pl_item["channelName"]
        ])
    print_table(table)


def print_my_playlist_table(pl_list):
    table = [["playlist ID", "name", "open to"]]
    for pl_item in pl_list:
        table.append([
            str(pl_item["playlistNum"]), pl_item["playlistName"],
            "global" if pl_item["openCode"] == 0 else "private"
        ])
    print_table(table)
