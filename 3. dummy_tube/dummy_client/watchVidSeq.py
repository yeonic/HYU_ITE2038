from PyInquirer import prompt
from dummy_client.chanInfoSeq import other_chen_info_seq


def watch_vid_seq(services, curr_chen_id, video_id, video_owner_id):
    video_service = services["videoService"]

    res = video_service.watch_video(curr_chen_id, video_id)
    if res == 0:
        print("failed to play video.")
        return 0

    print("Now playing...\n")
    print(res["videoTitle"] + " | by " + res["channelName"]
          + " | " + str(res["createdAt"]) + " | hits: " + str(res["hits"]))
    print("00:06 ━⬤───────── 04:05\n")

    while True:
        answer = prompt([{
            "type": "list",
            "name": "vid_act",
            "message": "Choose your action.",
            "choices": ["Channel info", "Quit"]
        }])

        action = answer.get("vid_act")
        if action == "Quit":
            return 0
        else:
            res = other_chen_info_seq(services, video_owner_id)
            if res == 0:
                return 0
