from cli_tables.cli_tables import print_table


def print_video_as_table(video_list):
    table = [['ID', 'title', 'channel', 'created at', 'hits']]
    for video in video_list:
        table.append([str(video["videoId"]), video["videoTitle"],
                      video["channelName"], str(video["createdAt"]),
                      str(video["hits"])])

    print("\nVIDEOS IN FEED")
    print_table(table)
