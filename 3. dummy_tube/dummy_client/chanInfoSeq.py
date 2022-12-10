from PyInquirer import prompt

from dummy_client.utils.print_table import print_video_as_table, print_playlist_as_table

from dummy_client.myPlaylistSeq import my_playlist_seq
from dummy_client.myVideoSeq import my_video_seq
from dummy_client.editInfoSeq import edit_info_seq
from dummy_client.historySeq import history_seq

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

    while True:
        print("CHANNEL INFO")
        chan_intro = res["chanIntro"]
        print("INTRO: " + chan_intro + "\n" + "CREATED_AT: " + str(res["createdAt"]))

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
                print("Fetching videos failed.")
                continue

            print_video_as_table(res)

            answer = prompt(quit_q)

            if answer.get("quit") == "Quit":
                continue

        elif action == "Show playlists":
            res = pl_service.get_someones_playlists(other_chen_num)
            if res == 0:
                print("Fetching playlists failed.")
                continue

            print_playlist_as_table(res)

            answer = prompt(quit_q)

            if answer.get("quit") == "Quit":
                continue

        else:
            print("Return to menu.")
            return 0


def my_chen_info_seq(services, chen_id):
    chan_service = services["channelService"]
    res = chan_service.get_channel_data(chen_id)

    if res == 0:
        print("Failed to load channel data.")
        return 0

    while True:
        print("CHANNEL INFO")
        chan_intro = res["chanIntro"]
        print("INTRO: " + chan_intro + "\n" + "CREATED_AT: " + str(res["createdAt"]))

        answer = prompt([{
            "type": "list",
            "name": "my_chan_task",
            "message": "choose the task",
            "choices": ["My playlists", "My videos",
                        "Edit channel info", "Watch history",
                        "Quit"]
        }])
        task = answer.get("my_chan_task")

        if task == "My playlists":
            my_playlist_seq(services, chen_id)
            continue

        elif task == "My videos":
            my_video_seq(services, chen_id)
            continue

        elif task == "Edit channel info":
            edit_info_seq(services, chen_id)
            continue

        elif task == "Watch history":
            history_seq(services, chen_id)
            continue

        else:
            print("Back to menu.")
            return 0


