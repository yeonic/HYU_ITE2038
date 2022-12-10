from PyInquirer import prompt
from cli_tables.cli_tables import print_table

from dummy_client.utils.print_table import print_video_as_table

quit_q = [{
    "type": "list",
    "name": "quit",
    "message": "",
    "choices": ["Quit"]
}]


def other_chen_info_seq(services, other_chen_num):
    # services used in this sequence
    pl_service = services["plService"]
    video_service = services["videoService"]
    chan_service = services["channelService"]

    res = chan_service.get_channel_data(other_chen_num)
    if res == 0:
        print("Failed to fetch info.")
        return 0

    print("CHANNEL INFO")
    print("INTRO: " + res["chanIntro"] + "\n" + "CREATED_AT: " + str(res["createdAt"]))

    answer = prompt([{
        "type": "list",
        "name": "what_to_do",
        "message": "tell me what you want to do with this channel.",
        "choices": ["Show videos", "Show playlists", "Quit"]
    }])

    action = answer.get("what_to_do")

    if action == "Show videos":
        res = video_service.get_others_videos_to_feed(other_chen_num)
        if res == 0:
            return 0
        print_video_as_table(res)

        answer = prompt(quit_q)

        if answer.get("quit") == "Quit":
            return 0

    elif action == "Show playlists":
        res = pl_service.get_someones_playlists(other_chen_num)
        if res == 0:
            return 0

        print_playlist_as_table(res)

        answer = prompt(quit_q)

        if answer.get("quit") == "Quit":
            return 0

    else:
        return 0


def print_playlist_as_table(pl_list):
    table = [["playlist_id", "playlist_name", "created by"]]
    for pl_item in pl_list:
        table.append([
            str(pl_item["playlistNum"]),
            pl_item["playlistName"], pl_item["channelName"]
        ])
    print_table(table)


def my_chen_info_seq(services):
    pass


