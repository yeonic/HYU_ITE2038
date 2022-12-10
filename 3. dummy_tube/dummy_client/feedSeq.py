from PyInquirer import prompt
from dummy_client.utils.print_table import print_video_as_table

from dummy_client.watchVidSeq import watch_vid_seq


feed_seq_q = [{
        "type": "list",
        "name": "action",
        "message": "Choose action",
        "choices": ["Watch", "Quit"]
}]

what_to_watch = [{
        "type": "input",
        "name": "what_to_watch",
        "message": "Type ID of a video to watch:"
}]


def find_userid_by_videoid(video_list, video_id):
    for video_item in video_list:
        if int(video_item["videoId"]) == video_id:
            return video_item["chanId"]


def feed_seq(services, current_user):
    video_services = services["videoService"]

    # fetch videos to feed
    video_list = video_services.get_videos_to_feed()

    if video_list == 0:
        print('Video load failed. Return to main menu.')
        return 0

    print_video_as_table(video_list)

    # inquire
    answer = prompt(feed_seq_q)
    action = answer.get("action")

    if action == "Watch":
        # watch video seq
        answer = prompt(what_to_watch)
        vid_id = answer.get("what_to_watch")
        vid_owner_id = find_userid_by_videoid(video_list, int(vid_id))
        res = watch_vid_seq(services, current_user["userId"],
                            vid_id, vid_owner_id)
        if res == 0:
            return 0
    else:
        print("Return to main.")
        return 0




